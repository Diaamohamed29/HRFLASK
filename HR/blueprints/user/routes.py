from flask import request , render_template , redirect , url_for , Blueprint,session,flash
from HR.db import connection , cursor ,connect_to_zkteco
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
    connect_to_zkteco()
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

    query = "SELECT DISTINCT employe_id  , Date , check_in , check_out,check_in_per,check_out_per  FROM zktecoAll  WHERE employe_id = ? and Date between ? and ? ORDER BY Date"
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
    cursor.execute(""" select employe_id , date , from_date , to_date ,
                    no_of_days , vac_type from vacation_requests where employe_id = ?""",(username))
    results = cursor.fetchall()
    return render_template('user/vacations.html',name=name,username=username,normal_days=normal_days,
                           casual_days=casual_days,total_days=total_days,results=results)
    



@user.route('/add_vacation',methods=['POST','GET'])
def add_vacation():
    if request.method == 'GET':
        cursor = connection.cursor()
        username = session['username']
        cursor.execute("select name from employes where employe_id = ?",(username))
        name = cursor.fetchall()
        cursor.execute("Select job_role from employes where employe_id = ?" ,(username))
        job_role = cursor.fetchall()
        return render_template('user/add_vacation.html',name=name,username=username,job_role=job_role)

    elif request.method == 'POST':
        employe_id = request.form.get('employe_id')
        type = request.form.get('type')
        name = request.form.get('name')
        job_role = request.form.get('job_role')
        date = request.form.get('date')
        no_of_days = request.form.get('no_of_days')
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')
        status = 0 
          # Here you can insert the vacation request data into your database table
            # Example code:
        cursor = connection.cursor()
        sql = "INSERT INTO vacation_requests (employe_id,name, job_role, vac_type, date, no_of_days, from_date, to_date,status) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)"
        cursor.execute(sql, (employe_id, name,job_role, type, date, no_of_days, from_date, to_date,status))
        connection.commit()
        cursor.execute(""" 
            update vacation_requests 
                       set department = (select department from employes where employe_id = vacation_requests.employe_id)
            """)
        connection.commit()
        cursor.close()

        flash('Vacation request added successfully!', 'success')
        return redirect(url_for('user.add_vacation'))



@user.route('/vacation_requests')
def vacation_requests():
    employe_id = session['username']
    cursor.execute("""SELECT employe_id, name, department, job_role, date, vac_type,
                                      no_of_days, from_date, to_date ,status
                               FROM vacation_requests where employe_id  = ? """,(employe_id) )
    results = cursor.fetchall()
    return render_template('user/vacation_requests.html',employe_id=employe_id,results=results)









@user.route('/mission_requests')
def mission_requests():
    
         
    employe_id = session['username']

    cursor.execute("""SELECT employe_id,name,job_role ,date, from_time,
                                      to_time, reason ,status
                               FROM missions where employe_id  = ? """,(employe_id) )
    results = cursor.fetchall()
    return render_template('user/mission_requests.html',employe_id=employe_id,results=results)
@user.route('/missions')
def missions():
    username = session['username']
    cursor.execute("select name from employes where employe_id = ?",(username))
    name = cursor.fetchall()
    return render_template('user/missions.html',name=name,username=username)

@user.route('/add_mission',methods=['POST','GET'])
def add_mission():
    if request.method == 'GET':
        username = session['username']
        cursor = connection.cursor()
        cursor.execute("select name from employes where employe_id = ?",(username))
        name = cursor.fetchall()

        cursor.execute("Select job_role from employes where employe_id = ?" ,(username))
        job_role = cursor.fetchall()
        return render_template('user/add_mission.html',name=name,username=username,job_role=job_role)
    elif request.method =='POST':
        employe_id = request.form.get('employe_id')
        name = request.form.get('name')
        job_role = request.form.get('job_role')
        date = request.form.get('date')
        from_time = request.form.get('from_time')
        to_time = request.form.get('to_time')
        reason = request.form.get('reason')
        status = 0
        cursor = connection.cursor()
        sql = "INSERT INTO missions (employe_id,name, date, job_role,from_time, to_time, reason,status) VALUES (?, ?, ?, ?, ?, ?,?,?)"
        cursor.execute(sql, (employe_id, name, date,job_role, from_time, to_time,reason,status))
        connection.commit()
        
        flash('mission request added successfully!', 'success')
        return redirect(url_for('user.add_mission'))
@user.route('/view_missions')
def view_missions():
    username = session['username']
    cursor.execute("select name from employes where employe_id = ?",(username))
    name = cursor.fetchall()
    cursor.execute(""" 
            select employe_id , name ,job_role, date , from_time , to_time ,reason from missions where employe_id = ?

        """,(username))
    results = cursor.fetchall()
    return render_template('user/view_missions.html',name=name,username=username,results=results)
