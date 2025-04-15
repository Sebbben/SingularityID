from flask import request, jsonify
import src.requestDefs as requestDefs
from src.db import DatabaseManager
from src.config import Config
import datetime


def session_token():
    db = DatabaseManager.get_instance().get_db(Config.APP_DB_NAME)

    data: dict[str, str] = request.get_json()

    if not ("refresh_token" in data and "expires_in" in data): return requestDefs.bad_request("Missing refreshtoken or expiration time in request body")

    # TODO: Verify token and expiration time formats before adding to database

    expires_at = datetime.datetime.now() + datetime.timedelta(seconds=int(data["expires_in"]))

    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO token_pairs(refresh_token, expires_at) VALUES (%s, %s) RETURNING session_token", (data["refresh_token"], expires_at))
            res = cur.fetchone()

            conn.commit()

        return jsonify({
            "session_token": res[0]
        })
    
    return requestDefs.internal_server_error("Something went wrong with session token creation")