import psycopg2
from flask import flash


# POSTGRESQL CONNECTION
####################################################
def connect_postgresql(dbname, user, password, host, port, query):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

        cur = conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]  # Get column names
        query_result = cur.fetchall()

        cur.close()
        conn.close()

        return query_result, columns
    except psycopg2.Error as e:
        flash(f'Error executing query: {e}', 'danger')
        return None, None
