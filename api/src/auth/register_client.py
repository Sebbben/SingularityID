import src.utils.requestDefs as requestDefs
import secrets
from src.db import DatabaseManager
from src.utils.sessionHandler import SessionManager
from flask import request
import bcrypt
from src.config import Config
import src.utils.auth as auth



def register_client():
    """
    POST /auth/register_client
    Handles client registration.
    Request JSON body:
    {
        "name": "string",
        "redirect_uris": ["string"],
        "scopes": ["string"],
        "grant_types": ["string"]
    }
    Response:
    - 201 Created
    - 400 Bad request
    - 409 Conflict
    """
    if request.method != "POST": return requestDefs.method_not_allowed()

    if not auth.is_logged_in(): return auth.login_redirect_response()

    json = request.get_json()

    if not json or not all(key in json for key in ["name", "redirect_uris", "scopes", "grant_types"]):
        return requestDefs.bad_request("Missing required fields")

    secret = secrets.token_urlsafe(32)
    hashed_secret = bcrypt.hashpw(secret.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


    db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)


    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM clients WHERE name = %s", (json["name"],))
            if cur.fetchone():
                return requestDefs.conflict("Client name already exists")

            access_token = SessionManager.get_instance().get_session(request.cookies.get("session_token"))["access_token"]
            cur.execute("SELECT user_id FROM access_tokens WHERE token=%s", (access_token, ))

            user_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO clients (secret, name, owner_id, access_token_lifetime, refresh_token_lifetime)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """, (hashed_secret, json["name"], user_id, 3600, 1209600)) # Access token lifetime 1h refreshtoken 2 weeks

            client_id = cur.fetchone()[0]

            for uri in json["redirect_uris"]:
                cur.execute("""
                    INSERT INTO client_redirect_uris (client_id, redirect_uri)
                    VALUES (%s, %s);
                """, (client_id, uri))

            for scope in json["scopes"]:
                cur.execute("""
                    INSERT INTO client_scope (client_id, scope)
                    VALUES (%s, %s);
                """, (client_id, scope))

            for grant in json["grant_types"]:
                cur.execute("""
                    INSERT INTO client_grants (client_id, grant_type)
                    VALUES (%s, %s);
                """, (client_id, grant))

            conn.commit()

    return requestDefs.created({"id": str(client_id), "secret": secret, "name": json["name"]})