from flask import request, redirect
import src.utils.requestDefs as requestDefs
from src.db import DatabaseManager
import bcrypt
import re
from src.utils.general import URL
from src.utils.auth import OAuth
from src.config import Config


def isValidPassword(password):
    """
    A strong password:
    - At least 9 characters
    - Contains uppercase and lowercase letters
    - Contains digits
    - Contains special characters
    """

    if len(password) < 9:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def hasRequiredRegisterParams(params):
    return all([
        field in params for field in [
            "username", 
            "password", 
            "confirm_password", 
            "terms"
        ]
    ])

def isPasswordMatch(password, confirmPassword):
    return password == confirmPassword

def isTermsAccepted(terms):
    return terms == "true"

def isValidRegisterForm(params):
    return hasRequiredRegisterParams(params) and \
    isValidPassword(params["password"]) and \
    isPasswordMatch(params["password"], params["confirm_password"]) and \
    isTermsAccepted(params["terms"])

def register():
    """
    POST /auth/register
    Handles user registration.
    Request JSON body:
    {
        "username": "string",
        "password": "string",
        "confirm_password": "string",
        "terms": "true",
        "client_id": "string",
        "response_type": "string",
        "redirect_uri": "string",
        "state": "string"
    }
    Response:
    - 302 Redirect with authorization code
    - 400 Bad request
    - 409 Conflict
    - 500 Internal server error
    """
    if request.method != "POST": return requestDefs.method_not_allowed()
    json = request.get_json()
    
    if not json: return requestDefs.bad_request("Request body must be JSON")

    if not OAuth.isValidGrantReqest(json):
        return requestDefs.bad_request("Invalid grant request")

    if not isValidRegisterForm(json):
        return requestDefs.bad_request("Bad register form")


    db = DatabaseManager.get_instance().get_db(Config.IDP_DB_NAME)

    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (json["username"],))
            if cur.fetchone():
                return requestDefs.conflict("Username already exists")
            
            hashed_password = bcrypt.hashpw(json["password"].encode(), bcrypt.gensalt()).decode()
            cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id", (json["username"], hashed_password))
            userId = cur.fetchone()[0]
            conn.commit()


    


    code, expiresAt = OAuth.generateAuthenticationCode(json["client_id"], userId, json["redirect_uri"])

    extraParams = {
        "code": code,
        "expires_at": int(expiresAt.timestamp())
    } # TODO: Pass params like state through the redirect

    return requestDefs.redirectTemp(URL.addParamsToUriString(json["redirect_uri"], extraParams))