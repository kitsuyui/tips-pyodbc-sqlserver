from nose.tools import ok_, eq_
import pyodbc

from utils import get_connection_string


def test_example():
    eq_(1, 1)
    ok_(True)


def test_import_pyodbc():
    pyodbc


def test_get_connection_string():
    eq_(type(get_connection_string()), str)
