from flask import request , render_template , redirect , url_for , Blueprint,session,jsonify,flash
from HR.db import connection , cursor ,connect_to_zkteco
from datetime import datetime , timedelta


super = Blueprint("super", __name__, template_folder="templates",static_folder='static')


@super.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        cursor.execute("SELECT employe_id FROM employes")
        all_employes = [emp[0] for emp in cursor.fetchall()]
        return render_template('super/index.html', all_employes=all_employes)

    elif request.method == 'POST':
        cursor.execute("SELECT employe_id FROM employes")
        all_employes = [emp[0] for emp in cursor.fetchall()]
        
        employe_id = request.form['employeid']
        cursor.execute(""" SELECT name , date , ISNULL(CONVERT(varchar, from_time, 108), '') AS from_time , ISNULL(CONVERT(varchar, to_time, 108), '') AS to_time , reason  
                       FROM missions WHERE status = 1 and employe_id = ?""", (employe_id,))
        missions_data = cursor.fetchall()

        cursor.execute("""select name , date , from_date , to_date , no_of_days
                         from vacation_requests where status = 1 and employe_id = ?""",(employe_id))
        vacations_requests = cursor.fetchall()

        cursor.execute("select * from vacations where employe_id = ?",(employe_id))
        vacations = cursor.fetchall()

        cursor.execute("""SELECT name, day, date,   ISNULL(CONVERT(varchar, check_in, 108), '') AS check_in, 
                         ISNULL(CONVERT(varchar, check_out, 108), '') AS check_out
                       , extra_hours, 
       check_vacation, check_mission, check_per
FROM head_attendance
WHERE employe_id = ?
ORDER BY 
    CASE WHEN name = 'Total' THEN 1 ELSE 0 END,  -- Sort 'total' row last
    date;""",(employe_id))
        attendance_data = cursor.fetchall()


        return render_template('super/index.html', all_employes=all_employes,
                                missions_data=missions_data,
                                vacations_requests=vacations_requests,
                                vacations=vacations,
                                attendance_data=attendance_data)
@super.route('/head_payroll')
def head_payroll():
    cursor.execute('select * from head_payroll')
    results = cursor.fetchall()
    return render_template('super/head_payroll.html',results=results,cursor=cursor)

