from tkinter import Tk, ttk
from src.database.db import Database
from src.windows.function import FunctionWindows

class ManagementWindow(Tk):
    def __init__(self):
        super().__init__()
        
        # Настройки окна
        self.title('Тестовое окно')
        self.width = 400
        self.height = 400
        self.minsize(self.width, self.height)
        self.x = int(self.winfo_screenwidth()/2 - self.width/2)
        self.y = int(self.winfo_screenheight()/2 - self.height/2)
        self.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        
        # Разметка 
        notebook = ttk.Notebook(self)
        notebook.pack(expand=1, fill="both")
        
        # Получаеи названия таблицы отсартированных по алфавиту
        tab_titles = [title[0] for title in Database().get_request_data(
            """ SELECT name FROM sqlite_master WHERE type='table' ORDER BY name """
            )[1::]]

        # Переменная для хранения tree
        self.trees = {}

        for tab_name in tab_titles:
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=tab_name) #f'{tab_name: ^20s}'
            tree = ttk.Treeview(tab, show="headings")
            tree.pack(expand=1, fill='both')
            
            self.trees[tab_name] = tree
            
            tree['columns'], data = self.get_data(tab_name)
            [tree.heading(column, text=column) for column in tree['columns']]
            [tree.insert("", "end", values=row) for row in data]
            btns = [
                ttk.Button(tab, text='Добавить', 
                           command=lambda name=tab_name: self.add_data(notebook, name, self.trees[name])),
                ttk.Button(tab, text='Изменить', 
                           command=lambda name=tab_name: self.changing_data(name, self.trees[name])),
                ttk.Button(tab, text='Удалить', 
                           command=lambda name=tab_name: self.delete_data(name, self.trees[name])),
            ]
            [btn.pack(side='left') for btn in btns]
            
        self.mainloop()
        
            
    # Функции
    # Добавления данных
    def add_data(self, notebook, tab_name, tree):
        current_tab_index = notebook.select()
        current_tab_name = notebook.tab(current_tab_index, "text")
        current_tab = current_tab_name
        FunctionWindows().add(current_tab)
        self.update_data(tab_name, tree)
    
    # Изменение данных
    def changing_data(self, tab_name, tree):
        current_item = tree.focus()
        if current_item != "":
            data = tree.item(current_item)['values']
            FunctionWindows().changing(tab_name, data)
            self.update_data(tab_name, tree)
    
    # Удаление выбраной строки
    def delete_data(self, name, tree):
        current_item = tree.focus()
        id = tree.item(current_item)['values'][0]
        print(f"delete from %s where id = %s" % (name, id))
        Database().delete_data(name, id)
        self.update_data(name, tree)
        
    # Обновление таблицы
    def update_data(self, tab_name, tree):
        for item in tree.get_children():
            tree.delete(item)

        tree['columns'], data = self.get_data(tab_name)
        [tree.heading(column, text=column) for column in tree['columns']]
        [tree.insert("", "end", values=row) for row in data]
    
    # Получение данных из БД
    def get_data(self, table):
        # Аккаунт
        if table == 'Аккаунт':
            titels = Database().get_request_data("select name from pragma_table_info('Аккаунт')")
            data = Database().get_request_data("""
                                               
                                                select 
                                                Аккаунт.id, логин, пароль, concat(фамилия,' ',имя,' ',отчество) 
                                                as преподователь from Аккаунт 
                                                inner join Преподаватель 
                                                on Аккаунт.преподаватель = Преподаватель.id
                                                
                                               """)
            return titels, data
        
        # Группа
        elif table == 'Группа':
            titels = Database().get_request_data("select name from pragma_table_info('Группа')")
            data = Database().get_request_data("select * from Группа")
            return titels, data
        
        # Предмет
        elif table == 'Предмет':
            titels = Database().get_request_data("select name from pragma_table_info('Предмет')")
            data = Database().get_request_data("select * from Предмет")
            return titels, data
        
        # Преподаватель  
        elif table == 'Преподаватель':
            titels = Database().get_request_data("select name from pragma_table_info('Преподаватель')")
            data = Database().get_request_data("""
                                               
                                                select Преподаватель.id, фамилия, имя, отчество, 
                                                Предмет.предмет as предмет,
                                                concat(курс,'-',Группа.группа, substring(направление, 1, 1), класс) as группа
                                                from Преподаватель 
                                                left join Предмет on Преподаватель.предмет = Предмет.id
                                                left join Группа on Преподаватель.группа = Группа.id
    
                                               """)
            return titels, data
        
        # Студент
        elif table == 'Студент':
            titels = Database().get_request_data("select name from pragma_table_info('Студент')")
            data = Database().get_request_data("""
                                               
                                                select Студент.id, фамилия, имя, отчество, 
                                                concat(курс,'-',Группа.группа, substring(направление, 1, 1), класс) as группа 
                                                from Студент 
                                                inner join Группа on Студент.группа = Группа.id 
                                                
                                               """)
            return titels, data

        # Успеваемость
        elif table == 'Успеваемость':
            titels = Database().get_request_data("select name from pragma_table_info('Успеваемость')")
            data = Database().get_request_data("""
                                               
                                                SELECT Успеваемость.id,
                                                concat(Студент.фамилия,' ', Студент.имя,' ',Студент.отчество) as студент,
                                                Предмет.предмет, оценка
                                                FROM Успеваемость
                                                INNER JOIN Студент ON Успеваемость.студент = Студент.id
                                                INNER JOIN Предмет ON Успеваемость.предмет = Предмет.id
                                                
                                               """)
            return titels, data
        
        # Если нет запроса
        else:
            return [], []