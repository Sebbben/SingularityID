from urllib.parse import urlparse, urlunparse, urlencode
from src.db import DatabaseManager
import datetime, bcrypt
from src.config import Config



class URL:
    @staticmethod
    def makeUrlParamsString(params):
        return urlencode(params)

    @staticmethod
    def addParamsToUriString(url, params): # TODO: Check for url safety
        parsedUrl = urlparse(url)

        if parsedUrl.query == "":
            parsedUrl = parsedUrl._replace(query=URL.makeUrlParamsString(params))
        else:
            query = parsedUrl.query.split("&")
            query = {(split:=param.split("="))[0]: split[1] for param in query}

            params.update(query)
            parsedUrl = parsedUrl._replace(query=URL.makeUrlParamsString(params))

        return urlunparse(parsedUrl)
    

class Result:
    def __init__(self, success, error=None):
        self.success = success
        self.error = error if isinstance(error, list) else ([error] if error else [])

    @staticmethod
    def Ok():
        return Result(success=True)

    @staticmethod
    def Error(error):
        return Result(success=False, error=error)

    def is_ok(self):
        return self.success

    def is_error(self):
        return not self.success

    def get_errors(self):
        return self.error

    def concat(self, other):
        """Combine this result with another result."""
        if other.is_error():
            self.success = False
            self.error += other.error

        return self

    def __str__(self):
        if self.is_ok():
            return f"Result(Ok, errors={self.error})"
        return f"Result(Error, errors={self.error})"
    
def init_singularity_client():
    secret = Config.CLIENT_SECRET
    hashed_secret = bcrypt.hashpw(secret.encode('utf-8'), bcrypt.gensalt())

    db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)

    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM clients WHERE name='SingularityId'")
            res = cur.fetchone()
            if not res:
                hashed_password = bcrypt.hashpw(Config.ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt())
                cur.execute("INSERT INTO users(username, password_hash) VALUES (%s, %s) RETURNING id", ("admin", hashed_password))
                admin_id = cur.fetchone()[0]
                cur.execute("INSERT INTO clients(secret, name, owner_id) VALUES (%s, 'SingularityId', %s) RETURNING id", (hashed_secret, admin_id))
                res = cur.fetchone()
                cur.execute("INSERT INTO client_redirect_uris(client_id, redirect_uri) VALUES (%s, %s)", (res[0], "/authorize"))
                conn.commit()
                print(f"Your singularity id is: '{res[0]}'", flush=True)
