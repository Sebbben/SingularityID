from flask import request, jsonify
import src.utils.requestDefs as requestDefs
from src.utils.sessionHandler import SessionManager
import datetime


def session_token():

    data: dict[str, str] = request.get_json()

    if not (
        "access_token" in data and 
        "refresh_token" in data and 
        "expires_in" in data
    ): return requestDefs.bad_request("Missing access_token, refresh_token or expires_in in request body")

    # TODO: Verify token and expiration time formats before adding to database

    expires_at = datetime.datetime.now() + datetime.timedelta(seconds=int(data["expires_in"]))

    session = SessionManager.get_instance().create_session(
        data["refresh_token"],
        data["access_token"],
        expires_at
    )

    if not session:
        return requestDefs.internal_server_error("Something went wrong with session token creation")
 

    return jsonify({
        "session_token": session["session_token"]
    })
    