

create table month_report (employe_id int , 
							name nvarchar(max) , 
							department nvarchar(max) , 
							job_role nvarchar(max) , 
							day nvarchar(max) , 
							date date , 
							check_in time , 
							check_out time , 
							check_in_per decimal(10,2) default 0 ,
							check_out_per decimal(10,2) default 0 , 
							check_per int default 0 ,
							extra_hours decimal(10,2) default 0 , 
							check_vacation int default 0 , 
							check_mission int default 0 




CREATE PROCEDURE InsertValuesIntoMonthReport
(
    @start_date DATE,
    @end_date DATE
)
AS
BEGIN
    BEGIN TRY
        -- Start a transaction
        BEGIN TRANSACTION;

        -- Delete existing data from month_report table within the specified date range
        DELETE FROM month_report
        WHERE date BETWEEN @start_date AND @end_date;

        -- Insert values into the month_report table
        INSERT INTO month_report (employe_id, date, check_in, check_out, check_in_per, check_out_per)
        SELECT 
            employe_id, date, check_in, check_out, check_in_per, check_out_per
        FROM 
            zktecoAll
        WHERE 
            date BETWEEN @start_date AND @end_date;

        -- Update the extra_hours column in month_report
        UPDATE month_report
        SET extra_hours = (SELECT SUM(extra_minutes) / 60 FROM zktecoAll WHERE employe_id = month_report.employe_id AND date BETWEEN @start_date AND @end_date);

        -- Update name, department, job_role, and day columns using subqueries
        UPDATE month_report
        SET 
            name = (SELECT name FROM employes WHERE employe_id = month_report.employe_id),
            department = (SELECT department FROM employes WHERE employe_id = month_report.employe_id),
            job_role = (SELECT job_role FROM employes WHERE employe_id = month_report.employe_id),
            day = (SELECT day_name FROM calendar WHERE date = month_report.date)
        WHERE 
            date BETWEEN @start_date AND @end_date;

        -- Commit the transaction
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        -- If an error occurs, roll back the transaction
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        -- Handle the error (you can log it, raise it, or do any other appropriate action)
        THROW;
    END CATCH;
END;


