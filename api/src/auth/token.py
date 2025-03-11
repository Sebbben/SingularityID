from flask import request, jsonify
from db import getDB
import requestDefs
import utils
import datetime

def token():
    data: dict[str, str] = request.get_json()

    grant_type = data["grant_type"]
    code = data["code"]
    redirect_uri = data["redirect_uri"]
    client_id = data["client_id"]


    # TODO: Make util function for proper check of params per oauth spec
    if grant_type != "authorization_code":
        return requestDefs.bad_request("Invalid grant type")



    with getDB().connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id, scope FROM authorization_codes WHERE code=%s AND client_id = %s AND redirect_uri = %s AND expires_at <= NOW()", (code, client_id, redirect_uri))
            res = cur.fetchall()

    if len(res) == 0:
        return requestDefs.bad_request("Invalid authorization code")
    if len(res) != 1:
        return requestDefs.internal_server_error("Something whent wrong with token fetching")

    user_id, scope = res[0]
    access_token, access_expiration = utils.OAuth.makeAccessToken(client_id, user_id, scope)
    # refresh_token, refresh_expiration = utils.OAuth.makeRefreshToken(client_id, user_id, scope)

    access_expires_in = int((access_expiration-datetime.datetime.now()).total_seconds())

    return jsonify({
        "token_type": "bearer",
        "access_token": access_token,
        "expires_in": access_expires_in,
        # "refresh_token": refresh_token,
        "scope": scope
    })