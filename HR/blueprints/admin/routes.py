from flask import request , render_template , redirect , url_for , Blueprint,session,jsonify,flash
from HR.db import connection , cursor ,connect_to_zkteco
from datetime import datetime , timedelta


admin = Blueprint("admin", __name__, template_folder="templates")




### MAIN ADMIN PAGE
@admin.route('/')
def index():
    return render_template('admin/index.html')
### END ADMIN PAGE ###


### EMPLOYES PAGES ###


@admin.route('/employes')
def employes():

    return render_template('admin/employes.html')

@admin.route('/add_employe', methods=["POST", "GET"])
def add_employe():
    if request.method == 'GET':
        return render_template('admin/add_employe.html')
    elif request.method == 'POST':
        try:
            cursor = connection.cursor()  # Initialize cursor

            # Fetch form data
            employe_id = request.form['employeid']
            name = request.form['name']
            job_role = request.form['job_role']
            department = request.form['department']
            net_salary = request.form['net_salary']
            allowance = request.form['allowance']
            telephone = request.form['telephone']
            qualification = request.form['qualification']
            national_id = request.form['national_id']
            address = request.form['address']
            print(employe_id,name,job_role)
            # Prepare and execute SQL INSERT statement
            sql = """INSERT INTO employes (employe_id, name, job_role, department, net_salary, allowance, telephone, qualification, national_id, address)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (employe_id, name, job_role, department, net_salary, allowance, telephone,
                                 qualification, national_id, address))
            connection.commit()

            flash('Employee added successfully!', 'success')  # Flash success message
            return redirect(url_for('admin.add_employe'))  # Redirect to the same page after adding the employee
        except Exception as e:
            connection.rollback()  # Rollback the transaction if an error occurs
            return f"Error: {e}"
        finally:
            cursor.close()  # Close cursor after execution


@admin.route('/update_employe',methods=['POST'])
def update_employe():
    try:
        cursor = connection.cursor()

        # Fetch data from the form
        employee_id = request.form['employeeId']
        cell_index = request.form['cellIndex']
        new_value = request.form['newValue']

        # Determine which column to update based on the cell index
        columns = ['employe_id', 'name', 'department', 'job_role', 'qualification', 'national_id', 'address', 'telephone', 'hire_date', 'net_salary', 'allowance']
        column_to_update = columns[int(cell_index)]

        # Prepare and execute the SQL UPDATE statement
        sql = f"UPDATE employes SET {column_to_update} = ? WHERE employe_id = ?"
        cursor.execute(sql, (new_value, employee_id))
        connection.commit()

        flash('Employe Updated successfully!', 'success') 
    except Exception as e:
        connection.rollback()
        return f"Error: {e}"
    finally:
        cursor.close()
    
        return redirect(url_for('admin.view_employes'))
@admin.route('/delete_employe',methods=['POST'])
def delete_employe():
    try:
        cursor = connection.cursor()

        # Get the employee ID from the form submission
        employee_id = request.form['employeeId']

        # Prepare and execute the SQL DELETE statement
        sql = "DELETE FROM employes WHERE employe_id = ?"
        cursor.execute(sql, (employee_id,))
        connection.commit()

        flash('Employee deleted successfully!', 'success')
    except Exception as e:
        connection.rollback()
        flash(f"Error deleting employee: {e}", 'error')
    finally:
        cursor.close()

    return redirect(url_for('admin.view_employes'))


@admin.route('/view_employes')
def view_employes():
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
    return render_template('admin/view_employes.html',number=number,results=results)


### END EMPLOYES PAGES ###







### ATTENDANCE PAGE ###

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
    connect_to_zkteco()
    cursor.execute("SELECT DISTINCT employe_id from zktecoAll")
    all_employes = cursor.fetchall()
    all_employes = [emp[0] for emp in all_employes]
    print(all_employes)
    


    return render_template('admin/attendance.html',all_employes=all_employes)


### END ATTENDANCE PAGE ###



### VACATIONS PAGE ###
@admin.route('/vacations')
def vacations():
    return render_template('admin/vacations.html')

@admin.route('/vacation_requests', methods=['POST', 'GET'])
def vacation_requests():
    if request.method == 'POST':
        try:
            employe_id = request.form.get('employe_id')
            date = request.form.get('date')
            action = request.form.get('action')

            if action == 'accept':
                cursor.execute(""" 
                    UPDATE vacation_requests 
                    SET status = 1 
                    WHERE employe_id = ? AND date = ?
                """, (employe_id, date))
                connection.commit()
                flash("Vacation request accepted successfully!", "success")

            elif action == 'reject':
                cursor.execute(""" 
                    UPDATE vacation_requests
                    SET status = -1 
                    WHERE employe_id = ? AND date = ?
                """, (employe_id, date))
                connection.commit()
                flash("Vacation request rejected successfully!", "danger")

            else:
                flash("Invalid action!", "danger")

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")

        return redirect(url_for('admin.vacation_requests'))

    else:
        try:
            cursor.execute("""SELECT employe_id, name, department, job_role, date, vac_type,
                                      no_of_days, from_date, to_date 
                               FROM vacation_requests 
                               WHERE status = 0 """)
            results = cursor.fetchall()
            return render_template('admin/vacation_requests.html', results=results)
        
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('admin.vacation_requests'))




@admin.route('/all_vacations')
def all_vacations():
    cursor.execute("""
            select * from vacations
        """)
    results = cursor.fetchall()
    return render_template('admin/all_vacations.html',results=results)



@admin.route('/add_vacation',methods=["GET","POST"])
def add_vacation():
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("""SELECT employe_id FROM employes""")
        all_employes = [emp[0] for emp in cursor.fetchall()]
        cursor.execute(""" select distinct job_role from employes """)
        job_roles = [job_role[0] for job_role in cursor.fetchall()]


        return render_template('admin/add_vacation.html',all_employes=all_employes,job_roles=job_roles)
    elif request.method == 'POST':
        try:
        # Retrieve form data
            employe_id = request.form['employe_id']
            job_role = request.form['job_role']
            type = request.form['type']
            date = request.form['date']
            no_of_days = request.form['no_of_days']
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            status = 1

            # Here you can insert the vacation request data into your database table
            # Example code:
            cursor = connection.cursor()
            sql = "INSERT INTO vacation_requests (employe_id, job_role, vac_type, date, no_of_days, from_date, to_date,status) VALUES (?, ?, ?, ?, ?, ?, ?,?)"
            cursor.execute(sql, (employe_id, job_role, type, date, no_of_days, from_date, to_date,status))
            connection.commit()
            cursor.execute(""" 

                UPDATE vacation_requests 
                SET name = (SELECT name FROM employes WHERE employe_id = vacation_requests.employe_id),
                    department = (SELECT department FROM employes WHERE employe_id = vacation_requests.employe_id)

            """)
            connection.commit()
            cursor.close()

            flash('Vacation request added successfully!', 'success')
        except Exception as e:
            flash(f"Error adding vacation request: {e}", 'error')

        return redirect(url_for('admin.add_vacation'))




### END VACATIONS PAGE ###


### MISSIONS PAGE ###

@admin.route('/missions')
def missions():
    return render_template('admin/missions.html')




@admin.route('/add_mission_page', methods=['GET', 'POST'])
def add_mission_page():
    if request.method == 'GET':
        cursor = connection.cursor()  # Initialize cursor
        try:
            cursor.execute("""SELECT employe_id FROM employes""")
            all_employes = [emp[0] for emp in cursor.fetchall()]
            return render_template('admin/add_mission.html', all_employes=all_employes)
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()  # Close cursor after execution
    elif request.method == 'POST':
        try:
            cursor = connection.cursor()  # Initialize cursor

            # Fetch form data
            employee_id = request.form['employe_id']
            date = request.form['date']
            from_time = request.form['from_time']
            to_time = request.form['to_time']
            reason = request.form['reason']
            status = 0

            # Prepare and execute SQL INSERT statement
            sql = """INSERT INTO missions (employe_id, date, from_time, to_time, reason,status)
                     VALUES (?, ?, ?, ?, ?,?)"""
            cursor.execute(sql, (employee_id, date, from_time, to_time, reason,status))
            connection.commit()
            cursor.execute(""" 
                    update missions 
                           set name = (select name from employes where employe_id = missions.employe_id),
                                job_role = (select job_role from employes where employe_id = missions.employe_id)
                """)
            connection.commit()
            flash('Mission added successfully!', 'success')  # Flash success message
            return redirect(url_for('admin.add_mission_page'))  # Redirect to the same page after adding the mission
        except Exception as e:
            connection.rollback()  # Rollback the transaction if an error occurs
            return f"Error: {e}"
        finally:
            cursor.close()  # Close cursor after execution



@admin.route('/all_missions')
def view_missions():
    return render_template('admin/all_missions.html')


@admin.route('/mission_requests',methods=["POST","GET"])
def mission_requests():
    if request.method == 'POST':
        try:
            employe_id = request.form.get('employe_id')
            date = request.form.get('date')
            action = request.form.get('action')

            if action == 'accept':
                cursor.execute(""" 
                    UPDATE missions 
                    SET status = 1 
                    WHERE employe_id = ? AND date = ?
                """, (employe_id, date))
                connection.commit()
                flash("Mission request accepted successfully!", "success")

            elif action == 'reject':
                cursor.execute(""" 
                    UPDATE missions
                    SET status = -1 
                    WHERE employe_id = ? AND date = ?
                """, (employe_id, date))
                connection.commit()
                flash("Mission request rejected !", "danger")

            else:
                flash("Invalid action!", "danger")

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")

        return redirect(url_for('admin.mission_requests'))

    else:
        try:
            cursor.execute("""SELECT employe_id, name, job_role, date, from_time, to_time,
                                      reason
                               FROM missions 
                               WHERE status = 0 """)
            results = cursor.fetchall()
            return render_template('admin/mission_requests.html', results=results)
        
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('admin.mission_requests'))



### END MISSIONS PAGE ###




### REPORTS PAGES ###
@admin.route('/reports')
def reports():
    return render_template('admin/reports.html')
### END REPORT PAGE ###


### GAZ PAGE ###
@admin.route('/gaz')
def gaz():
    return render_template('admin/gaz.html')
### END GAZ PAGE ###




### SALARIES PAGE ###
@admin.route('/salaries')
def salaries():

    return render_template('admin/salaries.html')

@admin.route('/update_salaries',methods=['POST'])
def update_salaries():
    try:
        cursor = connection.cursor()

        # Fetch data from the form
        employee_id = request.form['employeeId']
        cell_index = request.form['cellIndex']
        new_value = request.form['newValue']

        # Determine which column to update based on the cell index
        columns = ['employe_id', 'name', 'department', 'job_role', 'net_salary', 'allowance']
        column_to_update = columns[int(cell_index)]

        # Prepare and execute the SQL UPDATE statement
        sql = f"UPDATE salaries SET {column_to_update} = ? WHERE employe_id = ?"
        cursor.execute(sql, (new_value, employee_id))
        connection.commit()

        flash('Employe Updated successfully!', 'success') 
    except Exception as e:
        connection.rollback()
        return f"Error: {e}"
    finally:
        cursor.close()
    
        return redirect(url_for('admin.head_salaries'))

@admin.route('/head_salaries')
def head_salaries():
    # connect_to_zkteco()
    # month_report()
    cursor.execute(""" 
            select employe_id , name , department , job_role , net_salary  ,
                   allowance , total_net from salaries 
            """)
    results = cursor.fetchall()
    return render_template('admin/head_salaries.html',results=results)


@admin.route('/month_salary')
def month_salary():
    return render_template('admin/month_salary.html')



### END SALARIES PAGE ###
