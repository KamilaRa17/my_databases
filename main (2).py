import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main() # Создать рамки, кнопки, поля в рамке, иконки
        self.db = db # Подключение базы данных
        self.view_records() # Просмотр базы данных в таблице

    def init_main(self):
        toolbar = tk.Frame(bg="#d7d8e0", bd=0) # Создание рамки
        toolbar.pack(side=tk.TOP, fill=tk.X) # Вывод рамки на экран с выравниваем
        self.add_img = tk.PhotoImage(file="./img/add.png") # Вставка картинки
        btn_open_dialog = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                           image=self.add_img, command=self.open_dialog) # Создание кнопки с генерацией виджета
        btn_open_dialog.pack(side=tk.LEFT) # Вывод кнопки на экран с выравниваем

        self.tree = ttk.Treeview(self, columns=("ID", "name", "phone", "email", "salary"),
                                  height=45, show="headings") # Добавление элемента колонок
        
        self.tree.column("ID", width=30, anchor=tk.CENTER) # Настраивание колон
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=100, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID") # Настраивание заголовков колон
        self.tree.heading("name", text="Имя")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Почта")
        self.tree.heading("salary", text="Зарплата")

        self.tree.pack(side=tk.LEFT) # Добавление колоноки

        self.update_img = tk.PhotoImage(file="./img/update.png") # Добавление картинки
        btn_edit_dialog = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                           image=self.update_img, command=self.open_update_dialog) # Редактирование кнопки с картинкой
        btn_edit_dialog.pack(side=tk.LEFT) # Выравнивание кнопки

        self.delete_img = tk.PhotoImage(file="./img/delete.png") # Добавление картинки
        btn_delete = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                           image=self.delete_img, command=self.delete_record) # Редактирование кнопки с картинкой
        btn_delete.pack(side=tk.LEFT) # Выравнивание кнопки
        
        self.search_img = tk.PhotoImage(file="./img/search.png") # Добавление картинки
        btn_search = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                           image=self.search_img, command=self.open_search_dialog) # Редактирование кнопки с картинкой
        btn_search.pack(side=tk.LEFT) # Выравнивание кнопки

        self.refresh_img = tk.PhotoImage(file="./img/refresh.png") # Добавление картинки
        btn_refresh = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                           image=self.refresh_img, command=self.view_records) # Редактирование кнопки с картинкой
        btn_refresh.pack(side=tk.LEFT) # Выравнивание кнопки

    def open_dialog(self): # Создание дочернего виджета
        Child()

    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary) # Заполнение записи в базе данных
        self.view_records() # Просмотр базы данных в таблице

    def view_records(self): # Просмотр базы данных в таблице
        self.db.cur.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()] # Очистка окна
        [self.tree.insert("", "end", values=row)
         for row in self.db.cur.fetchall()] # Заполнение окна
        
    def open_update_dialog(self): # Создание дочернего виджета
        Update()

    def Update_record(self, name, phone, email, salary):
        self.db.cur.execute("""UPDATE db SET name=?, phone=?, email=?, salary=? WHERE ID=?""",
                            (name, phone, email, salary, self.tree.set(self.tree.selection() [0], "#1"))) # Обновление выделеного контакта (по ID)
        # Выбор у первой выделеной строки первого элемента (ID)
        self.db.conn.commit()
        self.view_records() # Просмотр базы данных в таблице
    
    def delete_record(self): # Удаление контакта по ID
        for selection_item in self.tree.selection():
            self.db.cur.execute("""DELETE FROM db WHERE id=?""", (self.tree.set(selection_item, "#1"),)) # Удаление выделеного контакта (по ID) через цикл
        self.db.conn.commit()
        self.view_records() # Просмотр базы данных в таблице

    def open_search_dialog(self): # Создание дочернего виджета
        Search()

    def search_record(self, name): # Поиск имени
        name = ("%" + name + "%")
        self.db.cur.execute("""SELECT * FROM db WHERE name LIKE ?""", (name,))    
        [self.tree.delete(i) for i in self.tree.get_children()] # Очистка окна
        [self.tree.insert("", "end", values=row)
         for row in self.db.cur.fetchall()] # Заполнение окна

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child() # Вызов функции ниже
        self.view = app # Основная рамка в переменной view 

    def init_child(self):
        self.title("Добавить") # Имя рамки
        self.geometry("420x250") # Размер рамки
        self.resizable(False, False) # Блокировка изменения размера рамки
        self.grab_set() # заставляет текущий компонент перехватывать все события
                        # всех типов, что возникают в приложении
        self.focus_set() # Создание фокуса для получения всех событий в виджете
        
        label_name = tk.Label(self, text="ФИО") # Надпись ФИО
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text="Телефон") # Надпись Телефон
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text="E-mail") # Надпись E-mail
        label_email.place(x=50, y=110)
        label_gain = tk.Label(self, text="Зарплата") # Надпись Зарплаты
        label_gain.place(x=50, y=140)

        self.entry_name = ttk.Entry(self) # Поле ввода ФИО
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self) # Поле ввода почты
        self.entry_email.place(x=200, y=80)
        self.entry_phone = ttk.Entry(self) # Поле ввода телефона
        self.entry_phone.place(x=200, y=110)
        self.entry_gain = ttk.Entry(self) # Поле ввода зарплаты
        self.entry_gain.place(x=200, y=140)

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) # Кнопка отмены
        self.btn_cancel.place(x=250, y=180)

        self.btn_ok = ttk.Button(self, text="Добавить") # Кнопка подтверждения 
        self.btn_ok.place(x=170, y=180)

        self.btn_ok.bind("<Button-1>", lambda event:   # Отклик на левую кнопку мыши
                        self.view.records(self.entry_name.get(), # Записи аргументов в функцию record()
                                          self.entry_email.get(),
                                          self.entry_phone.get(),
                                          self.entry_gain.get()))

class Update(Child):
    def __init__(self):
        super().__init__()
        self.db = db # Подключение базы данных
        self.view = app # Основная рамка в переменной view 
        self.init_update() # Редактирование данных 
        self.default_data() # Отображение значений контакта при редактировании

    def init_update(self): # Редактирование данных 
        self.title("Редактировать контакт")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=140, y=180)
        btn_edit.bind("<Button-1>",  lambda event:   # Отклик на левую кнопку мыши
                        self.view.Update_record(self.entry_name.get(), # Записи аргументов в функцию record()
                                                self.entry_email.get(),
                                                self.entry_phone.get(),
                                                self.entry_gain.get()))
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+") # add="+"  -  Дополнительный функционал для кнопки
        self.btn_ok.destroy()
    
    def default_data(self): # Отображение значений контакта при редактировании
        self.db.cur.execute("""SELECT * FROM db WHERE ID=?""", (self.view.tree.set(self.view.tree.selection() [0], "#1"),)) # Выборка выделеного контакта (для ID)
        row = self.db.cur.fetchone() # Выбор строки контакта
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_phone.insert(0, row[3])
        self.entry_gain.insert(0, row[4])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search() # Вызов функции ниже 
        self.view = app # Основная рамка в переменной view 

    def init_search(self): # Поиск контакта
        self.title("Поиск контакта") # Имя рамки
        self.geometry("300x100") # Размер рамки
        self.resizable(False, False) # Блокировка изменения размера рамки

        label_search = tk.Label(self, text="Имя") # Создание текста
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self) # Создание поля для ввода
        self.entry_search.place(x=100, y=20, width=155)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) # Создание кнопки Закрыть
        btn_cancel.place(x=180, y=50)

        btn_search = ttk.Button(self, text="Найти") # Создание кнопки Найти
        btn_search.place(x=100, y=50)
        btn_search.bind("<Button-1>", lambda event:
                        self.view.search_record(self.entry_search.get())) # Поиск имени по кнопке
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+") # add="+"  -  Дополнительный функционал для кнопки

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("db.db") # Делаем связь с базой данных 
        self.cur = self.conn.cursor() # Делаем переменную для запросов в SQL
        self.cur.execute(""" 
        CREATE TABLE IF NOT EXISTS db (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       phone TEXT,
                       email TEXT,
                       salary TEXT)""") # Делаем запрос 
        self.conn.commit() # Выполняем запрос

    def insert_data(self, name, phone, email, salary): # Заполнение записи в базе данных
        self.cur.execute("""INSERT INTO db (name, phone, email, salary)
                       VALUES(?, ?, ?, ?)""", (name, phone, email, salary)) # Делаем запро
        self.conn.commit() # Выполняем запрос



if __name__ == "__main__": # Если имя файла "main", то ...
    root = tk.Tk()
    db = DB()
    app = Main(root) # Создание рамки
    app.pack() # Вывод рамки на экран
    root.title("Список сотрудников компании") # Имя рамки
    root.geometry("760x450") # Размер рамки
    root.resizable(False, False) # Блокировка изменения размера рамки
    root.protocol("WM_DELETE_WINDOW", root.quit) # Плавное закрытие окна
    root.mainloop() # Запускает цикл событий для отображения окна

