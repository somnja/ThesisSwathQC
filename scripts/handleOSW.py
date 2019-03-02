'''reading sqlite based data fromats,
including
    - .osw
    - .pqp
'''

import sqlite3
import pandas as pd


def connOSW(osw_file):
    """connect to sqlite based database, e.g osw or pqp
    :param osw database
    :return database connection objeczt"""
    conn = sqlite3.connect(osw_file)
    return conn

def listOSWTables(conn):
    """list all available tables in database
    :param database connection (use readOSW)
    :return list of table names as strings"""
    conn_cursor = conn.cursor()
    conn.text_factory = str
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=[name[0] for name in res]
    return tables

def listOSWColumns(conn, tables):
    """
    :param conn: databse connection
    :param tables: list of tables in database
    :return:
    """
    names = []
    for t in tables:
        res = conn.execute("select * from " + t)
        for description in res.description:
            names.append(description[0])
    return sorted(list(set(names)))

def columnInOSW(osw_file, col):
    """
    check if a column is present in any table of the dataframe
    :param osw_file:
    :param col:
    :return:
    """
    conn = connOSW(osw_file)
    tables = listOSWTables(conn)
    cols = listOSWColumns(conn, tables)
    return col in cols

def OSW2df(osw_file, table_name):
    """
    read a table into pandas dataframe
    :param osw_file:
    :param table_name:
    :return:
    """
    conn = connOSW(osw_file)
    df = pd.read_sql_query("SELECT * FROM " + table_name, conn)
    return df

