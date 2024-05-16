import pyodbc
from zk import ZK , const 
import pandas as pd 
from sqlalchemy import create_engine

connection = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-RNTE44E;DATABASE=Professional_HR;Trusted_Connection=yes;')
cursor = connection.cursor()


def connect_to_zkteco():
    

    



    DB = {'servername':'DESKTOP-RNTE44E',
            'database':'Professional_HR',
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





connect_to_zkteco()