from nose.tools import eq_, raises
import pyodbc

from utils import get_connection_string


def test_not_mars_not_autocommit():
    conn = pyodbc.connect(get_connection_string())
    conn.execute('BEGIN TRANSACTION')
    trancount, = conn.execute('SELECT 1').fetchone()
    conn.execute('COMMIT')
    eq_(trancount, 1)
    conn.close()


def test_mars_not_autocommit():
    conn = pyodbc.connect(get_connection_string(),
                          MARS_Connection='yes')
    conn.execute('BEGIN TRANSACTION')
    trancount, = conn.execute('SELECT 1').fetchone()
    conn.execute('COMMIT')
    eq_(trancount, 1)
    conn.close()


def test_not_mars_autocommit():
    conn = pyodbc.connect(get_connection_string(),
                          autocommit=True)
    conn.execute('BEGIN TRANSACTION')
    trancount, = conn.execute('SELECT 1').fetchone()
    conn.execute('COMMIT')
    eq_(trancount, 1)
    conn.close()


@raises(pyodbc.ProgrammingError)
def test_mars_autocommit_will_fail():
    conn = pyodbc.connect(get_connection_string(),
                          MARS_Connection='yes',
                          autocommit=True)
    conn.execute('BEGIN TRANSACTION')
    '''
    pyodbc.ProgrammingError: ('42000', '[42000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]A transaction that was started in a MARS batch is still active at the end of the batch. The transaction is rolled back. (3997) (SQLExecDirectW)')
    '''


def test_mars_autocommit_and_switching():
    conn = pyodbc.connect(get_connection_string(),
                          MARS_Connection='yes',
                          autocommit=True)
    conn.autocommit = False
    trancount, = conn.execute('SELECT @@TRANCOUNT').fetchone()
    eq_(trancount, 1)
    conn.commit()
    conn.autocommit = True
    trancount, = conn.execute('SELECT @@TRANCOUNT').fetchone()
    eq_(trancount, 0)
    conn.close()
