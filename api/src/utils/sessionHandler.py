from src.config import Config
from src.db import DatabaseManager
from datetime import datetime, timedelta
import requests

class SessionManager:
    _instance = None

    def __init__(self):
        self.session_cache = {}
        self.db = DatabaseManager.get_instance().get_db(Config.APP_DB_NAME)

    @staticmethod
    def get_instance():
        if not SessionManager._instance:
            SessionManager._instance = SessionManager()
        return SessionManager._instance
    
    def create_session(self, refresh_token: str, access_token: str, expires_at: datetime):
        with self.db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO token_pairs(refresh_token, expires_at) VALUES (%s, %s) RETURNING session_token", (refresh_token, expires_at))
                res = cur.fetchone()
                conn.commit()

        # TODO: Verify succesfull creation of token

        self.update_cache(res[0], access_token, refresh_token, expires_at)
        return self.get_session(res[0])

    def update_cache(self, session_token: str, access_token: str, refresh_token: str, expires_at: datetime):
        self.session_cache[session_token] = {
            "session_token": session_token,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at
        }

    def get_session(self, session_token, refresh = True) -> dict[str, str] | None:
        """
        Get the session from the session_token if the session exists
        If the session does not exist this method returns None
        If the session exists but is expired or soon to be, the session will be refreshed and then returned
        If the session is exists and is active the session is returned
        """
        # TODO: Verify that session is valid

        if session_token not in self.session_cache:
            session = self.load_session(session_token)
            if session is None: return None

        if not refresh: return self.session_cache[session_token]

        status = self.get_session_status(session_token)
        if status == "active":
            return self.session_cache[session_token]
        elif status == "deathbed" or status == "expired":
            self.refresh_session(session_token)
            return self.session_cache[session_token]
        else:
            return None # Something is wrong with session. TODO: Cleanup session?


        
    def load_session(self, session_token):
        """
        Fetches session from DB if it exists and caches it.
        Returns the session if it exists else None
        NOTE: Sessions loaded from DB will not have access_token. Extra steps are needed to refresh the session
        """
        with self.db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT session_token, refresh_token, expires_at FROM token_pairs WHERE session_token = %s", (session_token, ))
                res = cur.fetchall()
                if len(res) != 1: return None

        session_token, refresh_token, expires_at = res[0]
        self.update_cache(session_token, None,  refresh_token, expires_at)

        return self.session_cache[session_token]

    def get_session_status(self, session_token: str):
        session = self.session_cache[session_token] if session_token in self.session_cache else None
        if not session: return "error"

        now = datetime.now()
        if session["expires_at"] < now:
            return "expired"
        elif session["expires_at"] - now < timedelta(minutes=15):
            return "deathbed"
        
        return "active"

    def has_session(self, session_token) -> bool:
        return self.get_session(session_token) is not None

    def refresh_session(self, session_token):
        session = self.get_session(session_token, refresh=False)
        if not session or "refresh_token" not in session: return

        res = requests.post("http://api:3000/auth/token", json = {
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"]
        })


        if res.status_code == 400:
            self.revoke_tokens(refresh_token = session["refresh_token"])
            return

        tokens = None        
        try:
            tokens = res.json()
        except requests.exceptions.JSONDecodeError as e:
            print("Error while reading json of refresh api respose", flush=True)
        
        if tokens is None: return

        # TODO: Check correct expires_in format

        if "expires_in" in tokens:
            expires_at = datetime.now() - timedelta(seconds=int(tokens["expires_in"]))

        self.update_cache(session_token, tokens["access_token"], session["refresh_token"], expires_at)


    def revoke_tokens(self, session_token = None, access_token = None, refresh_token = None):
        with self.db.connection() as conn:
            with conn.cursor() as cur:        
                if session_token is not None:
                    cur.execute("DELETE FROM token_pairs WHERE session_token=%s", (session_token,))
                    conn.commit()

                if access_token is not None:
                    for session_token, session in self.session_cache.items():
                        if session["access_token"] == access_token:
                            # self.session_cache.remove(session)
                            session["access_token"] = None
                            self.refresh_session(session_token) # TODO: Should the entire session be revoken when revoking access_token?
                
                if refresh_token is not None:
                    cur.execute("DELETE FROM token_pairs WHERE refresh_token = %s RETURNING session_token", (refresh_token,))
                    conn.commit()
                    res = cur.fetchall()
                    if len(res) > 0:
                        for session_token in res:
                            if session_token in self.session_cache:
                                self.session_cache.pop(session_token)
