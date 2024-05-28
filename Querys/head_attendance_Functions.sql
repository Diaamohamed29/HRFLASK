

CREATE PROCEDURE InsertValuesIntoHeadAttendance
(
    @start_date DATE,
    @end_date DATE
)
AS
BEGIN
    -- Delete existing data from head_attendance table within the specified date range
    DELETE FROM head_attendance
    
    
    -- Insert values into the head_attendance table for each employee and date
    INSERT INTO head_attendance (employe_id, name, job_role, date, day, check_in, check_out, check_in_per, check_out_per, extra_hours)
    SELECT 
        e.employe_id,
        e.name,
        e.job_role,
        c.date,
        c.day_name,
        z.check_in,
        z.check_out,
        z.check_in_per,
        z.check_out_per,
        CONVERT(DECIMAL(5,2), z.extra_minutes / 60.0)
    FROM 
        employes e
    CROSS JOIN 
        calendar c
    LEFT JOIN
        zktecoAll z ON e.employe_id = z.employe_id AND c.date = z.Date
    WHERE 
        c.date BETWEEN @start_date AND @end_date;
	  -- Add a row for each employee with total values
    INSERT INTO head_attendance (employe_id, name, job_role, date, day, check_in, check_out, check_in_per, check_out_per, extra_hours,check_vacation,check_mission,check_per,check_extra_day)
    SELECT 
        employe_id,
        'Total', -- Placeholder for name (you can adjust this according to your requirements)
        'Total', -- Placeholder for job_role
        NULL, -- NULL date since this represents the total row
        NULL, -- NULL day since this represents the total row
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
		NULL,
		NULL,
		NULL,
		NULL
    FROM 
        head_attendance
    WHERE 
        date BETWEEN @start_date AND @end_date
    GROUP BY 
        employe_id;
	update head_attendance 
	set extra_hours = 0 
	where extra_hours is NULL and name != 'Total'
END;






CREATE PROCEDURE UpdateMissionsInHeadAttendance
AS
BEGIN
    UPDATE ha
    SET ha.check_mission = ISNULL(m.status, 0)
    FROM head_attendance ha
    LEFT JOIN missions m ON ha.employe_id = m.employe_id AND ha.date = m.date
    WHERE ha.name != 'Total';
END;



CREATE PROCEDURE UpdateVacationRequestsInHeadAttendance
AS
BEGIN
    -- Update check_vacation in head_attendance table based on vacation_requests table
    UPDATE head_attendance
    SET check_vacation = 1
    FROM head_attendance ha
    JOIN vacation_requests vr ON ha.employe_id = vr.employe_id AND ha.date BETWEEN vr.from_date AND vr.to_date
    WHERE ha.name != 'Total';
END;



CREATE PROCEDURE UpdateExtraDaysInHeadAttendance
AS
BEGIN
    -- Update check_extra_day in head_attendance table based on month_extra_days table
    UPDATE head_attendance
    SET head_attendance.check_extra_day = month_extra_days.status
    FROM head_attendance
    JOIN month_extra_days ON head_attendance.date = month_extra_days.date
                          AND head_attendance.employe_id = month_extra_days.employe_id
    WHERE head_attendance.name != 'Total';
END;


CREATE PROCEDURE UpdateCheckPerInHeadAttendance
AS
BEGIN
    -- First update the check_per based on the conditions
    UPDATE head_attendance 
    SET check_per = 
        CASE 
            WHEN check_mission = 0 AND check_vacation = 0 AND check_out_per = 0 AND check_extra_day = 0 AND name != 'total' THEN check_in_per
            WHEN check_mission = 0 AND check_vacation = 0 AND check_in_per = 0 AND check_extra_day = 0 AND name != 'total' THEN check_out_per
            ELSE 0
        END
    WHERE name != 'Total';
END;

CREATE PROCEDURE UpdateTotalRowsInHeadAttendance
AS
BEGIN
    -- Update the "Total" rows in head_attendance
    UPDATE ha
    SET 
        check_per = 
            CASE 
                WHEN total.check_per <= 4 THEN 0
                ELSE (total.check_per - 4) * 0.25
            END,
        check_vacation = ISNULL(total.check_vacation, 0),
        check_mission = ISNULL(total.check_mission, 0),
        extra_hours = ISNULL(total.extra_hours, 0),
        check_extra_day = ISNULL(total.check_extra_day, 0)
    FROM head_attendance ha
    INNER JOIN (
        SELECT employe_id,
               SUM(check_vacation) AS check_vacation,
               SUM(check_mission) AS check_mission,
               SUM(check_per) AS check_per,
               SUM(extra_hours) AS extra_hours,
               SUM(check_extra_day) AS check_extra_day
        FROM head_attendance
        WHERE name != 'Total'
        GROUP BY employe_id
    ) AS total ON ha.employe_id = total.employe_id
    WHERE ha.name = 'Total';
END;

