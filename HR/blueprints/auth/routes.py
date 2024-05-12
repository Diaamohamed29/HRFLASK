from flask import request , render_template , redirect , url_for , Blueprint,session,flash
from HR.blueprints.user.routes import user
from HR.blueprints.admin.routes import admin
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
            
            print(account)

            if account[0] == 'admin' and account[1] =='admin':
                session['username'] = username
                flash('Logged in successfullly','success')
                return redirect(url_for('admin.index'))
            if account[0] == username and account[1] == password:
                session['username'] = username
                flash('Logged in successfullly','success')
                return redirect(url_for('user.index'))
            # print(account)
        
            # if account :
            #     session['username']=username 
            #     session['password']=password
            #     print(username) 
            #     print(password)
            #     session['username'] == username and session['password'] == password
            #     return redirect(url_for('user.index'))
            # if username == 'admin' and password =='admin':
            #     return redirect(url_for('admin.index'))
            # if session['username'] =='super' and password =='super':
            #     pass 

         
    return render_template('auth/login.html')
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
