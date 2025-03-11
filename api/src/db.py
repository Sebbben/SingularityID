import psycopg
from psycopg_pool import ConnectionPool
import os

class Database:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection_pool = None
        self.open_connections = []

    def initialize_pool(self):
        connection_string = (
            f"postgresql://{self.db_config['user']}:{self.db_config['password']}@"+
            f"{self.db_config['host']}:{self.db_config['port']}/"+
            f"{self.db_config['database']}"
        )

        self.connection_pool = ConnectionPool(conninfo=connection_string)

    def _get_connection(self):
        if not self.connection_pool or self.connection_pool.closed:
            self.initialize_pool()
        new_connection = self.connection_pool.getconn()
        self.open_connections.append(new_connection)
        return new_connection

    def release_connection(self, connection):
        if self.connection_pool:
            self.open_connections.remove(connection)
            self.connection_pool.putconn(connection)

    def close_all_connections(self):
        if self.connection_pool:
            for conn in self.open_connections:
                self.connection_pool.putconn(conn)
            self.open_connections = []
            self.connection_pool.close()

    class ConnectionContext:
        def __init__(self, db_instance):
            self.db_instance = db_instance
            self.conn = None

        def __enter__(self) -> psycopg.Connection:
            self.conn = self.db_instance._get_connection()
            return self.conn

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.db_instance.release_connection(self.conn)

    def connection(self):
        return self.ConnectionContext(self)


DB = None
# Example usage
def init():
    global DB

    db_config = {
        'user': os.getenv("POSTGRES_USER"),
        'password': os.getenv("POSTGRES_PASSWORD"),
        'host': os.getenv("DATABASE_HOST"),
        'port': os.getenv("DATABASE_PORT"),
        'database': os.getenv("AUTH_DB")
    }

    DB = Database(db_config)
    DB.initialize_pool()


def getDB() -> Database:
    global DB

    if not DB:
        init()
    return DB

def tearDownDB():
    global DB

    if not DB: return
    
    DB.close_all_connections()