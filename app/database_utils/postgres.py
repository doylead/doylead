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
    from app.aws_utils.aurora import (AWS_RDS_ENDPOINT as HOST,
                                      POSTGRES_DB as DATABASE,
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

def _execute(sql_query: str,
             data: tuple = (),
             db_name = DATABASE,
             return_col_names = False):
    """Allows running a SQL query, allows for DRY principle in code"""

    # It is the responsibility of the caller of this method to properly
    # format a SQL query (using psycopg2 methods to prevent against SQL
    # injection), with the exception of including optional data

    # TODO There may be better/more efficient ways to handle inserting
    # multiple rows at once

    query_results = None

    # Connect to database
    conn = _db_connect(db_name)

    # Necessary for some operations (e.g. database creation)
    conn.autocommit = True

    # Find the words in the SQL query
    tokens = sql_query.as_string(conn).lower().split(" ")

    # Some types of query are uniquely specified by the first word,
    # e.g. "SELECT"
    mode = tokens[0]

    # Some types of query require two words, e.g. "CREATE DATABASE"
    # List may need to be expanded
    if tokens[1] in ["create", "alter"]:
        mode += tokens[1]

    try:
        with conn.cursor() as cur:
            if data:
                cur.execute(sql_query, data)
            else:
                cur.execute(sql_query)

            if mode.lower() == "select":
                query_results = cur.fetchall()
                col_names = [desc[0] for desc in cur.description]
    finally:
        # Close connection to database
        conn.close()

    # Using a dictionary with variable keys allows client consistency
    all_results = {"results": query_results}
    if mode.lower() == "select" and return_col_names:
        all_results["col_names"] = col_names

    return all_results

def _get_current_time():
    """Get current time from Aurora PostgreSQL.
    May be a useful diagnostic"""
    sql_query = sql.SQL("SElECT now()")
    query_results = _execute(sql_query)

    return query_results

def _list_databases():
    """Provides an API for listing all databases on the Aurora instance.
    May be used as a diagnostic"""
    # Structured in an admittedly strange way to demonstrate function of _execute()
    sql_query = sql.SQL("""SELECT d.datname as "Name"
                FROM "pg_catalog"."pg_database" d
                ORDER BY 1""")

    return _execute(sql_query, return_col_names = True)

def _add_database(db_name: str):
    """Provides an API for creating a database on the Aurora instance.
    Unlikely to be called often"""

    sql_query = sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(db_name)
    )
    _execute(sql_query)

    return _list_databases()

def _delete_database(db_name: str):
    """Provides an API for dropping a database on the Aurora instance.
    Unlikely to be called often"""

    sql_query = sql.SQL("DROP DATABASE {}").format(
        sql.Identifier(db_name)
    )
    _execute(sql_query)

    return _list_databases()

def _list_tables():
    """Provides an API to list tables"""
    sql_query = sql.SQL("""SELECT table_schema, table_name FROM information_schema.tables
                WHERE table_schema not in ('information_schema', 'pg_catalog')
                AND table_type = 'BASE TABLE'""")

    return _execute(sql_query, return_col_names = True)

def _add_table(table_name: str, columns: list[tuple[str, str]], db_name: str = DATABASE):
    """Provides an API to add a table to a database"""

    # Columns should be provided as a dictionary with keys representing column names,
    # and associated values representing data types. Full list of supported data types:
    # https://www.postgresql.org/docs/current/datatype.html
    # e.g.
    # _add_table("user", [("name", "text"), ("active", "boolean"), ("age", "integer")])

    # All tables will have an "id" column containing their primary key
    fields = [
        sql.SQL("{} {}").format(
            sql.Identifier("id"),
            sql.SQL("serial PRIMARY KEY")
        )
    ]

    # Add user-specified columns
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

    _execute(sql_query, db_name = db_name)

    return _list_tables()

def _delete_table(table_name: str, db_name: str = DATABASE):
    """Provids an API for deleting tables"""

    sql_query = sql.SQL("DROP TABLE {}").format(
        sql.Identifier(table_name)
    )

    _execute(sql_query, db_name = db_name)
    return _list_tables()

def insert_into_table(table_name: str,
                      data: dict,
                      db_name: str = DATABASE):
    """Provides an API to insert a single row into a table"""

    # Data should be provided in the form of a dictionary whose keys
    # are columnn names and coresponding values are to be insertd into
    # those columns

    # Pull keys first to ensure consistent ordering
    keys = list(data.keys())

    # Generate a comma-separated list of column names
    col_names = []
    for key in keys:
        col_names.append(
            sql.Identifier(key)
        )

    # Generate a comma-separated list of the string "%s"
    # repeated n times, where n is the number of columns
    # specified
    placeholders = sql.SQL(",").join(
        len(keys) * [sql.SQL("%s")]
    )

    sql_query = sql.SQL("""INSERT INTO {}
                        ({})
                        VALUES ({})""").format(
        sql.Identifier(table_name),
        sql.SQL(",").join(col_names),
        placeholders
    )

    # Extract the data
    sql_data = [data[i] for i in keys]

    _execute(sql_query, db_name = db_name, data = sql_data)

    return None # Is there a better way to provide information, e.g. diagnostics?

def select_rows(table_name: str,
                    column_names: tuple = (),
                    max_row_count: int = -1,
                    return_column_names: bool = False,
                    db_name: str = DATABASE):
    """Provides an API for selecting data from a table"""


    # If no column names are provided, return all columns
    if not column_names:
        columns = sql.SQL("*")
    else:
        columns = sql.SQL(",").join(
            [sql.Identifier(x) for x in column_names]
        )

    sql_query = sql.SQL("SELECT {} FROM {}").format(
        columns,
        sql.Identifier(table_name)
    )

    # TODO - Add filtering / WHERE clause
    # TODO - Add sorting / ORDER BY clause
    # As a general matter I'd only currently imagine asking the database
    # to sort if we are also applying some limitation.  E.g. asking for the
    # n most recent posts

    # Apply limit to max row count, if appropriate
    if max_row_count > 0 and isinstance(max_row_count, int):
        sql_query = sql.SQL(" ").join([
            sql_query,
            sql.SQL("LIMIT {}").format(
                sql.SQL(str(max_row_count))
            )
        ])

    query_results = _execute(sql_query,
                             db_name = db_name,
                             return_col_names = return_column_names)

    return query_results
