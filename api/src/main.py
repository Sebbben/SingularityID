from flask import Flask
from config import Config
import os

from db import init as initDB
from db import tearDownDB

from auth.login import login
from auth.token import token
from auth.logout import logout
from auth.register import register
from auth.resetPassword import resetPassword

app = Flask(__name__)
app.config.from_object(Config)


app.add_url_rule("/auth/login", None, login, methods=["POST"])
app.add_url_rule("/auth/token", None, token, methods=["POST"])
app.add_url_rule("/auth/register", None, register, methods=["POST"])
# app.add_url_rule("/auth/logout", None, logout, methods=["POST"])
# app.add_url_rule("/auth/resetPassword", None, resetPassword, methods=["POST"])

initDB()


@app.teardown_appcontext
def tearDown(c):
    tearDownDB()

if __name__ == '__main__':
    app.run(debug=os.environ["DEBUG"], host="0.0.0.0", port=3000)
