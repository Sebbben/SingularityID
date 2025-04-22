from src.db import DatabaseManager
from src.config import Config
from flask import request
from src.utils.sessionHandler import SessionManager
import src.utils.requestDefs as requestDefs

class ClientManager:
    @staticmethod
    def get_clients(**client_filter) -> list[dict]:
        """
        Returns a list of clients the user has permission to see
        """
        if "client_id" in client_filter and not ClientManager.has_permission(request.args.get("client_id")): return requestDefs.forbidden("Client does not exist or you do not have permission")

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

                if "client_id" in client_filter:
                    query += "AND id = %s"
                    params.append(client_filter["client_id"])

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
        return client_dict_list
    

    @staticmethod
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
                """
                params = [client_id, session["access_token"]]

                cur.execute(query, params)

                res = cur.fetchall()

                return len(res) == 1