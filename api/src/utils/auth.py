import src.utils.requestDefs as requestDefs
from src.utils.general import URL
from src.config import Config
from flask import request
from src.utils.sessionHandler import SessionManager
from src.db import DatabaseManager
import datetime, bcrypt
from src.utils.general import Result



def login_redirect_response():
    url = URL.addParamsToUriString("/login", {
        "response_type": "code",
        "client_id": Config.CLIENT_ID,
        "redirect_uri": "/authorize",
        "state": None
    })
    return requestDefs.redirectTemp(url)

def is_logged_in(): # Move to sessionHandler?
    return (
        "session_token" in request.cookies and
        SessionManager.get_instance().has_session(request.cookies.get("session_token"))
    )


class OAuth:
    def isValidClient(client_id): 
        db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)
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
        db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)
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
        db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)

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
        db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)

        with db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO
                            access_tokens(client_id, user_id, scope, token, expires_at)
                            VALUES
                            (%s, %s, %s, gen_random_uuid(), NOW()::timestamp + INTERVAL '1 hour') 
                            RETURNING token, expires_at
                            """, (client_id, user_id, scope))
                conn.commit()
                token, expires_at = cur.fetchone()

        return token, expires_at
    
    def makeRefreshToken(client_id, user_id, scope) -> tuple[str, datetime.datetime]:
        db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)

        with db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO
                            refresh_tokens(client_id, user_id, scope, token, expires_at)
                            VALUES
                            (%s, %s, %s, gen_random_uuid(), NOW()::timestamp + INTERVAL '1 hour') 
                            RETURNING token, expires_at
                            """, (client_id, user_id, scope))
                conn.commit()
                token, expires_at = cur.fetchone()

        return token, expires_at
    
    def verifyClientCredentials(client_id, secret):
        db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)

        with db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT secret FROM clients WHERE id = %s", (client_id,))
                result = cur.fetchone()

                if result is None:
                    return Result.Error("No client with this id")

                stored_secret = result[0].encode('utf-8')  # Ensure stored secret is in bytes
                provided_secret = secret.encode('utf-8')  # Convert provided secret to bytes

                if not bcrypt.checkpw(provided_secret, stored_secret):
                    return Result.Error("Incorrect client password")
                