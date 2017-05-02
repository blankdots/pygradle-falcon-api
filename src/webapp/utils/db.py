import sqlite3
from webapp.utils.logs import app_logger


def connect_DB(db_file=None):
    """Connect to DB by parsing configuration."""
    db_filename = ''
    if db_file is None:
        db_filename = 'data.db'
    else:
        db_filename = db_file
    try:
        conn = sqlite3.connect(db_filename)
        app_logger.info('Connecting to database.')
        tb_indexes_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='indexes'"
        if not conn.execute(tb_indexes_exists).fetchone():
            create_table(conn, """create table if not exists indexes (indexstatus text, data text, author text, timestamp datetime)""")
        return conn
    except Exception as error:
        app_logger.error('Connection Failed!\
            \nError Code is {0};\
            \nError Content is {1};'.format(error.args[0], error.args[1]))
        return error


def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement.

    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        db_cursor = conn.cursor()
        db_cursor.execute(create_table_sql)
        app_logger.info('Creating tables in the database if they do not exist.')
    except Exception as error:
        app_logger.error('Error {0}'.format(error))
        return error
