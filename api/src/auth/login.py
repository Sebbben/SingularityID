from flask import request, jsonify
import bcrypt
from src.db import DatabaseManager
import src.requestDefs as requestDefs
import src.utils as utils

def login():
    """
    POST /auth/login
    Handles user login.
    Request JSON body:
    {
        "username": "string",
        "password": "string",
        "client_id": "string",
        "redirect_uri": "string",
        "response_type": "string",
        "state": "string"
    }
    Response:
    - 302 Redirect with authorization code
    - 400 Bad request
    - 401 Unauthorized
    - 500 Internal server error
    """

    data:dict[str,str] = request.get_json()

    username = data.get('username')
    password = data.get('password')
    client_id = data.get("client_id")
    redirect_uri = data.get("redirect_uri")
    response_type = data.get("response_type")
    state = data.get("state")

    grantValidationCheck = utils.OAuth.isValidGrantReqest({
        "client_id": client_id, 
        "redirect_uri": redirect_uri,
        "response_type": response_type,
        "state": state
    })
    
    if not grantValidationCheck.is_ok():
        return requestDefs.bad_request("Invalid grant request\n" + "\n".join(grantValidationCheck.get_errors()))

    if not username or not password:
        return requestDefs.bad_request("Missing username or password")

    db = DatabaseManager.get_instance().get_db(os.getenv("AUTH_DB"))

    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT password_hash FROM users WHERE username=%s", (username, ))
            res = cur.fetchone()
    
    if not res:
        return requestDefs.unauthorized("Wrong username or password")

    hashed_password = res[0]

    is_correct_password = bcrypt.checkpw(password.encode(), hashed_password.encode())

    if is_correct_password:

        with db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM users WHERE username=%s", (username, ))
                res = cur.fetchone()
        


        code, expiresAt = utils.OAuth.generateAuthenticationCode(client_id, res[0], redirect_uri)


        extraParams = {
            "code": code,
            "expires_at": int(expiresAt.timestamp())
        } # TODO: Pass params like state through the redirect

        return requestDefs.redirectTemp(utils.URL.addParamsToUriString(redirect_uri, extraParams))

    return requestDefs.internal_server_error("Something whent wrong during the authentication process")