from flask import Flask
from src.config import Config
import os

from src.db import DatabaseManager
from src.utils import init_singularity_client

from src.auth.login import login
from src.auth.token import token
from src.auth.logout import logout
from src.auth.register import register
from src.auth.register_client import register_client
from src.auth.resetPassword import resetPassword
from src.routes.session_token import session_token

app = Flask(__name__)
app.config.from_object(Config)


app.add_url_rule("/auth/login", None, login, methods=["POST"])
app.add_url_rule("/auth/token", None, token, methods=["POST"])
app.add_url_rule("/auth/register", None, register, methods=["POST"])
app.add_url_rule("/auth/register_client", None, register_client, methods=["POST"])
app.add_url_rule("/session_token", None, session_token, methods=["POST"])
# app.add_url_rule("/auth/logout", None, logout, methods=["POST"])
# app.add_url_rule("/auth/resetPassword", None, resetPassword, methods=["POST"])

DatabaseManager.get_instance()

@app.teardown_appcontext
def tearDown(c):
    DatabaseManager.get_instance().tear_down_DBs()

if __name__ == '__main__':
    init_singularity_client()
    app.run(debug=os.environ["DEBUG"], host="0.0.0.0", port=3000)
