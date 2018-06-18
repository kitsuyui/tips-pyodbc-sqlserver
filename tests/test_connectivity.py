from nose.tools import ok_
import pyodbc

from utils import get_connection_string


def test_connectivity():
    conn = pyodbc.connect(get_connection_string())
    conn.execute('SELECT 1')
    ok_(True)
    conn.close()
