from nose.tools import eq_
import pyodbc

from utils import get_connection_string


def test_connect_without_autocommit_then_transaction_count_become_1():
    conn = pyodbc.connect(get_connection_string())
    trancount, = conn.execute('SELECT @@TRANCOUNT').fetchone()
    eq_(trancount, 1)
    conn.close()


def test_connect_with_autocommit_then_transaction_count_become_0():
    conn = pyodbc.connect(get_connection_string(),
                          autocommit=True)
    trancount, = conn.execute('SELECT @@TRANCOUNT').fetchone()
    eq_(trancount, 0)
    conn.close()
