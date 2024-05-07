from flask import request , render_template , redirect , url_for , Blueprint,session
from HR.blueprints.user.routes import user
from HR.db import connection,cursor
auth = Blueprint("auth", __name__, template_folder="templates")





@auth.route('/')
def landingPage():
    return render_template('auth/index.html')

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM user_ WHERE username = ? AND password = ?"
            cursor.execute(query, (username, password))
            account = cursor.fetchone()
            username_t = account[0]
            password_t = account[1]
            if account :
                session['username'] = username
                return redirect(url_for('user.index'))
            if username_t == 'admin' and password =='admin':
                pass
            if username_t =='super' and password =='super':
                pass 

         
    return render_template('auth/login.html')
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
