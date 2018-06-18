import copy


DEFAULT_DRIVER = 'ODBC Driver 17 for SQL Server'
DEFAULT_HOST = 'sqlserver'
DEFAULT_USERNAME = 'sa'
DEFAULT_PASSWORD = 'passWORD1234'


def escape(text):
    # TODO: not sufficient
    return f'{{{text}}}'


def get_connection_string(**kwargs):
    d = {
        'DRIVER': DEFAULT_DRIVER,
        'SERVER': DEFAULT_HOST,
        'UID': DEFAULT_USERNAME,
        'PWD': DEFAULT_PASSWORD,
    }
    d.update(kwargs)
    return dict_to_connection_string(d)


def dict_to_connection_string(options):
    copied = copy.deepcopy(options)
    return ';'.join(f'{k}={escape(v)}' for k, v in copied.items())
