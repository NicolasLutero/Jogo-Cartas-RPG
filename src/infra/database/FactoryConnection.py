# FactoryConnection.py
import psycopg2
from psycopg2.extensions import connection


class FactoryConnection:
    _connection: connection | None = None

    @classmethod
    def get_connection(cls) -> connection:
        if cls._connection is None or cls._connection.closed:
            cls._connection = psycopg2.connect(
                host="localhost",
                port=5432,
                database="GeradorCartasBD",
                user="GenCartas",
                password="SenhaGenCartas"
            )

        return cls._connection

    @classmethod
    def close_connection(cls) -> None:
        if cls._connection and not cls._connection.closed:
            cls._connection.close()
            cls._connection = None
