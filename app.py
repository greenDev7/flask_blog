from flask import Flask, render_template, request, url_for, flash, redirect 
import sqlite3
from werkzeug.exceptions import abort

def get_db_connection():    
    conn = sqlite3.connect('database.db') #Открываем соединение с файлом базы данных database.db
    
    # Устанавливаем атрибут row_factory в sqlite3.Row, чтобы получить доступ 
    # к столбцам на основе имен. Это означает, что подключение к базе 
    # данных будет возвращать строки, которые ведут себя как обычные словари Python    
    conn.row_factory = sqlite3.Row
    return conn
    
def get_post(post_id):
    """Возвращает post по его id"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None: # Если такого поста не существует
       abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key' # Секретный ключ должен представлять собой длинную случайную строку

@app.route('/')
def index():
    conn = get_db_connection() # открываем подключение к базе данных
    posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall() # выполняем SQL-запрос. Метод fetchall() достает все строки запроса.
    conn.close() # Закрываем подключение к БД
    
    # Передаем объект posts в качестве аргумента, который содержит результаты, полученные из базы данных. 
    # Это откроет доступ к постам блога в шаблоне index.html.
    return render_template('index.html', posts = posts)
    
@app.route('/<int:post_id>') # Правило переменной. После слеша передаем id-шник поста
def post(post_id): # Здесь берем этот id
    post = get_post(post_id) # и по нему достаем пост с помощью функции get_post()
    return render_template('post.html', post = post) # Формируем html-страницу с отображением нашего поста
    

# Запросы GET принимаются по умолчанию. 
# Для того чтобы также принимать запросы POST, 
# которые посылаются браузером при подаче форм,
# передаем кортеж с приемлемыми типами запросов в аргумент methods декоратора @app.route()
@app.route('/create', methods = ('GET', 'POST'))
def create():
    """ Создает маршрут /create, который принимает запросы GET и POST"""
    return render_template('create.html')
    
