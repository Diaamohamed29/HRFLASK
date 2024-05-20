import pyodbc
from zk import ZK , const 
import pandas as pd 
from sqlalchemy import create_engine
from datetime import datetime , timedelta
connection = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-6RVJEGB;DATABASE=HR;Trusted_Connection=yes;')
cursor = connection.cursor()


def connect_to_zkteco():
    

    



    DB = {'servername':'DESKTOP-6RVJEGB',
            'database':'HR',
            'driver':'driver=SQL Server Native Client 11.0'}

    engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])
    conn = None

    zk = ZK('192.168.1.208', port=4370, timeout=5)
    print ('Connecting to device ...')

    zk_conn = zk.connect()
    users = zk_conn.get_users()

    user_info_list = [(user.uid, user.name) for user in users]
    users_df = pd.DataFrame(user_info_list,columns=['userid','name'])
    users_df.to_sql('users',index=False,con=engine,if_exists='replace')


    attendances = zk_conn.get_attendance()
    attendance_info_list = [(att.user_id, att.timestamp) for att in attendances]

    attendance_df = pd.DataFrame(attendance_info_list, columns=['userid', 'date_time'])
    attendance_df['date_time'] = pd.to_datetime(attendance_df['date_time'])
    attendance_df['Date'] = pd.to_datetime(attendance_df['date_time']).dt.date
    attendance_df['Time'] = pd.to_datetime(attendance_df['date_time']).dt.strftime('%H:%M')


    attendance_df.drop(columns=['date_time'], inplace=True)

    # Group by userid and date, and aggregate the min and max of Time
    check_in_out_df = attendance_df.groupby(['userid', 'Date']).agg(check_in=pd.NamedAgg(column='Time', aggfunc='min'),
                                                                check_out=pd.NamedAgg(column='Time', aggfunc='max')).reset_index()
    check_in_out_df.to_sql('zktecoAll',index=False,con=engine,if_exists='replace')


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
            WHEN CAST(check_in AS TIME) BETWEEN '01:00:00' AND '09:16:00' THEN 0
            WHEN CAST(check_in AS TIME) BETWEEN '09:16:00' AND '10:00:00' THEN 1
            WHEN CAST(check_in AS TIME) BETWEEN '10:01:00' AND '11:00:00' THEN 2
            WHEN CAST(check_in AS TIME) BETWEEN '11:01:00' AND '12:00:00' THEN 3
            WHEN CAST(check_in AS TIME) BETWEEN '12:01:00' AND '13:00:00' THEN 4
            ELSE 0
        END;

        """)
    connection.commit()

    cursor.execute(""" 


        UPDATE zktecoAll
        SET check_out_per = CASE
            WHEN CAST(check_out AS TIME) BETWEEN '16:59:00' and '23:59:00' THEN 0
            WHEN CAST(check_out AS TIME) BETWEEN '16:01:00' AND '17:00:00' THEN 1
            WHEN CAST(check_out AS TIME) BETWEEN '15:01:00' AND '16:00:00' THEN 2
            WHEN CAST(check_out AS TIME) BETWEEN '14:01:00' AND '15:00:00' THEN 3
            WHEN CAST(check_out AS TIME) BETWEEN '13:01:00' AND '14:00:00' THEN 4
            
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
    SET 
        extra_minutes = CASE 
                        WHEN check_out BETWEEN '17:15:00' AND '23:59:00' THEN 
                            DATEDIFF(MINUTE, '17:00:00', CASE WHEN check_out < '23:59:00' THEN check_out ELSE '23:59:00' END) 
                        ELSE 
                            0 
                    END
        WHERE 
        check_out IS NOT NULL;

    """)
    connection.commit()
    # cursor.execute(""" 
    #                 UPDATE month_report
    #     SET 
    #         check_in = z.check_in,
    #         check_out = z.check_out,
    #         check_in_per = z.check_in_per,
    #         check_out_per = z.check_out_per,
    #         check_extra_minutes = z.extra_minutes
            
    #     FROM month_report mr
    #     INNER JOIN zktecoAll z ON mr.employe_id = z.employe_id AND mr.date = z.date

    #         """)
    # connection.commit()

    # cursor.execute(""" 
            
    #         UPDATE mr
    #             SET 
    #                 mr.check_mission = m.status,
    #                 mr.check_vacation = CASE WHEN vr.employe_id IS NOT NULL THEN 1 ELSE 0 END,
    #                 mr.check_per = CASE 
    #                                     WHEN mr.check_in_per <> 0 AND mr.check_out_per = 0 AND mr.check_mission = 0 AND mr.check_vacation = 0 
    #                                     THEN mr.check_in_per
    #                                     ELSE mr.check_per
    #                                 END
    #             FROM month_report mr
    #             LEFT JOIN missions m ON mr.employe_id = m.employe_id AND mr.date = m.date
    #             LEFT JOIN vacation_requests vr ON mr.employe_id = vr.employe_id AND mr.date BETWEEN vr.from_date AND vr.to_date;

    #             """)
    # connection.commit()






def current_month_report():
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
        
    cursor.execute(""" 
    DELETE FROM current_month_report
    """)
    connection.commit()

    cursor.execute(""" 
    INSERT INTO current_month_report (employe_id, name, date, day, check_in, check_out,
                                        total_extra, check_vacation, check_mission,
                                        check_per)
    SELECT employe_id, name, date, day,
            check_in, check_out, total_extra,
            check_vacation, check_mission, check_per
    FROM month_report 
    WHERE date BETWEEN ? AND ?
    """, (start_date, end_date))
    connection.commit()

    
    cursor.execute(""" 
                    
    UPDATE cmr
    SET cmr.check_per = CASE
                            WHEN cmr.check_vacation = 1 OR cmr.check_mission = 1 THEN 0
                            WHEN mr.check_in_per <> 0 AND cmr.check_mission = 0 AND cmr.check_vacation = 0 THEN mr.check_in_per
                            ELSE cmr.check_per
                        END
    FROM current_month_report cmr
    
    INNER JOIN month_report mr ON cmr.employe_id = mr.employe_id AND cmr.date = mr.date;
                   
                   """)
    connection.commit()



    cursor.execute(""" 
                   
UPDATE md
SET late = CASE
               WHEN i.check_per_sum < 4 THEN 0
               ELSE (i.check_per_sum - 4) * 0.25
           END
FROM month_deductions md
JOIN (
    SELECT employe_id, SUM(check_per) AS check_per_sum
    FROM current_month_report
    GROUP BY employe_id
) AS i ON md.employe_id = i.employe_id;


                   
                   """)
    connection.commit()







def update_month_report():
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
    cursor.execute("EXEC InsertIntoMonthReportFromZktecoAll")
    cursor.execute("EXEC UpdateNameAndDayInMonthReport")
    cursor.execute("EXEC UpdateMissionsInMonthReport")
    cursor.execute("EXEC UpdateVacationRequestsInMonthReport")
    cursor.execute("EXEC InsertValuesIntoCurrentMonthReport ?, ?", start_date, end_date)

    connection.commit()
    


# update_month_report()
connect_to_zkteco()