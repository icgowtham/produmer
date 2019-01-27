"""Unit test(s) for the utility functions."""

import pytest

from utils.helpers import connect_to_db, disconnect_from_db


@pytest.mark.positive
def test_db_connection():
    """Unit test for testing the database connection."""
    conn = connect_to_db()
    assert conn
    disconnect_from_db(conn)
    assert conn.closed != 0
