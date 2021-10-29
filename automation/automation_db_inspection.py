import pyodbc
import pandas as pd
import re
from dataclasses import dataclass, field, asdict
from typing import List

@dataclass
class DetectedPayload:
    detected_type: str = ""
    detected_values: list[str] = field(default_factory=list)


@dataclass
class Column:
    column_name: str = ""
    detected_payloads: list[DetectedPayload] = field(default_factory=list)


@dataclass
class Table:
    table_name: str = ""
    columns: list[Column] = field(default_factory=list)


@dataclass
class Tables:
    tables: list[Table] = field(default_factory=list)


def get_cursor_and_connection():
    server = 'localhost'
    database = 'mytest'
    username = 'pyuser'
    password = 'Test1234%^&'

    mssql_conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=" + server + ";PORT=1433;DATABASE=" + database + "; UID=" + username + "; PWD=" + password)

    cursor = mssql_conn.cursor()
    
    return cursor, mssql_conn

cursor, mssql_conn = get_cursor_and_connection()

def get_table_names():
    tables = Tables()
    sql_get_tables = "SELECT name FROM sysobjects WHERE xtype='U'"
    cursor.execute(sql_get_tables)
    rows = cursor.fetchall()

    for row in rows:
        table = Table()
        table.table_name = row[0]
        tables.tables.append(table)

    return tables

def get_column_names(table):
    column_names = []
    sql_get_columns = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?"
    cursor.execute(sql_get_columns, table.table_name)
    rows=cursor.fetchall()

    for row in rows:
        column = Column()
        column.column_name = row[0]
        table.columns.append(column)
    
    return table

def make_column_query(columns):
    column_query = ''

    for column in columns:
        column_query = column_query + column.column_name + ','
    column_query = column_query[:-1]

    return column_query

def make_dataframe(table):
    column_query = make_column_query(table.columns)
    query1 = "SELECT top 10 " + column_query + " FROM " + table.table_name + "(nolock)"
    df = pd.read_sql(query1, mssql_conn)

    return df

def check_personal_pattern(data_cells, column):
    mobile_tel_pattern = "(01[016789][-~.\s]?[0-9]{3,4}[-~.\s]?[0-9]{4})"
    detected_payload = DetectedPayload()

    for data_cell in data_cells:
        data_cell = str(data_cell)
        match_mobile_tel = re.search(mobile_tel_pattern, data_cell)

        if match_mobile_tel:
            detected_payload.detected_values.append(match_mobile_tel.group(1))

    if len(detected_payload.detected_values) > 0:
        detected_payload.detected_type = "mobile"
        column.detected_payloads.append(detected_payload)

if __name__ == "__main__":
    tables = get_table_names()

    print("-"*30 + "Check Tables" + "-"*30)
    
    for table in tables.tables:
        print("[" + table.table_name + "]")
        table = get_column_names(table)
        my_dataframe = make_dataframe(table)
        
        for column in table.columns:
            data_cells = my_dataframe[column.column_name].tolist()
            check_personal_pattern(data_cells, column)
    
    print("-"*30 + "Result" + "-"*30)
    for table in tables.tables:
        for column in table.columns:
            if len(column.detected_payloads) > 0:
                for detected_payload in column.detected_payloads:
                    print("Table:Column - " + table.table_name + " : " + column.column_name)
                    print("Type:Reslut - "+ detected_payload.detected_type + " : " + str(detected_payload.detected_values))
