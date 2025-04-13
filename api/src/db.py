import psycopg
from psycopg_pool import ConnectionPool
import os

class Database:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection_pool = None
        self.open_connections = []

    def initialize_pool(self) -> None:
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

class DatabaseManager:
    instance = None

    def __init__(self):
        self.DBs: dict[str, Database] = {}

        self.init_db(os.getenv("IDP_DB"))
        self.init_db(os.getenv("APP_DB"))

    def init_db(self, database):
        db_config = {
            'user': os.getenv("POSTGRES_USER"),
            'password': os.getenv("POSTGRES_PASSWORD"),
            'host': os.getenv("DATABASE_HOST"),
            'port': os.getenv("DATABASE_PORT"),
            'database': database
        }

        self.DBs[database] = Database(db_config)
        self.DBs[database].initialize_pool()

    def get_db(self, database):
        if database not in self.DBs:
            raise NameError(f"Database {database} not initiated")
        return self.DBs[database]

    @staticmethod
    def get_instance():
        if DatabaseManager.instance == None:
            DatabaseManager.instance = DatabaseManager()
        
        return DatabaseManager.instance



    def tear_down_DBs(self):
        for name, db in self.DBs:        
            db.close_all_connections()