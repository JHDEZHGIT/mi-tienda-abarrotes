# tests/system/test_postgres_db.py

import pytest

from appweb.postgres_db import pgdb


# PGDB ROLLBACK
# =========================================================
def test_pgdb_rollback():
    with pytest.raises(Exception):
        with pgdb.get_cursor() as cur:
            cur.execute("SELECT * FROM tabla_que_no_existe")