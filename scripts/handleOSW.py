import sqlite3
import pandas as pd


def connOSW(osw_file):
    """read sqlite db/osw file into conection object
    :param osw database
    :return database connection objeczt"""
    conn = sqlite3.connect(osw_file)
    return conn

def listOSWTables(conn):
    """
    :param database cnnection (use readOSW)
    :return list of table names as strings"""
    conn_cursor = conn.cursor()
    conn.text_factory = str
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=[name[0] for name in res]
    return tables

def listOSWColumns(conn, tables):
    """for given db connection and list of tables in that db,
    :return list of all unique column names, sorted"""
    names = []
    for t in tables:
        res = conn.execute("select * from " + t)
        for description in res.description:
            names.append(description[0])
    return sorted(list(set(names)))

def columnInOSW(osw_file, col):
    """
    @brief check if a column is in the database
    @params osw_file and column name as string
    :return boolean"""
    conn = connOSW(osw_file)
    tables = listOSWTables(conn)
    cols = listOSWColumns(conn, tables)
    return col in cols

def OSW2df(osw_file, table_name):
    """
    read a specified OSW table into dataframe
    :param osw_file, name of the tbale in the frame (needs to be known beforehand)
    :return:  dataframe
    """
    conn = connOSW(osw_file)
    df = pd.read_sql_query("SELECT * FROM " + table_name, conn)
    return df

