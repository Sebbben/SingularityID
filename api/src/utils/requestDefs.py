from flask import jsonify, make_response

def ok(data=None, message="OK"):
    response = {
        "status": "success",
        "message": message,
        "data": data
    }
    return make_response(jsonify(response), 200)

def created(message="Resource created"):
    response = {
        "status": "success",
        "message": message
    }
    return make_response(jsonify(response), 201)

def bad_request(message="Bad request"):
    response = {
        "status": "fail",
        "message": message
    }
    return make_response(jsonify(response), 400)

def unauthorized(message="Unauthorized"):
    response = {
        "status": "fail",
        "message": message
    }
    return make_response(jsonify(response), 401)

def forbidden(message="Forbidden"):
    response = {
        "status": "fail",
        "message": message
    }
    return make_response(jsonify(response), 403)

def not_found(message="Resource not found"):
    response = {
        "status": "fail",
        "message": message
    }
    return make_response(jsonify(response), 404)

def conflict(message="Conflict"):
    response = {
        "status": "fail",
        "message": message
    }
    return make_response(jsonify(response), 409)

def internal_server_error(message="Internal server error"):
    response = {
        "status": "error",
        "message": message
    }
    return make_response(jsonify(response), 500)

def method_not_allowed(message="Method not allowed"):
    response = {
        "status": "fail",
        "message": message
    }
    return make_response(jsonify(response), 405)

def redirectTemp(url):
    response = {
        "redirect_uri": url
    }
    print(response, flush=True)
    return jsonify(response), 302