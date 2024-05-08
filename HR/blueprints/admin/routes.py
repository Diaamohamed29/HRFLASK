from flask import request , render_template , redirect , url_for , Blueprint,session
from HR.db import connection , cursor 
from datetime import datetime , timedelta


admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/employes')
def employes():
    cursor.execute(""" 

            SELECT COUNT(*) AS row_count
            FROM employes;   
            """)
    number = cursor.fetchall()
    

    cursor.execute(""" 

            select employe_id , name , department , job_role ,
                    qualification , national_id , address , telephone , hire_date ,
                   net_salary , allowance from employes """)
    results = cursor.fetchall()
    return render_template('admin/employes.html',number=number,results=results)





@admin.route('/submit_attendance',methods=['POST'])
def submit_attendance():
    cursor.execute("SELECT DISTINCT employe_id from zktecoAll")
    all_employes = cursor.fetchall()
    all_employes = [emp[0] for emp in all_employes]
    

    
    employe_id = request.form['employeid']
    print(employe_id)
    from_date = request.form['fromDate']
    to_date = request.form['toDate']

    if employe_id == 'all':
        cursor.execute('SELECT employe_id, date, check_in, check_out FROM zktecoAll WHERE date BETWEEN ? AND ? ', (from_date, to_date))
    else:
        cursor.execute('SELECT  employe_id, date, check_in, check_out FROM zktecoAll WHERE employe_id = ? AND date BETWEEN ? AND ? ', (employe_id, from_date, to_date))
    results = cursor.fetchall()


    return render_template('admin/attendance.html',results=results,all_employes=all_employes)



@admin.route('/attendance')
def attendance():
    
    cursor.execute("SELECT DISTINCT employe_id from zktecoAll")
    all_employes = cursor.fetchall()
    all_employes = [emp[0] for emp in all_employes]
    print(all_employes)
    


    return render_template('admin/attendance.html',all_employes=all_employes)







@admin.route('/vacations')
def vacations():
    return render_template('admin/vacations.html')
@admin.route('/all_vacations')
def all_vacations():
    return render_template('admin/all_vacations.html')
@admin.route('/add_vacation')
def add_vacation():
    return render_template('admin/add_vacation.html')




@admin.route('/missions')
def missions():
    return render_template('admin/missions.html')
@admin.route('/add_mission')
def add_mission():
    return render_template('admin/add_missions')
@admin.route('/view_missions')
def view_missions():
    return render_template('admin/view_missions.html')