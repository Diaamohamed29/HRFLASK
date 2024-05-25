
-- user table that contain login credintials 
create table user_(username nvarchar(max) ,
 password nvarchar(max))


 -- employes table 
create table employes(employe_id int ,
name nvarchar(max) ,
department nvarchar(max), 
job_role nvarchar(max) ,
net_salary real  , 
allowance real ,
hire_date date ,
telephone nvarchar(max),
qualification nvarchar(max) ,
national_id nvarchar(max) ,
address nvarchar(max),
social_insurance real )

-- vacations table 
create table vacations (employe_id int , 
name nvarchar(max) , 
normal_days decimal (10, 2) ,
casual_days decimal (10, 2) ,
total_days as (normal_days + casual_days))


-- missions table 


create table missions( employe_id int ,
 name nvarchar(max) ,
 job_role nvarchar(max),
  date date , 
  from_time time , 
  to_time time , 
  reason nvarchar(max),
  status int)


-- salaries table 
create table salaries(employe_id int , 
name nvarchar(max)  ,
department nvarchar(max) , 					
job_role nvarchar(max) , 
net_salary real , 
daily_salary as (net_salary / 30) ,
allowance real ,					    
total_net_salary as(net_salary + allowance)
)


-- vacations requests table 
create table vacation_requests(employe_id int ,

 name nvarchar(max) , 
 department nvarchar(max) , 
 job_role nvarchar(max) , 
 date date , 
 from_date date ,
 to_date date , 
 no_of_days decimal(10,2),
 vac_type nvarchar(max),
 status int)


-- month report table 
create table month_report(employe_id int ,
name nvarchar(max) , 
date date ,
day varchar(50) ,
check_in time ,
check_out time ,
check_in_per int DEFAULT 0 ,
check_out_per int DEFAULT 0 ,
check_extra_hours int DEFAULT 0 ,
check_extra_minutes int DEFAULT 0 ,
total_extra AS (
        CAST(
            CASE 
                WHEN check_extra_minutes >= 60 THEN check_extra_minutes / 60.0
                ELSE check_extra_minutes * 1.0 / 60
            END AS DECIMAL(10,2)
			)),
check_vacation int DEFAULT 0 ,
check_mission int DEFAULT 0,
check_per int DEFAULT 0 ) ;




-- month dedcutions table 
create table month_deductions (employe_id int ,
name nvarchar(max) , 
deduction_days decimal(10,2) default 0 ,
vacation_days decimal(10,2) default 0 , 
absent_days decimal(10,2) default 0 ,
late decimal(10,2) default 0 , 
total_deduction as (deduction_days + vacation_days + absent_days + late),

)



-- month administrative table
create table month_administrative (employe_id int ,
name nvarchar(max) , 
admin_absent_value real default 0 , 
admin_pen int default 0 , 
admin_per_value real default 0 , 
deductions real default 0 
)


-- month extra hours table
create table month_extra_hours(employe_id int , 
net_salary real , 
allowance real , 
daily_salary real ,
hourly_salary as (daily_salary / 8),
extra_hours real , 
extra_hours_rate decimal (10,2) default 1.2 , 
)




-- current_month function and table

CREATE FUNCTION dbo.GetCheckPerSum(@employe_id INT)
RETURNS INT
AS
BEGIN
    DECLARE @sum INT;

    SELECT @sum = SUM(check_per)
    FROM current_month_report
    WHERE employe_id = @employe_id;

    RETURN @sum;
END;
CREATE TABLE current_month_report (
    employe_id INT,
    name NVARCHAR(MAX),
    date DATE,
    day NVARCHAR(MAX),
    check_in TIME,
    check_out TIME,
    total_extra DECIMAL(10, 2) DEFAULT 0,
    check_vacation INT DEFAULT 0,
    check_mission INT DEFAULT 0,
    check_per INT DEFAULT 0,
    check_per_sum AS (dbo.GetCheckPerSum(employe_id))
);




-- calendar table 


CREATE TABLE  calendar (
    date DATE PRIMARY KEY,
    day_name NVARCHAR(MAX)
);

-- Generate and insert all the dates and day names for the year
WITH Dates_CTE AS (
    SELECT CAST('2024-01-01' AS DATE) AS date
    UNION ALL
    SELECT DATEADD(day, 1, date)
    FROM Dates_CTE
    WHERE date < '2027-01-01'
)
INSERT INTO calendar (date, day_name)
SELECT date, DATENAME(weekday, date) AS day_name
FROM Dates_CTE
OPTION (MAXRECURSION 0);




create table head_attendance (employe_id int , 
						name nvarchar(max) , 
						job_role nvarchar(max), 
						day nvarchar(max) , 
						date date , 
						check_in time , 
						check_out time , 
						check_in_per decimal (10,2) default 0,
						check_out_per decimal(10,2) default 0 , 
						extra_hours decimal (10,2) default 0 , 
						check_vacation decimal (10,2) default 0 , 
						check_mission decimal (10,2) default 0,
							check_per decimal (10,2) default 0)

create table head_payroll (employe_id int , 
							name nvarchar(max) , 
							job_role nvarchar(max) ,  
							net_salary real , 
							allowance real , 
							extra_hours decimal(10,2) default 0 ,
							extra_hours_value real , 
							total_salary real , 
							deduction_days int default 0 , 
							vacation_days int default 0 , 
							absent_days int default 0,
							late decimal (10,2) default 0 ,
							total_deduction decimal (10,2) default 0 , 
							total_deduction_value real default 0 ,
							total_net real , 
							administrative_absent_value real default 0 , 
							administrative_pen int default 0  , 
							administrative_pen_value real default 0 , 
							deductions real default 0 , 
							loans real default 0, 
							social_insurance real default 0 , 
							labor_box real default 0, 
							suspended real default 0,
							total_net_salary real , 
							payment_way nvarchar(max) )
							 


create table month_loans_insurance (employe_id int , 
									name nvarchar(max) , 
									loans real default 0 , 
									social_insurance real default 0 , 
									labor_box real default 0,
									suspended real default 0 )
