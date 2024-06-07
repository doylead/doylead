"""Provides a higher-level API to a Postgres resource"""

import psycopg2
from psycopg2 import sql

import sys
from os import path
sys.path.append(
    path.join(path.dirname(__file__), '../..')
)

# Determine where the data source is defined
DATABASE_LOC = "docker"

# If running postgres on Aurora
if DATABASE_LOC == "Aurora":
    from app.config import AWS_RDS_ENDPOINT as HOST
    from app.aws_utils.aurora import (POSTGRES_DB as DATABASE,
                                      POSTGRES_USER as USER,
                                      POSTGRES_PASSWORD as PASSWORD)

# If running postgres in Docker/locally
if DATABASE_LOC == "docker":
    from app.docker_utils.docker_postgres import (POSTGRES_HOST as HOST,
                                                  POSTGRES_DB as DATABASE,
                                                  POSTGRES_USER as USER,
                                                  POSTGRES_PASSWORD as PASSWORD)
                                              
def _db_connect(database = DATABASE):
    """Connects to Aurora Postgres instance"""
    # Attempt to connect to the database.  If operations fail,
    # print error
    try:
        conn = psycopg2.connect(database = database,
                                host = HOST,
                                user = USER,
                                password = PASSWORD,
                                port = "5432",
                                sslrootcert = "SSLCERTIFICATE")

    except Exception as e:
        print(f"Database connection failed due to {e}")

    return conn

def _execute(sql_query: str, placeholders: tuple[str] = None, data = None, db_name = DATABASE):
    """Allows running a SQL query, allows for DRY principle in code"""

    # Takes as input a static, numbered, or auto-numbered SQL query to be run
    # e.g.
    # select * from table where foo > 0, placeholders not passed
    # select * from {} where foo > 0, placeholders = ("table", )
    # select * from {} where {} > 0, placeholders = ("table", "foo")

    # Determine what type of query we're running
    tokens = sql_query.lower().split(' ')

    # Some modes can be described by one term, e.g. "select" or "update"
    mode = tokens[0]

    # Other queries should include two terms, e.g. "create database" 
    if tokens[0] in ("create", "drop"):
        mode += " " + tokens[1]

    # Santize sql query
    formatted_query = sql.SQL(sql_query)

    if placeholders:
        placeholders = [sql.Identifier(x) for x in placeholders]
        formatted_query = formatted_query.format(*placeholders)

    query_results = None

    # Execute query
    conn = _db_connect(db_name)

    # Necessary for some operations (e.g. database creation)
    conn.autocommit = True

    if not data:
        try:
            with conn.cursor() as cur:
                cur.execute(formatted_query)
                if mode == "select":
                    query_results = cur.fetchall()
                    print([desc[0] for desc in cur.description])
        finally:
            # Close connection to database
            conn.close()
    if data:
        # TODO
        pass

    return query_results

def _get_current_time():
    """Get current time from Aurora PostgreSQL.
    May be a useful diagnostic"""
    sql_query = "SElECT now()"
    query_results = _execute(sql_query)

    return query_results

def _list_databases():
    """Provides an API for listing all databases on the Aurora instance.
    May be used as a diagnostic"""
    # Structured in an admittedly strange way to demonstrate function of _execute()
    sql_query = """SELECT d.datname as "Name"
                FROM {}.{} d
                ORDER BY 1"""

    placeholders = ("pg_catalog", "pg_database")

    return _execute(sql_query, placeholders = placeholders)

def _add_database(db_name: str):
    """Provides an API for creating a database on the Aurora instance.
    Unlikely to be called often"""

    sql_query = "CREATE DATABASE {}"
    placeholders = (db_name,)
    _execute(sql_query, placeholders = placeholders)

    return _list_databases()

def _delete_database(db_name: str):
    """Provides an API for dropping a database on the Aurora instance.
    Unlikely to be called often"""

    sql_query = "DROP DATABASE {}"
    placeholders = (db_name,)
    _execute(sql_query, placeholders = placeholders)

    return _list_databases()

def _list_tables():
    """Provides an API to list tables"""
    sql_query = """SELECT table_schema, table_name FROM information_schema.tables
                WHERE table_schema not in ('information_schema', 'pg_catalog')
                AND table_type = 'BASE TABLE'"""

    return _execute(sql_query)

def _create_table(table_name: str, columns: list[tuple[str, str]], db_name: str = "doylead"):
    """Provides an API to add a table to a database"""

    # Columns should be provided as a dictionary with keys representing column names,
    # and associated values representing data types. Full list of supported data types:
    # https://www.postgresql.org/docs/current/datatype.html
    # e.g.
    # _create_table("user", [("name", "text"), ("active", "boolean"), ("age", "integer")])

    fields = []
    for col in columns:
        fields.append( 
            sql.SQL("{} {}").format(
                sql.Identifier( col[0] ),
                sql.SQL( col[1] )
            )
        )

    sql_query = sql.SQL("CREATE TABLE {} ({})").format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(fields)
    )

    conn = _db_connect(db_name)
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            cur.execute(sql_query)
    finally:
        conn.close()

    return _list_tables()
