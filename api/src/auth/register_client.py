import requestDefs

def register_client():
    """
    POST /auth/register_client
    Handles client registration.
    Request JSON body:
    {
        "name": "string",
        "secret": "string",
        "redirect_uris": ["string"],
        "scopes": ["string"],
        "grant_types": ["string"]
    }
    Response:
    - 201 Created
    """
    return requestDefs.created()