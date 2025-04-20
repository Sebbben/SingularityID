import psycopg
from psycopg_pool import ConnectionPool
import os
from src.config import Config

class Database:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection_pool = None
        self.open_connections = []

    def initialize_pool(self) -> None:

        if self.connection_pool:
            self.close_all_connections()


        connection_string = (
            f"postgresql://{self.db_config['user']}:{self.db_config['password']}@"+
            f"{self.db_config['host']}:{self.db_config['port']}/"+
            f"{self.db_config['database']}"
        )
        self.connection_pool = ConnectionPool(conninfo=connection_string)
        self.open_connections = []  # Clear stale connections

    def _get_connection(self):
        if not self.connection_pool or self.connection_pool.closed:
            self.initialize_pool()
        new_connection = self.connection_pool.getconn()
        self.open_connections.append(new_connection)
        return new_connection

    def release_connection(self, connection: psycopg.Connection):
        if self.connection_pool and connection in self.open_connections:
            self.open_connections.remove(connection)
            try:
                self.connection_pool.putconn(connection)
            except ValueError as e:
                print(f"Error returning connection to pool: {e}")
        else:
            print("Attempted to release a connection not tracked by the current pool.")
            if not connection.closed:
                connection.close()

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

        self.init_db(Config.IDP_DB_NAME)
        self.init_db(Config.APP_DB_NAME)

    def init_db(self, database):
        db_config = {
            'user': Config.POSTGRES_USER,
            'password': Config.POSTGRES_PASSWORD,
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
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
        for _, db in self.DBs.items():
            db.close_all_connections()