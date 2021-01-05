from flask import Flask, render_template
import sqlite3

def get_db_connection():    
    conn = sqlite3.connect('database.db') #Открываем соединение с файлом базы данных database.db
    
    # Устанавливаем атрибут row_factory в sqlite3.Row, чтобы получить доступ 
    # к столбцам на основе имен. Это означает, что подключение к базе 
    # данных будет возвращать строки, которые ведут себя как обычные словари Python    
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection() # открываем подключение к базе данных
    posts = conn.execute('SELECT * FROM posts').fetchall() # выполняем SQL-запрос. Метод fetchall() достает все строки запроса.
    conn.close() # Закрываем подключение к БД
    
    # Передаем объект posts в качестве аргумента, который содержит результаты, полученные из базы данных. 
    # Это откроет доступ к постам блога в шаблоне index.html.
    return render_template('index.html', posts = posts)