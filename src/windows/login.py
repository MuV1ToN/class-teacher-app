from tkinter import Tk, ttk, IntVar, messagebox
from src.windows.management import ManagementWindow
from src.windows.classrom_teacher import ClassromTeahcerWindow
from src.database.db import Database
from dotenv import load_dotenv
import os

class LoginWindow(Tk):
    def __init__(self):
        super().__init__()
        
        # Настройки окна
        self.title('Авторизация')
        self.width = 400
        self.height = 400
        self.x = int(self.winfo_screenwidth()/2 - self.width/2)
        self.y = int(self.winfo_screenheight()/2 - self.height/2)
        self.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        self.resizable(False, False)
        
        # Виджеты
        ttk.Label(text="Авторизация",font=('Arial bold', 30)).pack(pady=(40))
        self.enabled = IntVar()
        fields = [
            ttk.Label(self, text='логин:', font=('Arial', 15)),
            login := ttk.Entry(self, font=('Arial', 20)),
            ttk.Label(self, text="пароль:", font=('Arial', 15)),
            password := ttk.Entry(self, show='*', font=('Arial', 20)),
            ttk.Checkbutton(self, text='Показать пароль', padding=10, 
                            variable=self.enabled,
                            command = lambda:show_password()),
            ttk.Button(self, text='Войти', padding=10, command=lambda: get_login())
        ]
        [field.pack(fill='x', padx=40) for field in fields]
        
        # Функции
        # Показать пароль
        def show_password():
            if password.cget('show') == "*":
                password.config(show="")
            else:
                password.config(show="*")
        
        # Авторизация     
        def get_login():
            load_dotenv()
            admin_login = os.getenv('admin_login')
            admin_password = os.getenv('admin_password')
            users = Database().get_request_data(" select логин, пароль, преподаватель from Аккаунт ")
            
            for user in users:
                    if login.get() == user[0] and password.get() == user[1]:
                        self.destroy()
                        self.quit()
                        ClassromTeahcerWindow().classrom_teacher(user[2])           


            if login.get() == admin_login and password.get() == admin_password:
                self.destroy()
                self.quit()
                ManagementWindow()
            else:
                messagebox.showerror(title='Ошибка авторизации', message='Неправильный логин или пароль!')

                
            
            
                
            
        
        # Запуск окна
        self.mainloop()