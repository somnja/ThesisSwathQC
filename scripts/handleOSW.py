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
    conn.close()
    return df


def irtDfFromSql(file):
    conn = connOSW(file)
    df = pd.read_sql_query("""SELECT FEATURE.NORM_RT as iRT, 
                                     FEATURE.PRECURSOR_ID as precursor, 
                                     PRECURSOR.LIBRARY_RT , 
                                     PRECURSOR.DECOY as decoy
                                     FROM PRECURSOR
                                     INNER JOIN FEATURE ON FEATURE.PRECURSOR_ID = PRECURSOR.ID """, conn)
    return df


def peptideScoreFromSql(file):
    conn = connOSW(file)
    df = pd.read_sql_query("""SELECT SCORE_PEPTIDE.PEPTIDE_ID as ID,
                            SCORE_PEPTIDE.SCORE as d_score,
                            SCORE_PEPTIDE.QVALUE,
                            SCORE_PEPTIDE.PVALUE,
                            SCORE_PEPTIDE.PEP,
                            SCORE_PEPTIDE.CONTEXT,
                            SCORE_PEPTIDE.RUN_ID,
                            PEPTIDE.ID as precursor, 
                            PEPTIDE.DECOY as decoy
                            FROM PEPTIDE
                            INNER JOIN SCORE_PEPTIDE ON SCORE_PEPTIDE.PEPTIDE_ID = PEPTIDE.ID """, conn)
    return df


def proteinScoreFromSql(file):
    conn = connOSW(file)
    df = pd.read_sql_query("""SELECT SCORE_PROTEIN.PROTEIN_ID,
                            SCORE_PROTEIN.SCORE as d_score,
                            SCORE_PROTEIN.QVALUE,
                            SCORE_PROTEIN.PVALUE,
                            SCORE_PROTEIN.PEP,
                            SCORE_PROTEIN.CONTEXT,
                            SCORE_PROTEIN.RUN_ID,
                            PROTEIN.ID, 
                            PROTEIN.DECOY as decoy
                            FROM PROTEIN
                            INNER JOIN SCORE_PROTEIN ON SCORE_PROTEIN.PROTEIN_ID = PROTEIN.ID  """, conn)
    return df


