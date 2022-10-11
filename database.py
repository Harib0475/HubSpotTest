import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()


class Database:
    def __init__(self):
        """
        Establish a connection with db
        if some error occurs then Retry  after 5 sec for 3 times.
        """
        result = urlparse(os.getenv('DB_URL'))
        self.db_user = result.username
        self.db_pass = result.password
        self.db_name = result.path[1:]
        self.db_host = result.hostname
        self.db_port = result.port
        self.connection = None

    def connect_db(self):
        """
            Establish a connection with db
        """
        try:
            self.connection = psycopg2.connect(database=self.db_name,
                                               host=self.db_host,
                                               user=self.db_user,
                                               password=self.db_pass,
                                               port=self.db_port)
            cursor = self.connection.cursor()
            cursor.close()
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f'connection error {error}')

    def close_connection(self):
        """
            Closing a connection
        """

        if self.connection is not None:
            self.connection.close()

    def execute_query(self, query, fetch=False):
        """
            Execute all queries
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            if fetch:
                return cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into table", error)

    def create_table(self, table_name):
        """
            Create a table if not exists in database
        """

        query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                email VARCHAR NOT NULL UNIQUE,
                hubspot_id VARCHAR,
                created_at timestamp default current_timestamp
            )"""
        self.execute_query(query)

    def add_record(self, table_name, data):
        """
            Add a record in database
        """

        query = f"""INSERT INTO {table_name} (first_name,last_name,email) VALUES ('{data['first_name']}',
             '{data['last_name']}', '{data['email']}')
            """
        self.execute_query(query)

    def update_record(self, table_name, data):
        """
            Update a record using email
        """

        query = f"""UPDATE {table_name}
            SET hubspot_id = '{data['vid']}'
            WHERE email = '{data['email']}';"""
        self.execute_query(query)

    def get_last_two_records(self, table_name):
        """
            Get last 2 records from database
        """

        query = f"""SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT 2"""
        records = self.execute_query(query, True)
        return records
