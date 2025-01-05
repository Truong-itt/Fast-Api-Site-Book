import os, sys, json
import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from passlib.context import CryptContext

from time import time
from glob import glob


POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5435
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "admin12345"
POSTGRES_DB = "postgres"

class Postgres():
    def __init__(self):
        self.host = POSTGRES_HOST
        self.user = POSTGRES_USER
        self.port = POSTGRES_PORT
        self.password = POSTGRES_PASSWORD
        self.database = POSTGRES_DB
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            port=self.port,
            password=self.password
        )
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.cursor.close()
        self.conn.close()

    def query(self, sql_query, fetch=True):
        try:
            self.cursor.execute(sql_query)
            self.conn.commit()
            if fetch:
                rows = self.cursor.fetchall()
                df = pd.DataFrame(rows, columns=[desc[0] for desc in self.cursor.description])
                return df
            return self.cursor.fetchall()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
          
    def create_schema(self, sql_path='*.sql'):
        with open(sql_path, 'r') as f:
            schema = f.read().split('\n\n')
        try:
            for statement in schema:
                self.cursor.execute(statement)
                if statement.find('CREATE TABLE') != -1:
                    print(f'''📢 Created table {statement.split('"')[1]}''')
                if statement.find('ALTER TABLE') != -1:
                    alter = statement.split('"')
                    print(f'''🔌 Linked table {alter[1]} -> {alter[5]}''')
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
    
    def get_columns(self, table_name):
        try:
            self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}'".format(table_name=table_name))
            cols = [i[0] for i in self.cursor.fetchall()]
            return cols
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
    
    def get_all_table(self,):
        try:
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = [i[0] for i in self.cursor.fetchall()]
            return tables
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
    
    def delete_table(self, table_names = []):
        for table in table_names:
            try:
                self.cursor.execute(f"DROP TABLE {table}")
                print(f"🗑 Deleted {table}")
            except Exception as e:
                self.cursor.execute("ROLLBACK")
                print(f'❌ ROLLBACK: {e}')
        self.conn.commit()
    
    def upsert(self, df, table_name, ids = [], updates:list=None):
        conflict_target='id'
        cols = list(df.columns)
        check_ids = []
        data = [tuple(i) for i in np.where(pd.isna(df), None, df).tolist()][0]
        update_cols = [c for c in cols if c != conflict_target]
        s_time = time()
        check_ids = [data[cols.index(id)].replace("'", "''") for id in ids]
        try:
            self.cursor.execute(f"SELECT {conflict_target} FROM {table_name} WHERE {' AND '.join([f'''{id} = '{c_id}'; ''' for id, c_id  in zip(ids, check_ids)])}")
            result = self.cursor.fetchone()
            if result:
                _id = result[0]
                sql_insert = f"""
                    INSERT INTO {table_name} ({','.join(cols)})
                    VALUES ({','.join(['%s']*len(cols))})
                    ON CONFLICT ({conflict_target})
                    DO UPDATE SET {updates};
                """
                if updates is None:
                    updates = ','.join([f"{c}={'EXCLUDED.'+c}" for c in update_cols])
                data = (_id,) + data
            else:
                sql_insert = f"""
                    INSERT INTO {table_name} ({','.join(cols)})
                    VALUES ({','.join(['%s']*len(cols))});
                """
                self.cursor.execute(sql_insert, data)
            self.conn.commit()
            print('\r', f"🟢 Inserted: {_id} - Time: {time()-s_time:.2f} seconds", end='')
            sys.stdout.flush()
        except Exception as e:
            print('\r', f"❌ Error index {_id}: {e} - Time: {time()-s_time:.2f} seconds", end='')
            sys.stdout.flush()
        print()
    
    def upserts(self, df, table_name, ids = [], updates:list=None):
        conflict_target='id'
        cols = list(df.columns)
        check_ids = []
        datas = [tuple(i) for i in np.where(pd.isna(df), None, df).tolist()]
        update_cols = [c for c in cols if c != conflict_target]
        s_time = time()
        for idx, data in enumerate(datas):
            check_ids = [data[cols.index(id)].replace("'", "''") for id in ids]
            try:
                self.cursor.execute(f"SELECT {conflict_target} FROM {table_name} WHERE {' AND '.join([f'''{id} = '{c_id}'; ''' for id, c_id  in zip(ids, check_ids)])}")
                result = self.cursor.fetchone()
                if result:
                    _id = result[0]
                    sql_insert = f"""
                        INSERT INTO {table_name} ({','.join(cols)})
                        VALUES ({','.join(['%s']*len(cols))})
                        ON CONFLICT ({conflict_target})
                        DO UPDATE SET {updates};
                    """
                    if updates is None:
                        updates = ','.join([f"{c}={'EXCLUDED.'+c}" for c in update_cols])
                    data = (_id,) + data
                else:
                    sql_insert = f"""
                        INSERT INTO {table_name} ({','.join(cols)})
                        VALUES ({','.join(['%s']*len(cols))});
                    """
                    self.cursor.execute(sql_insert, data)
                self.conn.commit()
                print('\r', f"🟢 Inserted: {idx} - Time: {time()-s_time:.2f} seconds", end='')
                sys.stdout.flush()
            except Exception as e:
                print('\r', f"❌ Error index {idx}: {e} - Time: {time()-s_time:.2f} seconds", end='')
                sys.stdout.flush()
        print()
    
    def delete(self, table_name, pk_id):
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id={pk_id};")
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
    
    def truncate(self, table_name):
        try:
            self.cursor.execute(f"TRUNCATE {table_name} CASCADE")
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")

def load_json(folder='./demo/data_web/'):
    files = glob(f'{folder}*.json') + glob(f'{folder}*.jsonl')
    data = []
    for file in files:
        with open(file , 'r') as f:
            if file.endswith('.json'):
                data.extend(json.load(f))
            elif file.endswith('.jsonl'):
                for line in f:
                    try:
                        data.append(json.loads(line))
                    except:
                        pass
    return data

def count_react(data):
    clike = 0
    dlike = 0
    for k in ['like', 'love', 'haha', 'wow', 'sad']:
        clike += data[k] if data[k] is not None else 0
    for k in ['angry', 'other']:
        dlike += data[k] if data[k] is not None else 0
    return {'like': clike, 'dislike': dlike}


def get_db():
    db = Postgres()
    return db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)