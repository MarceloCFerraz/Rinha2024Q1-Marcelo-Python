import os

from gevent.monkey import patch_all
from gevent.queue import Queue

# from psycopg2.pool import SimpleConnectionPool
from psycopg2 import Error, connect

patch_all()


class DbManager:
    connection_pool: Queue

    def __init__(self) -> None:
        db_port = os.getenv("DB_PORT")
        if db_port is None:
            db_port = 5432
        else:
            db_port = int(db_port)

        db_cons = os.getenv("MAX_DB_CONNECTIONS")
        if db_cons is None:
            db_cons = 10
        else:
            db_cons = int(db_cons)

        db_host = os.getenv("DB_HOSTNAME")
        if db_host is None:
            db_host = "localhost"

        db_name = os.getenv("DB_NAME")
        if db_name is None:
            db_name = "rinha"

        db_user = os.getenv("DB_USER")
        if db_user is None:
            db_user = "admin"

        db_pass = os.getenv("DB_PASS")
        if db_pass is None:
            db_pass = "mystrongpassword"

        self.connection_pool = Queue(db_cons)

        self.fill_conn_pool(db_port, db_host, db_name, db_user, db_pass, db_cons)

    def fill_conn_pool(self, db_port, db_host, db_name, db_user, db_pass, db_cons):
        print(f"Initializing connection pool with {db_cons} connections")
        print(
            f"Conn string: 'host={db_host};database={db_name};port={db_port};user={db_user};password={db_pass}'"
        )

        i = 0
        while i < db_cons:
            try:
                conn = connect(
                    host=db_host,
                    database=db_name,
                    port=db_port,
                    user=db_user,
                    password=db_pass,
                )
                self.connection_pool.put(conn)
                i += 1
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
            except (Exception, Error) as err:
                print(f"Error with connection {conn}")
                print(f"Type: {type(err)}")
                print(f"Error: {err}")
            finally:
                self.connection_pool.put(conn)
                # print("Re-queuing connection")
                return response
