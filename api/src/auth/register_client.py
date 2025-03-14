import requestDefs
import secrets
from db import getDB
from flask import request




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
    json = request.get_json()

    if not json or not all(key in json for key in ["name", "redirect_uris", "scopes", "grant_types"]):
        return requestDefs.bad_request("Missing required fields")

    secret = secrets.token_urlsafe(32)

    with getDB().connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM clients WHERE name = %s", (json["name"],))
            if cur.fetchone():
                return requestDefs.conflict("Client name already exists")

            cur.execute("""
                INSERT INTO clients (secret, name, access_token_lifetime, refresh_token_lifetime)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (secret, json["name"], 3600, 1209600)) # Access token lifetime 1h refreshtoken 2 weeks

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