"""Module for some common utility functions."""

import csv
import os
import psycopg2

from .config import DATA_DIR, UPDATE_STMT, INSERT_STMT

USER_DATA_MAP = {}


def process_csv(csv_file=None):
    """
    Function to read the content(s) of CSV file(s).

    The function reads the contents of CSV file(s) available in a
    certain directory and populate a dictionary with e-mail id as key
    in order to have unique e-mails.

    :param csv_file: Name of the csv_file.
    :return: dictionary containing the data from CSV.
    """
    if csv_file:
        _process_csv_data(csv_file, USER_DATA_MAP)
    else:
        csv_files_list = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        for fl in csv_files_list:
            _process_csv_data(fl, USER_DATA_MAP)
    return USER_DATA_MAP


def _process_csv_data(csv_file, user_data_map):
    """
    Private function to read the content(s) of CSV file(s).

    :param csv_file: Name of the csv_file
    :return: None
    """
    with open(csv_file, 'r') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if len(row) < 2:
                print('The CSV file is not in expected format.')
                raise Exception
            user_data_map[row[1].lower()] = row[0]


def connect_to_db():
    """
    Function to connect to the database.

    Connects to the 'Postgres' database running the docker container.

    :param: None
    :return: Database connection object.
    """
    try:
        conn = psycopg2.connect(database='postgres',
                                user='postgres',
                                password='docker',
                                host='localhost',
                                port='5432')
        print('Opened database successfully')
        return conn
    except Exception as e:
        print(str(e))
        raise e


def disconnect_from_db(conn):
    """
    Function to disconnect from the database.

    :param: Database connection object.
    :return: None
    """
    if conn:
        try:
            conn.close()
        except Exception as e:
            print(str(e))
            raise e


def add_to_db(name, email_id):
    """
    Function to add/update user data to the database.

    The function tries to use a generic 'upsert' by first trying
    to 'update' the record followed by insert if 'update' does not
    update any matching rows.

    :param name: User name.
    :param email_id: User email_id.
    :return: None
    """
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # This is the best way that I found to do an 'upsert' in a database agnostic way.
        # Try to update the data first, and if no records get updated, insert them.
        cur.execute(UPDATE_STMT.format(nm=name, em=email_id))
        if cur.rowcount == 0:
            cur.execute(INSERT_STMT.format(nm=name, em=email_id))
        conn.commit()
        print('Successfully added/updated record!')
    except Exception as e:
        print(str(e))
        disconnect_from_db(conn)
        raise e
    finally:
        disconnect_from_db(conn)
