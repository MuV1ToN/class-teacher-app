from tkinter import Toplevel, ttk, messagebox, Tk
from src.database.db import Database

class FunctionWindows(Tk):
    def __init__(self):
        super().__init__()
     
    # Добавление в БД   
    def add(self, title):
        self.title(f'{title}')
        self.width = 300
        self.height = 300
        self.minsize(self.width, self.height)
        self.x = int(self.winfo_screenwidth()/2 - self.width/2)
        self.y = int(self.winfo_screenheight()/2 - self.height/2)
        self.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        
        titles = [title[0] for title in Database().get_request_data(
            f"select name from pragma_table_info('%s')" % title
            )]
        
        fields = []
        data = {}
        for field in titles[1::]:
            ttk.Label(self, text=field).pack(fill='x', padx=(20))
            entry = ttk.Entry(self)
            entry.pack(fill='x', padx=(20))
            fields.append((field, entry))
        
        def save_to_db():
            for field, entry in fields:
                if entry.get() != '':
                    data[field] = entry.get()
                    
            try:
                Database().insert_data(title, data)
                self.destroy()
                self.quit()
                
            except:
                self.destroy()
                self.quit()
        
        ttk.Button(self, text='Сохранить', command=save_to_db).pack(pady=(20))
        
        self.mainloop()
        
        
    def changing(self, title, data):
        self.title(f'{title}')
        self.width = 300
        self.height = 300
        self.minsize(self.width, self.height)
        self.x = int(self.winfo_screenwidth()/2 - self.width/2)
        self.y = int(self.winfo_screenheight()/2 - self.height/2)
        self.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        
        titles = [title[0] for title in Database().get_request_data(
            f"select name from pragma_table_info('%s')" % title
            )]
        
        fields = dict(zip(titles, data))
        widgets = []
        id = fields['id']
        
        for field in titles[1::]:
            ttk.Label(self, text=field).pack(fill='x', padx=(20))
            entry = ttk.Entry(self)
            entry.insert(0, fields[field])
            entry.pack(fill='x', padx=(20))
            widgets.append((field, entry))
        
        def save_to_db():
            for field, entry in widgets:
                if entry.get() == '':
                    fields.pop(field)
                fields[field] = entry.get()
            fields.pop('id')
            try:
                Database().changing_data(title, fields, id)
                self.destroy()
                self.quit()
            except:
                self.destroy()
                self.quit()
                messagebox.showerror(title="Ошибка изменения", message='Проверте коректонось введеных данных и повторите снова!')
            
            
        ttk.Button(self, text='Сохранить', command=save_to_db).pack(pady=(20))
        
        self.mainloop()

        