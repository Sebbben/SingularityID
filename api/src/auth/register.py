from flask import request, redirect
import requestDefs
from db import getDB
import bcrypt
import re
import utils


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
    if request.method != "POST": return requestDefs.method_not_allowed()
    json = request.get_json()
    
    if not json: return requestDefs.bad_request("Request body must be JSON")

    if not utils.OAuth.isValidGrantReqest(json):
        return requestDefs.bad_request("Invalid grant request")

    if not isValidRegisterForm(json):
        return requestDefs.bad_request("Bad register form")

    with getDB().connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (json["username"],))
            if cur.fetchone():
                return requestDefs.conflict("Username already exists")
            
            hashed_password = bcrypt.hashpw(json["password"].encode(), bcrypt.gensalt()).decode()
            cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING user_id", (json["username"], hashed_password))
            userId = cur.fetchone()[0]
            conn.commit()


    


    code, expiresAt = utils.OAuth.generateAuthenticationCode(json["client_id"], userId, json["redirect_uri"])

    extraParams = {
        "code": code,
        "expires_at": int(expiresAt.timestamp())
    } # TODO: Pass params like state through the redirect

    return requestDefs.redirectTemp(utils.addParamsToUriString(json["redirect_uri"], extraParams))