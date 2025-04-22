from src.config import Config
from src.db import DatabaseManager
from datetime import datetime, timedelta

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

    def get_session(self, session_token):
        return self.session_cache[session_token] if session_token in self.session_cache else None
    

    def get_session_status(self, session_token: str):
        session = self.get_session(session_token)
        if not session: return "error"

        now = datetime.now()
        if session["expires_at"] < now:
            return "expired"
        elif session["expires_at"] - now < timedelta(minutes=15):
            return "deathbed"
        
        return "active"

    def has_session(self, session_token) -> bool:
        return session_token in self.session_cache and self.get_session_status(session_token) in ("active", "deathbed")
