delete from employes 


select * from missions 


insert into [HR].dbo.employes (employe_id , name , department , job_role , net_salary , allowance)
select employe_id , name , department , job_role , net_salary , allowance from [HR_GPT].dbo.employees


drop table head_attendance 



create table head_attendance (employe_id int , 
						name nvarchar(max) , 
						job_role nvarchar(max), 
						day nvarchar(max) , 
						date date , 
						check_in time , 
						check_out time , 
						check_in_per decimal (10,2) default 0,
						check_out_per decimal(10,2) default 0 , 
						extra_hours decimal (5,2) default 0 , 
						check_vacation decimal (10,2) default 0 , 
						check_mission decimal (10,2) default 0,
						check_per decimal (10,2) default 0 )

drop table head_payroll 

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
							 




CREATE PROCEDURE InsertIntoHeadPayroll
AS
BEGIN
	delete from head_payroll
    INSERT INTO head_payroll (employe_id, name, job_role, net_salary, allowance)
    SELECT employe_id, name, job_role, net_salary, allowance
    FROM employes;
END;



CREATE PROCEDURE UpdateExtraHoursInHeadPayroll
AS
BEGIN
    -- Update extra_hours in head_payroll based on values from head_attendance where name = 'total'
    UPDATE hp
    SET hp.extra_hours = ha.extra_hours
    FROM head_payroll hp
    INNER JOIN head_attendance ha
    ON hp.employe_id = ha.employe_id
    WHERE ha.name = 'total';
END;

CREATE PROCEDURE UpdateExtraHoursValueInHeadPayroll
AS
BEGIN
    -- Update extra_hours_value
    UPDATE head_payroll 
    SET extra_hours_value = ((net_salary / 30) / 8) * 1.2 * extra_hours;

    -- Update total_salary
    UPDATE head_payroll
    SET total_salary = net_salary + allowance + extra_hours_value;
END;





select * from head_payroll 



select * from month_deductions 





select * from zktecoAll


select * from missions 

select * from employes 

select * from vacation_requests 
delete from vacation_requests 

select * from head_attendance where employe_id = 498
order by date ,employe_id 


where check_mission = 1 or check_vacation = 1


select * from month_administrative
 
