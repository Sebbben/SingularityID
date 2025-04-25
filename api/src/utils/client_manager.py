from src.db import DatabaseManager
from src.config import Config
from flask import request
from src.utils.sessionHandler import SessionManager
import src.utils.requestDefs as requestDefs
from src.utils.general import Result

class ClientManager:
    @staticmethod
    def get_clients(**client_filter) -> Result:
        """
        Returns a list of clients the user has permission to see
        """
        if "client_id" in client_filter and not ClientManager.has_permission(request.args.get("client_id")): return Result.Error("Client does not exist or you do not have permission")

        db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)
        session = SessionManager.get_instance().get_session(request.cookies.get("session_token"))

        client_dict_list = None
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


                for client in client_dict_list:
                    cur.execute("""
                                SELECT redirect_uri 
                                FROM clients as c
                                JOIN client_redirect_uris AS r
                                ON c.id = r.client_id
                                WHERE id = %s""", (client["id"], ))
                    
                    client["redirect_uris"] = [x[0] for x in cur.fetchall()]

                    cur.execute("""
                                SELECT grant_type 
                                FROM clients as c
                                JOIN client_grants AS g
                                ON c.id = g.client_id
                                WHERE id = %s""", (client["id"], ))
                    client["grants"] = [x[0] for x in cur.fetchall()]
                    
                    
        return Result.Ok(client_dict_list)
    

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