import psycopg
from urllib.parse import urlparse, urlunparse, urlencode
from db import getDB
import datetime

class OAuth:
    def isValidClient(client_id): 
        db = getDB()
        with db.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM clients WHERE id=%s", (client_id,))
                res = cursor.fetchall()
                if len(res) != 1:
                    return False
                else:
                    return True

    def isValidRedirectUri(client_id, redirect_uri):
        # TODO: Do url validation before check
        db = getDB()
        with db.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT redirect_uri FROM client_redirect_uris WHERE client_id = %s AND redirect_uri = %s", (client_id, redirect_uri))
                res = cursor.fetchall()

                return len(res) == 1

    def hasRequiredParams(params):
        return all([param in params for param in ["client_id", "redirect_uri", "response_type", "state"]])

    def isValidResponseType(response_type):
        return response_type in ["code"]

    def isValidGrantReqest(params):
        return OAuth.hasRequiredParams(params) and \
        OAuth.isValidClient(params["client_id"]) and \
        OAuth.isValidRedirectUri(params["client_id"], params["redirect_uri"]) and \
        OAuth.isValidResponseType(params["response_type"])


    def generateAuthenticationCode(client_id, user_id, redirect_uri, scope="") -> tuple[str, datetime.datetime]:

        with getDB().connection() as conn:
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
        with getDB().connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO
                            access_tokens(client_id, user_id, scope, token, expires_at)
                            VALUES
                            (%s, %s, %s, gen_random_uuid(), NOW()::timestamp + INTERVAL '1 hour') 
                            RETURNING token, expires_at
                            """)
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
    
