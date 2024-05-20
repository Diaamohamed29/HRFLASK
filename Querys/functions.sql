CREATE PROCEDURE InsertIntoMonthReportFromZktecoAll
AS
BEGIN
    INSERT INTO month_report (employe_id, date, check_in, check_out, check_in_per, check_out_per, check_extra_minutes)
    SELECT 
        z.employe_id, z.date, z.check_in, z.check_out, z.check_in_per, z.check_out_per, z.extra_minutes
    FROM 
        zktecoAll z
    WHERE NOT EXISTS (
        SELECT 1
        FROM month_report m
        WHERE m.employe_id = z.employe_id
        AND m.date = z.date
    );
END;




CREATE PROCEDURE UpdateNameAndDayInMonthReport
AS
BEGIN
    UPDATE month_report
    SET 
        month_report.name = employes.name,
        month_report.day = calendar.day_name
    FROM 
        month_report
    JOIN 
        employes ON month_report.employe_id = employes.employe_id
    JOIN 
        calendar ON month_report.date = calendar.date;
END;



CREATE PROCEDURE UpdateMissionsInMonthReport
AS
BEGIN
    UPDATE month_report
    SET 
        check_mission = ISNULL(m.status, 0)
    FROM month_report mr
    LEFT JOIN missions m ON mr.employe_id = m.employe_id AND mr.date = m.date;
END;




CREATE PROCEDURE UpdateVacationRequestsInMonthReport
AS
BEGIN
    UPDATE month_report
    SET 
        check_vacation = 1
    FROM month_report mr
    JOIN vacation_requests vr ON mr.employe_id = vr.employe_id AND mr.date BETWEEN vr.from_date AND vr.to_date;
END;



CREATE PROCEDURE InsertValuesIntoCurrentMonthReport
(
    @start_date DATE,
    @end_date DATE
)
AS
BEGIN
    -- Delete existing data from current_month_report table within the specified date range
    DELETE FROM current_month_report
    

    -- Insert values into the current_month_report table
    INSERT INTO current_month_report (employe_id, name, date, day, check_in, check_out, total_extra)
    SELECT 
        employe_id, name, date, day, check_in, check_out, total_extra
    FROM 
        month_report -- Replace YourSourceTable with the source table name containing the data to be inserted
    WHERE 
        date BETWEEN @start_date AND @end_date;
END;
