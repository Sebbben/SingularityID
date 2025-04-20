import urllib.parse
from flask import request, jsonify
import src.utils.auth as auth
from src.db import DatabaseManager
from src.utils.sessionHandler import SessionManager
from src.config import Config
import src.utils.requestDefs as requestDefs
import urllib

def clients():
    if not auth.is_logged_in():
        return auth.login_redirect_response()
    
    if request.method == "GET":
        if "client_id" in request.args:
            if not has_permission(request.args.get("client_id")): return requestDefs.forbidden("Client does not exist or you do not have permission")
            return get_clients(request.args.get("client_id"))
        else:
            return get_clients()

    elif request.method == "POST":
        return requestDefs.internal_server_error("Not implemented")

    return requestDefs.method_not_allowed()
    
# TODO: refactor client handling into own file / class
def get_clients(client_id = None):
    db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)

    session = SessionManager.get_instance().get_session(request.cookies.get("session_token"))

    with db.connection() as conn:
        with conn.cursor() as cur:
            query = """
            SELECT id, name, access_token_lifetime, refresh_token_lifetime
            FROM clients
            WHERE owner_id = (
                SELECT user_id
                FROM access_tokens
                WHERE token = %s
                LIMIT 1
            )
            """
            params = [session["access_token"]]

            if not client_id is None:
                query += "AND id = %s"
                params.append(client_id)
            cur.execute(query, params)

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

def has_permission(client_id):
    db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)

    session = SessionManager.get_instance().get_session(request.cookies.get("session_token"))

    with db.connection() as conn:
        with conn.cursor() as cur:
            query = """
            SELECT 1
            FROM clients
            WHERE id = %s AND
            owner_id = (
                SELECT user_id
                FROM access_tokens
                WHERE token = %s
                LIMIT 1
            )
            AND id = %s
            """
            params = [client_id, session["access_token"]]

            cur.execute(query, params)

            res = cur.fetchall()

            return len(res) == 1