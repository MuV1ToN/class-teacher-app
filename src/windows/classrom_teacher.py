from tkinter import Tk, ttk, Listbox
from src.database.db import Database


class ClassromTeahcerWindow(Tk):
    def __init__(self):
        super().__init__()
        
    def classrom_teacher(self, teacher_id):
        # Настройки окна
        self.title('Классное руководстов')
    
        self.width = 400
        self.height = 400
        self.minsize(self.width, self.height)
        self.x = int(self.winfo_screenwidth()/2 - self.width/2)
        self.y = int(self.winfo_screenheight()/2 - self.height/2)
        self.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        
        teacher_info = Database().get_request_data(f"""
                                                   select 
                                                   id, 
                                                   concat(фамилия,' ',имя,' ',отчество) as фио, 
                                                   предмет, группа 
                                                   from Преподаватель 
                                                   where id = %s
                                                   """ % teacher_id)
        
        print(teacher_info)
        self.student_grades = Database().get_request_data(f"""
                                                        SELECT
                                                        CONCAT(Студент.фамилия, ' ', Студент.имя, ' ', Студент.отчество) AS фио,
                                                        GROUP_CONCAT(Успеваемость.оценка,', ') AS оценки,
                                                        Предмет.предмет
                                                        FROM Успеваемость
                                                        JOIN Предмет ON Успеваемость.предмет = Предмет.id
                                                        JOIN Студент ON Успеваемость.студент = Студент.id
                                                        WHERE Студент.группа = %s
                                                        GROUP BY Студент.id, Предмет.id
                                                        ORDER BY Студент.фамилия, Студент.имя, Студент.отчество;
                                                      """ % teacher_info[0][3])
        
        # Виджеты
        classrom_teacher_frame = ttk.Frame(self)
        classrom_teacher_frame.pack(fill='both', expand=1)
        
        classrom_teacher = ttk.Label(
            classrom_teacher_frame, 
            text=f'{teacher_info[0][1]}', 
            font=('Arial', 20)
            )
        classrom_teacher.pack(pady = 10)
        
        listbox = Listbox(classrom_teacher_frame, font=('Arial', 15))
        inserted_students = set() 
        for student in self.student_grades:
            if student[0] not in inserted_students:
                listbox.insert('end', student[0])
                inserted_students.add(student[0])    
        listbox.pack(expand=1, fill='both', padx=20)
        
        ttk.Button(classrom_teacher_frame, text='Обновить', padding=10).pack(pady=10)
        
        # Функции
        def exit():
            self.student_grades = Database().get_request_data(f"""
                                                        SELECT
                                                        CONCAT(Студент.фамилия, ' ', Студент.имя, ' ', Студент.отчество) AS фио,
                                                        GROUP_CONCAT(Успеваемость.оценка,', ') AS оценки,
                                                        Предмет.предмет
                                                        FROM Успеваемость
                                                        JOIN Предмет ON Успеваемость.предмет = Предмет.id
                                                        JOIN Студент ON Успеваемость.студент = Студент.id
                                                        WHERE Студент.группа = 1
                                                        GROUP BY Студент.id, Предмет.id
                                                        ORDER BY Студент.фамилия, Студент.имя, Студент.отчество;
                                                      """)
    
        def on_select(event):
            selected_student = listbox.get(listbox.curselection())
            selected_student_grades = [student for student in self.student_grades if student[0] == selected_student]
            if selected_student_grades:
                grade_window = Tk()
                grade_window.title(f'Оценки - {selected_student_grades[0][0]}')
                width = 300
                height = 300
                grade_window.minsize(width, height)
                x = int(grade_window.winfo_screenwidth()/2 - width/2)
                y = int(grade_window.winfo_screenheight()/2 - height/2)
                grade_window.geometry(f'{width}x{height}+{x}+{y}')
                for grade in selected_student_grades:
                    label = ttk.Label(grade_window, text=f' Предмет: {grade[2]}\tОценки: {grade[1]}', font=('Arial', 10))
                    label.pack(anchor='sw', fill='both')
                grade_window.mainloop()

        listbox.bind('<Double-Button-1>', on_select)
            
                
        self.mainloop()
        
        
    
    