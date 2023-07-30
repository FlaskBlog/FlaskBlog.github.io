import sqlite3
import os
from os import path
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_mysqldb import MySQL
from werkzeug.exceptions import abort
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import Blueprint
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'flaskcontacts'
app.config['UPLOAD_FOLDER'] = './static/uploads'
mysql = MySQL(app)

ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif', 'pdf', 'docx'])

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/')
def index1():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts=data)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES(?, ?)',(title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('¡El título es requerido!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'' WHERE id = ?',(title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Email = request.form['Email']
        Clave = request.form['Contraseña']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (Nombre, Email, Clave) VALUES (%s, %s, %s)', (Nombre, Email, Clave))
        mysql.connection.commit()
        flash('¡Se ha registrado correctamente!')
        return redirect(url_for('index1'))

@app.route('/edit/<id>', methods = ['POST'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return redirect(url_for('edit_contact.html', contact=data[0]))


@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Email = request.form['Email']
        Contraseña = request.form['Contraseña']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE FROM contacts SET Nombre=%s, Email=%s, Contraseña=%s WHERE id = %s', (Nombre, Email, Contraseña, id))
        mysql.connection.commit()
        flash('Contacto actualizado')
        return redirect(url_for('index1'))

@app.route('/delete/<string:id>', methods = ['POST'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto removido')
    return redirect(url_for('index1'))

@app.route("/")
def upload_file():
    return render_template('index.html')


def hello():
    return 'Hello, World!'

def allowed_file(file):
    file = file.split('.')
    if file[1] in ALLOWED_EXTENSIONS:
        print(file)
        return True

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['uploadfile']
        print(file, file.filename)
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'El archivo se subió satisfactoriamente'

@app.route('/credits', methods=['GET','POST'])
def credits():
    return render_template('credits.html')

app.run(None,5000,True)

