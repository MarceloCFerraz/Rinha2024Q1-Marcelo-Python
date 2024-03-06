import os

from gevent.queue import Queue

# from psycopg2.pool import SimpleConnectionPool
from psycopg2 import Error, connect


class DbManager:
    connection_pool: Queue

    def __init__(self) -> None:
        # API_PORT=8081
        # DB_PORT=5432
        # DB_HOSTNAME=db
        # DB_NAME=rinha
        # DB_USER=admin
        # DB_PASS=mystrongpassword
        # MAX_WORKERS=10
        # MAX_FIBERS=10
        # MAX_DB_CONNECTIONS=100
        db_port = os.getenv("DB_PORT")
        if db_port is None:
            db_port = 5432
        else:
            db_port = int(db_port)

        db_host = os.getenv("DB_HOSTNAME")
        if db_host is None:
            db_host = "db"

        db_name = os.getenv("DB_NAME")
        if db_name is None:
            db_name = "rinha"

        db_user = os.getenv("DB_USER")
        if db_user is None:
            db_user = "admin"

        db_pass = os.getenv("DB_PASS")
        if db_pass is None:
            db_pass = "mystrongpassword"

        db_cons = os.getenv("MAX_DB_CONNECTIONS")
        if db_cons is None:
            db_cons = 100
        else:
            db_cons = int(db_cons)

        self.connection_pool = Queue(db_cons)

        self.fill_conn_pool(db_port, db_host, db_name, db_user, db_pass, db_cons)

    def fill_conn_pool(self, db_port, db_host, db_name, db_user, db_pass, db_cons):
        print(f"Initializing connection pool with {db_cons} connections")

        for i in range(0, db_cons):
            try:
                conn = connect(
                    host=db_host,
                    database=db_name,
                    port=db_port,
                    user=db_user,
                    password=db_pass,
                )
                self.connection_pool.put(conn)
            except (Exception, Error) as error:
                print(f"Error creating connection {i}:\n{error}")

    def execute_query(self, query: str, params: tuple | None) -> list[tuple] | None:
        response = None
        with self.connection_pool.get() as conn:
            try:
                if conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query=query, vars=params)
                        # conn.commit()  # Commit if needed

                        response = cursor.fetchall()
            except (Exception, Error):
                print(f"Error with connection{conn}")
            finally:
                self.connection_pool.put_nowait(conn)
                # print("Re-queuing connection")
                return response
