# src/appweb/postgres_db.py

from psycopg2.pool import ThreadedConnectionPool
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()

# ============================================
# CONFIG DB
# ============================================

db_config = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}


# ============================================
# POSTGRES DB
# ============================================

class PostgresDB:

    def __init__(self):

        self.pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=20,
            **db_config
        )

    @contextmanager
    def get_cursor(self):

        conn = self.pool.getconn()

        cur = conn.cursor()

        try:

            yield cur

            conn.commit()

        except Exception:

            conn.rollback()

            raise

        finally:

            cur.close()

            self.pool.putconn(conn)

    def init_app(self, app):
        pass


# ============================================
# INSTANCIA
# ============================================

pgdb = PostgresDB()