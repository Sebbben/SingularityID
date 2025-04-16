import src.utils.requestDefs as requestDefs
from src.utils.general import URL
from src.config import Config
from flask import request
from src.utils.sessionHandler import SessionManager

def login_redirect_response():
    url = URL.addParamsToUriString("/login", {
        "response_type": "code",
        "client_id": Config.CLIENT_ID,
        "redirect_uri": "/authorize",
        "state": None
    })
    print(url, flush=True)
    return requestDefs.redirectTemp(url)

def is_logged_in():

    return (
        "session_token" in request.cookies and
        SessionManager.get_instance().has_session(request.cookies.get("session_token"))
    )