from nose.tools import ok_, eq_, raises
import pyodbc

from utils import get_connection_string


def setup():
    conn = pyodbc.connect(get_connection_string())
    conn.execute('''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='x' AND xtype='U')
    CREATE TABLE x(a INT PRIMARY KEY)
    ''')
    conn.commit()
    conn.execute('''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='y' AND xtype='U')
    CREATE TABLE y(b INT PRIMARY KEY)
    ''')
    conn.close()


def test_x_exists():
    conn = pyodbc.connect(get_connection_string())
    conn.execute('SELECT * FROM x')
    ok_(True)
    conn.close()


@raises(pyodbc.ProgrammingError)
def test_y_does_not_exists():
    conn = pyodbc.connect(get_connection_string())
    conn.execute('SELECT * FROM y')
    ok_(True)
    conn.close()


def test_transaction_isolation_level_in_two_connections_default():
    conn_a = pyodbc.connect(get_connection_string())
    conn_b = pyodbc.connect(get_connection_string())
    conn_a.execute('INSERT INTO x(a) VALUES (1)')
    conn_a.commit()
    (result,), = conn_b.execute('SELECT * FROM x')
    eq_(result, 1)
    conn_a.execute('DELETE FROM x')
    conn_a.commit()
    conn_a.close()
    conn_b.close()


def test_transaction_isolation_level_snapshot_1():
    conn_a = pyodbc.connect(get_connection_string())

    # set conn_b to transaction isolation level snapshot
    conn_b = pyodbc.connect(get_connection_string())
    conn_b.autocommit = True
    conn_b.execute('SET TRANSACTION ISOLATION LEVEL SNAPSHOT')
    conn_b.autocommit = False

    # Once result is decided
    results = conn_b.execute('SELECT * FROM x')

    # Even if the content has changed
    eq_(tuple(results), ())
    conn_a.execute('INSERT INTO x(a) VALUES (1)')
    conn_a.commit()

    # then returns the old result set
    results = conn_b.execute('SELECT * FROM x')
    eq_(tuple(results), ())

    # teardown
    conn_a.execute('DELETE FROM x')
    conn_a.commit()
    conn_a.close()
    conn_b.close()


def test_transaction_isolation_level_snapshot_2():
    conn_a = pyodbc.connect(get_connection_string())

    # set conn_b to transaction isolation level snapshot
    conn_b = pyodbc.connect(get_connection_string())
    conn_b.autocommit = True
    conn_b.execute('SET TRANSACTION ISOLATION LEVEL SNAPSHOT')
    conn_b.autocommit = False

    # If the content has changed
    conn_a.execute('INSERT INTO x(a) VALUES (1)')
    conn_a.commit()

    # then returns the normal result set (if not be known old result)
    (result,) , = conn_b.execute('SELECT * FROM x')
    eq_(result, 1)

    # teardown
    conn_a.execute('DELETE FROM x')
    conn_a.commit()
    conn_a.close()
    conn_b.close()


def test_transaction_isolation_level_snapshot_3():
    conn_a = pyodbc.connect(get_connection_string())

    # set conn_b to transaction isolation level snapshot
    conn_b = pyodbc.connect(get_connection_string())
    conn_b.autocommit = True
    conn_b.execute('SET TRANSACTION ISOLATION LEVEL SNAPSHOT')

    # Once result is decided
    results = conn_b.execute('SELECT * FROM x')

    # Even if the content has changed
    eq_(tuple(results), ())
    conn_a.execute('INSERT INTO x(a) VALUES (1)')
    conn_a.commit()

    # then returns the old result set
    (result,) , = conn_b.execute('SELECT * FROM x')
    eq_(result, 1)

    # teardown
    conn_a.execute('DELETE FROM x')
    conn_a.commit()
    conn_a.close()
    conn_b.close()


def test_transaction_isolation_level_dirty_1():
    conn_a = pyodbc.connect(get_connection_string())

    # set conn_b to transaction isolation level snapshot
    conn_b = pyodbc.connect(get_connection_string())
    conn_b.autocommit = True
    conn_b.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED')
    conn_b.autocommit = False

    # Once result is decided
    results = conn_b.execute('SELECT * FROM x')

    # Even if the content has changed
    eq_(tuple(results), ())
    conn_a.execute('INSERT INTO x(a) VALUES (1)')
    conn_a.commit()

    # then returns the new result set
    (result,) , = conn_b.execute('SELECT * FROM x')
    eq_(result, 1)

    # teardown
    conn_a.execute('DELETE FROM x')
    conn_a.commit()
    conn_a.close()
    conn_b.close()


def test_transaction_isolation_level_dirty_2():
    conn_a = pyodbc.connect(get_connection_string())

    # set conn_b to transaction isolation level snapshot
    conn_b = pyodbc.connect(get_connection_string())
    conn_b.autocommit = True
    conn_b.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED')
    conn_b.autocommit = False

    # If the content has changed
    conn_a.execute('INSERT INTO x(a) VALUES (1)')
    conn_a.commit()

    # then returns the normal result set (if not be known old result)
    (result,) , = conn_b.execute('SELECT * FROM x')
    eq_(result, 1)

    # teardown
    conn_a.execute('DELETE FROM x')
    conn_a.commit()
    conn_a.close()
    conn_b.close()


def teardown():
    conn = pyodbc.connect(get_connection_string())
    conn.execute('DROP TABLE x')
    conn.commit()
    conn.close()
