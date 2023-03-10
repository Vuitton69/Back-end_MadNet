import sqlite3


class DB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('D:\\Back-end_MadNet\\bd.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def read(self, table, column):
        self.cursor.execute(f"SELECT {column} FROM {table}")
        return self.cursor.fetchall()

    def write(self, table, column, values):
        self.cursor.execute(f"INSERT INTO {table} ({column}) VALUES ({values})")
        return self.conn.commit()

    def update(self, table, values, arg):
        self.cursor.execute(f"UPDATE {table} SET {values} WHERE {arg}")
        return self.conn.commit()
    
    def delete(self, table, column, values):
        self.cursor.execute(f"DELETE FROM {table}  WHERE {column} = '{values}'")
        return True

    def close(self):
        self.conn.close()