from urllib.parse import urlparse, urlunparse, urlencode
from src.db import DatabaseManager
import datetime, os

class OAuth:
    def isValidClient(client_id): 
        db = DatabaseManager.get_instance().get_db(os.getenv("AUTH_DB"))
        with db.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM clients WHERE id=%s", (client_id,))
                res = cursor.fetchall()
                if len(res) != 1:
                    return Result.Error("Invalid client")
                else:
                    return Result.Ok()

    def isValidRedirectUri(client_id, redirect_uri):
        # TODO: Do url validation before check
        db = DatabaseManager.get_instance().get_db(os.getenv("AUTH_DB"))
        with db.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT redirect_uri FROM client_redirect_uris WHERE client_id = %s AND redirect_uri = %s", (client_id, redirect_uri))
                res = cursor.fetchall()

                if len(res) == 1:
                    return Result.Ok()
                return Result.Error("Invalid redirect url")

    def hasRequiredParams(params):
        if all([param in params for param in ["client_id", "redirect_uri", "response_type", "state"]]):
            return Result.Ok()
        return Result.Error("Missing required params")

    def isValidResponseType(response_type):
        return Result.Ok() if response_type in ["code"] else Result.Error("Invalid responsetype")

    def isValidGrantReqest(params):
        
        result = OAuth.hasRequiredParams(params)
        result.concat(OAuth.isValidClient(params["client_id"]))
        result.concat(OAuth.isValidRedirectUri(params["client_id"], params["redirect_uri"]))
        result.concat(OAuth.isValidResponseType(params["response_type"]))

        return result


    def generateAuthenticationCode(client_id, user_id, redirect_uri, scope="") -> tuple[str, datetime.datetime]:
        db = DatabaseManager.get_instance().get_db(os.getenv("AUTH_DB"))

        with db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO 
                            authorization_codes(client_id, user_id, redirect_uri, scope, code, expires_at) 
                            VALUES
                            (%s, %s, %s, %s, gen_random_uuid(), NOW()::timestamp + INTERVAL '10 min')
                            RETURNING code, expires_at""", (client_id, user_id, redirect_uri, scope))
                conn.commit()
                (code, expires_at) = cur.fetchone()


        return code, expires_at
    

    def makeAccessToken(client_id, user_id, scope) -> tuple[str, datetime.datetime]:
        db = DatabaseManager.get_instance().get_db(os.getenv("AUTH_DB"))

        with db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO
                            access_tokens(client_id, user_id, scope, token, expires_at)
                            VALUES
                            (%s, %s, %s, gen_random_uuid(), NOW()::timestamp + INTERVAL '1 hour') 
                            RETURNING token, expires_at
                            """, (client_id, user_id, scope))
                token, expires_at = cur.fetchone()

        return token, expires_at

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