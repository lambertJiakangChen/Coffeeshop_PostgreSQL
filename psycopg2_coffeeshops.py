import psycopg2
import configparser
import pandas as pd
from sql_queries import *

def create_database():

    config = configparser.ConfigParser()
    config.read('private.cfg')
    DB_NAME_DEFAULT = config.get('SQL', 'DB_NAME_DEFAULT')
    DB_USER = config.get('SQL', 'DB_USER')
    DB_PASSWORD = config.get('SQL', 'DB_PASSWORD')
    
    conn = psycopg2.connect("host=127.0.0.1 dbname={} user={} password={}".format(DB_NAME_DEFAULT, DB_USER, DB_PASSWORD))
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    cur.execute('DROP DATABASE IF EXISTS coffeeshops')
    cur.execute("CREATE DATABASE coffeeshops WITH ENCODING 'utf8' TEMPLATE template0")
    
    conn.close()
    
    conn = psycopg2.connect('host=127.0.0.1 dbname=coffeeshops user={} password={}'.format(DB_USER, DB_PASSWORD))
    cur = conn.cursor()
    
    return cur, conn


def drop_table(cur, conn):

    cur.execute(drop_employees_table)
    conn.commit()

def date_format(cur, conn):

    cur.execute(modify_date_format)
    conn.commit()

def create_table(cur, conn):

    cur.execute(create_employees_table)
    conn.commit()

def insert_table(cur, conn):
    df = pd.read_csv('coffeeshop.csv', converters={'employee_id': str})
    for i, row in df.iterrows():
        cur.execute(insert_employees_table, row.tolist())
        conn.commit()

def main():

    cur, conn = create_database()

    drop_table(cur, conn)
    date_format(cur, conn)
    create_table(cur, conn)
    insert_table(cur, conn)

    conn.close()
    
if __name__ == '__main__':

    main()