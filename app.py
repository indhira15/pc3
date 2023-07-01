from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'usersdb'
mysql = MySQL(app)

app.secret_key = 'Utec2023'

i_i = True

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    return render_template('index.html')


@app.route('/add_user', methods = ['POST'])
def add_user():
    if request.method == 'POST':
        des = request.form['user']
        pre = request.form['nombre']
        pre2 = request.form['apellidos']
        pre3 = request.form['clave']
        print('INSERT', des) 
        cur = mysql.connection.cursor()
        cur.execute('insert into usersdb(username,nombre, apellidos, clave) values(%s,%s, %s, %s)', (des, pre, pre2, pre3))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/reg')
def reg():
    return render_template('register.html')


@app.route('/sig', methods=['POST'])
def entrar():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        des = request.form['user']
        pre3 = request.form['clave']

    cur.execute('select * from usersdb where username = %s and clave = %s', (des, pre3))
    data = cur.fetchall()
    mysql.connection.commit()
    print(data)
    if data:
        flash('Se logeo correctamente')
        return redirect(url_for('sucess'))

    else:
        flash('datos mal colocados')
        return redirect(url_for('no_sucess'))


@app.route('/sucess')
def sucess():
    return render_template('saludar.html')

@app.route('/no_sucess')
def no_sucess():
    return render_template('adios.html')

if __name__ == '__main__':
    app.run(port=3000,debug=True)