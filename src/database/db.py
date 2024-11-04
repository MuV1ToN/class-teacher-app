import sqlite3 as sq

class Database:
    # Singletone
    __instance = None
    def __new__(cls, *args, **kwgs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    # Конструктор
    def __init__(self):
        self.connection = sq.connect('Колледж.db')
        self.connection.execute('PRAGMA foreign_keys = ON;')
        self.cursor = self.connection.cursor()
      
    # Получить данные 
    def get_request_data(self, request: str) -> list:
        self.cursor.execute(request)
        data = self.cursor.fetchall()
        return data
    
    # Внести данные
    def insert_data(self, table: str, data: dict) -> None:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())

        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'

        self.cursor.execute(query, values)
        self.connection.commit()
        
    # Обновить данные
    def changing_data(self, table: str, data: dict, id: str) -> None:
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values())

        query = f'UPDATE {table} SET {set_clause} WHERE id = {id}'
        
        self.cursor.execute(query, values)
        self.connection.commit()
        self.cursor.close()
        
    # Удалить данные   
    def delete_data(self, name, id) -> None:
        self.cursor.execute(f"delete from %s where id = %s" % (name, id))
        self.connection.commit()
        
    # Деструктор
    def __del__(self):
        
        self.connection.close()

if __name__ == '__main__':
    ...  
    