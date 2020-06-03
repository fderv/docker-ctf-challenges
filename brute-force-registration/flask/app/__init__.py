from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_mysqldb import MySQL
from flask_simple_captcha import CAPTCHA
import MySQLdb.cursors
import re
import os

app = Flask(__name__)


app.secret_key = 'asdasdas'
CAPTCHA_CONFIG = {'SECRET_CSRF_KEY':'wMmeltW4mhwidorQRli6Oijuhygtfgybunxx9VPXldz'}

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'user_db'

CAPTCHA = CAPTCHA(config={'SECRET_CSRF_KEY':'wMmeltW4mhwidorQRli6Oijuhygtfgybunxx9VPXldz'})
app = CAPTCHA.init_app(app)
mysql = MySQL(app)

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedIn'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            return render_template("login.html", error="Incorrect email/password!")
    else:
        return render_template("login.html", error="")

@app.route('/register', methods=["GET", "POST"])
def register():
    captcha = ""
    captcha_active = False
    attempts_so_far = 0
    if not (request.cookies.get('Attempts') is None):
        attempts_so_far = int(request.cookies.get('Attempts'))
    if attempts_so_far > 5:
        captcha_active = True
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'code' in request.form:
        email = request.form['email']
        password = request.form['password']
        code = request.form['code']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if not email or not password or not code:
            attempts = str(attempts_so_far + 1)
            if int(attempts) > 5:
                captcha = CAPTCHA.create()
                captcha_active = True
            res = make_response(render_template("register.html", error="Please fill out the form!", captcha=captcha, captcha_active=captcha_active))
            res.set_cookie('Attempts', attempts, max_age=None)
            return res
        elif account:
            attempts = str(int(request.cookies.get('Attempts')) + 1)
            if int(attempts) > 5:
                captcha = CAPTCHA.create()
                captcha_active = True
            res = make_response(render_template("register.html", error="Account already exists!", captcha=captcha, captcha_active=captcha_active))
            res.set_cookie('Attempts', attempts, max_age=None)
            return res
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            attempts = str(int(request.cookies.get('Attempts')) + 1)
            if int(attempts) > 5:
                captcha = CAPTCHA.create()
                captcha_active = True
            res = make_response(render_template("register.html", error="Invalid email address!", captcha=captcha, captcha_active=captcha_active))
            res.set_cookie('Attempts', attempts, max_age=None)
            return res
        elif not validate_code(code):
            attempts = str(int(request.cookies.get('Attempts')) + 1)
            if int(attempts) > 5:
                captcha = CAPTCHA.create()
                captcha_active = True
            res = make_response(render_template("register.html", error="Wrong registration code!", captcha=captcha, captcha_active=captcha_active))
            res.set_cookie('Attempts', attempts, max_age=None)
            return res
        elif captcha_active:
            print("HERE WE ARE!")
            c_hash = request.form.get('captcha-hash')
            c_text = request.form.get('captcha-text')
            if not CAPTCHA.verify(c_text, c_hash):
                attempts = str(int(request.cookies.get('Attempts')) + 1)
                if int(attempts) > 5:
                    captcha = CAPTCHA.create()
                    captcha_active = True
                res = make_response(render_template("register.html", error="Wrong captcha!", captcha=captcha, captcha_active=captcha_active))
                res.set_cookie('Attempts', attempts, max_age=None)
                return res
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (email, password))
            mysql.connection.commit()
            res = make_response(render_template("register.html", error="You have successfully registered!", captcha=captcha, captcha_active=captcha_active))
            res.set_cookie('Attempts', str(0), max_age=None)
            return res
    elif request.method == 'POST':
        attempts = str(int(request.cookies.get('Attempts')) + 1)
        if int(attempts) > 5:
            captcha = CAPTCHA.create()
            captcha_active = True
        # Form is empty... (no POST data)
        res = make_response(render_template("register.html", error="Please fill out the form!", captcha=captcha, captcha_active=captcha_active))
        res.set_cookie('Attempts', attempts, max_age=None)
        return res
    else:
        if not request.cookies.get('Attempts'):
            res = make_response(render_template("register.html", error="", captcha=captcha, captcha_active=captcha_active))
            res.set_cookie('Attempts', "1", max_age=None)
            return res
        attempts = int(request.cookies.get('Attempts'))
        if attempts > 5:
            captcha = CAPTCHA.create()
            captcha_active = True
        return render_template("register.html", error="", captcha=captcha, captcha_active=captcha_active)
    
@app.route('/home', methods=["GET", "POST"])
def home():
    if 'loggedIn' in session:
        return render_template('home.html', email=session['email'], flag=os.getenv("APP_FLAG"))
    return redirect(url_for('login'))

def validate_code(code):
    if code == '002864':
        return True
    return False