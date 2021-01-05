from flask import Flask, render_template
import sqlite3

def get_db_connection():    
    conn = sqlite3.connect('database.db') #открываем соединение с файлом базы данных database.db
    
    # устанавливаем атрибут row_factory в sqlite3.Row, чтобы получить доступ 
    # к столбцам на основе имен. Это означает, что подключение к базе 
    # данных будет возвращать строки, которые ведут себя как обычные словари Python    
    conn.row_factory = sqlite3.Row #

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')