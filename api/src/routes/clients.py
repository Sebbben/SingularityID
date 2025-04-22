from flask import request, jsonify
import src.utils.auth as auth
from src.config import Config
import src.utils.requestDefs as requestDefs

from src.db import DatabaseManager
from src.utils.sessionHandler import SessionManager
from src.utils.client_manager import ClientManager


def clients():
    if not auth.is_logged_in():
        return auth.login_redirect_response()
    
    if request.method == "GET":
        if "client_id" in request.args:
            clients_list = ClientManager.get_clients(client_id = request.args.get("client_id"))
            return jsonify(clients_list[0])
        else:
            return jsonify(ClientManager.get_clients())

    elif request.method == "POST":
        return requestDefs.internal_server_error("Not implemented")

    return requestDefs.method_not_allowed()
   