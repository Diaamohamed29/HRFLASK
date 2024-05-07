from flask import request , render_template , redirect , url_for , Blueprint,session
from HR.db import connection , cursor 
from datetime import datetime , timedelta
user = Blueprint("user", __name__, template_folder="templates")



@user.route('/')

def index():
        
    username = session['username']
    
    cursor.execute("SELECT name from employes where employe_id = ?",(username))
    name = cursor.fetchall()

# Get current date information
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_day = datetime.now().day

    # Define start and end dates based on the current date
    if current_day >= 26:
        start_date = datetime(current_year, current_month, 26).date()
        end_date = (datetime(current_year, current_month, 25) + timedelta(days=30)).date()
    else:
        current_month -= 1  # Adjust current month to previous month
        if current_month == 0:  # Handle the case where the current month is January
            current_month = 12
            current_year -= 1
        start_date = (datetime(current_year, current_month, 25) - timedelta(days=30)).date()
        end_date = datetime(current_year, current_month, 25).date()

    # Check if the current day is between 26th of the previous month and 25th of the current month
    if start_date <= datetime.now().date() <= end_date:
        print("Current day is between 26th of the previous month and 25th of the current month")
    else:
        print("Current day is not between 26th of the previous month and 25th of the current month")

    print("Start Date:", start_date)
    print("End Date:", end_date)
    return render_template('user/index.html',username=username,name=name,current_month=current_month)

@user.route('/attendance')
def attendance():
    username = session['username']
    
    cursor.execute("SELECT name from employes where employe_id = ?",(username))
    name = cursor.fetchall()

    current_month = datetime.now().month
    current_year = datetime.now().year
    current_day = datetime.now().day
    start_date = (datetime(current_year, current_month, 25) - timedelta(days=30)).date()
    end_date = datetime(current_year, current_month, 25).date()
    if current_day >= 26:
        current_month = datetime.now().month
        start_date = (datetime(current_year, current_month, 26)).date()
        end_date = (datetime(current_year, current_month, 25) + timedelta(days=30)).date()

    query = "SELECT DISTINCT employe_id  , date , check_in , check_out,check_in_per,check_out_per  FROM zktecoAll  WHERE employe_id = ? and date between ? and ? ORDER BY date"
    cursor.execute(query, (int(username),str(start_date),str(end_date),))
    results = cursor.fetchall()
    

    return render_template('user/attendance.html',username=username,name=name,results=results)

























































@user.route('/vacations')
def vacations():
    username = session['username']
    cursor.execute("select name from employes where employe_id = ?",(username))
    name = cursor.fetchall()
    cursor.execute(""" select normal_days from vacations where employe_id = ? """,(username))
    normal_days = cursor.fetchall()
    cursor.execute(""" select casual_days from vacations where employe_id = ?""",(username))
    casual_days = cursor.fetchall()
    cursor.execute(""" select total_days from vacations where employe_id = ? """,(username))
    total_days = cursor.fetchall()
    return render_template('user/vacations.html',name=name,username=username,normal_days=normal_days,casual_days=casual_days,total_days=total_days)
    



@user.route('/add_vacation')
def add_vacation():
    username = session['username']
    cursor.execute("select name from employes where employe_id = ?",(username))
    name = cursor.fetchall()
    return render_template('user/add_vacation.html',name=name,username=username)




# @user.route('/view_vacations')
# def view_vacations():
#     username = session['username']
#     cursor.execute("select name from employes where employe_id = ?",(username))
#     name = cursor.fetchall()
#     return render_template('user/view_vacations.html',name=name,username=username)
    























@user.route('/missions')
def missions():
    username = session['username']
    cursor.execute("select name from employes where employe_id = ?",(username))
    name = cursor.fetchall()
    return render_template('user/missions.html',name=name,username=username)

@user.route('/add_mission')
def add_mission():
    username = session['username']
    cursor.execute("select name from employes where employe_id = ?",(username))
    name = cursor.fetchall()

    cursor.execute("Select job_role from employes where employe_id = ?" ,(username))
    job_role = cursor.fetchall()
    return render_template('user/add_mission.html',name=name,username=username,job_role=job_role)
@user.route('/view_missions')
def view_missions():
    username = session['username']
    cursor.execute("select name from employes where employe_id = ?",(username))
    name = cursor.fetchall()
    cursor.execute(""" 
            select employe_id , name , date , from_time , to_time ,reason from missions where employe_id = ?

        """,(username))
    results = cursor.fetchall()
    return render_template('user/view_missions.html',name=name,username=username,results=results)
