from flask import request, jsonify
import src.utils.auth as auth
from src.db import DatabaseManager
from src.utils.sessionHandler import SessionManager
from src.config import Config

def clients():
    if not auth.is_logged_in():
        return auth.login_redirect_response()
    
    db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)

    session = SessionManager.get_instance().get_session(request.cookies.get("session_token"))

    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT id, name, access_token_lifetime, refresh_token_lifetime
            FROM clients
            WHERE owner_id = (
                SELECT user_id
                FROM access_tokens
                WHERE token = %s
                LIMIT 1
            )
            """, (session["access_token"], ))

            res = cur.fetchall()

    client_dict_list = [
        {
            "id": id,
            "name": name,
            "access_token_lifetime": a_time,
            "refresh_token_lifetime": r_time
        } for id, name, a_time, r_time in res
    ]

    return jsonify({"clients": client_dict_list})