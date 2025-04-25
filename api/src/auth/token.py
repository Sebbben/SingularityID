from flask import request, jsonify
import src.utils.requestDefs as requestDefs
from src.utils.auth import OAuth

def token():
    """
    POST /auth/token
    Exchanges authorization code for access token.
    Request JSON body:
    {
        "grant_type": "authorization_code",
        "code": "string",
        "redirect_uri": "string",
        "client_id": "string"
    }
    Response:
    - 200 OK with access token
    - 400 Bad request
    - 500 Internal server error
    """
    
    data: dict[str, str] = request.get_json()

    # Checks for correct requets params and returns None if request params are incorrect
    request_type = OAuth.token_request_type(data) 

    if request_type is None:
        return requestDefs.bad_request("Incorrect params for request")
    elif request_type == "authorization_code":
        res = OAuth.authorization_code_exchange(data["code"], data["client_id"], data["redirect_uri"])
    elif request_type == "refresh_token":
        res = OAuth.refresh_token_exchange(data["refresh_token"])

    if res.is_ok():
        return jsonify(res.get_data())
    else:
        return requestDefs.bad_request("\n".join(res.get_errors()))