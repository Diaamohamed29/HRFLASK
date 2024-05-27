import pyodbc
from zk import ZK, const
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from zk.exception import ZKNetworkError

connection = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-P1V3K1G;DATABASE=HR;Trusted_Connection=yes;')
cursor = connection.cursor()

def connect_to_zkteco():
    try:
        DB = {'servername': 'DESKTOP-P1V3K1G', 'database': 'HR', 'driver': 'driver=SQL Server Native Client 11.0'}
        engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])
        
        zk = ZK('192.168.1.208', port=4370, timeout=5)
        print('Connecting to device ...')
        
        zk_conn = zk.connect()
        users = zk_conn.get_users()

        user_info_list = [(user.uid, user.name) for user in users]
        users_df = pd.DataFrame(user_info_list, columns=['userid', 'name'])
        users_df.to_sql('users', index=False, con=engine, if_exists='replace')

        attendances = zk_conn.get_attendance()
        attendance_info_list = [(att.user_id, att.timestamp) for att in attendances]

        attendance_df = pd.DataFrame(attendance_info_list, columns=['userid', 'date_time'])
        attendance_df['date_time'] = pd.to_datetime(attendance_df['date_time'])
        attendance_df['Date'] = pd.to_datetime(attendance_df['date_time']).dt.date
        attendance_df['Time'] = pd.to_datetime(attendance_df['date_time']).dt.strftime('%H:%M')

        attendance_df.drop(columns=['date_time'], inplace=True)

        check_in_out_df = attendance_df.groupby(['userid', 'Date']).agg(
            check_in=pd.NamedAgg(column='Time', aggfunc='min'),
            check_out=pd.NamedAgg(column='Time', aggfunc='max')
        ).reset_index()
        check_in_out_df.to_sql('zktecoAll', index=False, con=engine, if_exists='replace')

        cursor.execute(""" 
        IF NOT EXISTS (
            SELECT *
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'zktecoAll' AND COLUMN_NAME = 'day'
        )
        BEGIN
            ALTER TABLE zktecoAll
            ADD day varchar(max);
        END;
        """)
        connection.commit()

        cursor.execute(""" 
        update zktecoAll
        set day = (select day_name from calendar where date = zktecoAll.Date)
        """)
        connection.commit()

        cursor.execute(""" 
        IF NOT EXISTS (
            SELECT *
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'zktecoAll' AND COLUMN_NAME = 'employe_id'
        )
        BEGIN
            ALTER TABLE zktecoAll
            ADD employe_id INT NULL;
        END;
        """)
        connection.commit()

        cursor.execute(""" 
        IF NOT EXISTS (
            SELECT *
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'zktecoAll' AND COLUMN_NAME = 'check_in_per'
        )
        BEGIN
            ALTER TABLE zktecoAll
            ADD check_in_per INT NULL;
        END;
        """)
        connection.commit()

        cursor.execute(""" 
        IF NOT EXISTS (
            SELECT *
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'zktecoAll' AND COLUMN_NAME = 'check_out_per'
        )
        BEGIN
            ALTER TABLE zktecoAll
            ADD check_out_per INT NULL;
        END;
        """)
        connection.commit()

        cursor.execute(""" 
        IF NOT EXISTS (
            SELECT *
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'zktecoAll' AND COLUMN_NAME = 'finger_miss'
        )
        BEGIN
            ALTER TABLE zktecoAll
            ADD finger_miss INT NULL;
        END;
        """)
        connection.commit()

        cursor.execute(""" 
        IF NOT EXISTS (
            SELECT *
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'zktecoAll' AND COLUMN_NAME = 'extra_minutes'
        )
        BEGIN
            ALTER TABLE zktecoAll
            ADD extra_minutes INT NULL;
        END;
        """)
        connection.commit()

        cursor.execute(""" 
        update zktecoAll 
        set employe_id = (Select name from users where userid = zktecoAll.userid)
        """)
        connection.commit()

        cursor.execute(""" 
        UPDATE zktecoAll
        SET check_in_per = CASE
            WHEN CAST(check_in AS TIME) BETWEEN '01:00:00' AND '09:16:00' and day!='Friday' and day!='Saturday' THEN 0
            WHEN CAST(check_in AS TIME) BETWEEN '09:16:00' AND '10:00:00' and day!='Friday' and day!='Saturday' THEN 1
            WHEN CAST(check_in AS TIME) BETWEEN '10:01:00' AND '11:00:00' and day!='Friday' and day!='Saturday' THEN 2
            WHEN CAST(check_in AS TIME) BETWEEN '11:01:00' AND '12:00:00' and day!='Friday' and day!='Saturday' THEN 3
            WHEN CAST(check_in AS TIME) BETWEEN '12:01:00' AND '13:00:00' and day!='Friday' and day!='Saturday'  THEN 4
            ELSE 0
        END;
        """)
        connection.commit()

        cursor.execute(""" 
        UPDATE zktecoAll
        SET check_out_per = CASE
            WHEN CAST(check_out AS TIME) BETWEEN '16:59:00' and '23:59:00' and day!='Friday' and day!='Saturday' THEN 0
            WHEN CAST(check_out AS TIME) BETWEEN '16:01:00' AND '17:00:00' and day!='Friday' and day!='Saturday' THEN 1
            WHEN CAST(check_out AS TIME) BETWEEN '15:01:00' AND '16:00:00' and day!='Friday' and day!='Saturday' THEN 2
            WHEN CAST(check_out AS TIME) BETWEEN '14:01:00' AND '15:00:00' and day!='Friday' and day!='Saturday' THEN 3
            WHEN CAST(check_out AS TIME) BETWEEN '13:01:00' AND '14:00:00' and day!='Friday' and day!='Saturday' THEN 4
            ELSE 0
        END;
        """)
        connection.commit()

        cursor.execute(""" 
        update zktecoAll 
        set finger_miss = CASE
            WHEN check_in = check_out then 1
            ELSE 0
        END;
        """)
        connection.commit()

        cursor.execute(""" 
        UPDATE zktecoAll
        SET extra_minutes = 
            CASE 
                WHEN employe_id IN (146, 120, 507, 498) and day != 'Friday' and day != 'Saturday' THEN
                    CASE 
                        WHEN check_out BETWEEN '17:15:00' AND '23:59:00' THEN DATEDIFF(MINUTE, '17:00:00', check_out)
                        ELSE 0
                    END
                WHEN employe_id IN (273, 470) and day != 'Friday' and day != 'Saturday' THEN
                    CASE 
                        WHEN check_out BETWEEN '18:00:00' AND '23:59:00' THEN DATEDIFF(MINUTE, '17:00:00', check_out)
                        ELSE 0
                    END
                ELSE 0
            END
        WHERE check_out IS NOT NULL;
        """)
        connection.commit()

    except ZKNetworkError as e:
        raise ZKNetworkError(f"Can't reach device: {str(e)}")

def head_attendance():


    # Get current date and time
    current_datetime = datetime.now()

    # Extract current year, month, and day
    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day

    # Set start date to the 26th of the previous month
    start_date = datetime(current_year, current_month, 26) - timedelta(days=30)

    # Set end date to the 25th of the current month
    end_date = datetime(current_year, current_month, 25)

# Adjust start and end dates if the current day is after the 25th
    if current_day >= 26:
        start_date = datetime(current_year, current_month, 26)
        end_date = start_date + timedelta(days=30)

    cursor.execute("EXEC InsertValuesIntoHeadAttendance ?, ?",(start_date,end_date))
    cursor.execute("EXEC UpdateVacationRequestsInHeadAttendance")
    cursor.execute("EXEC UpdateMissionsInHeadAttendance")
    # cursor.execute("EXEC UpdateExtraDaysInHeadAttendance")
    # cursor.execute("EXEC UpdateCheckPerInHeadAttendance")

    connection.commit()


def head_payroll():
    cursor.execute("EXEC InsertIntoHeadPayroll")
    cursor.execute("EXEC UpdateExtraHoursInHeadPayroll")
    cursor.execute("EXEC UpdateExtraHoursValueInHeadPayroll")
    cursor.execute("EXEC UpdateHeadPayroll")


    connection.commit()


# connect_to_zkteco()
# head_attendance()
# head_payroll()

