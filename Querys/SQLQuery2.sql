delete from employes 


select * from employes
 


insert into [Professional_HR].dbo.employes (employe_id , name , department , job_role , net_salary , allowance,social_insurance)
select employe_id , name , department , job_role , net_salary , allowance,social_insurance from [HR].dbo.employes


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








drop month_loans_insurance




alter table month_loans_insurance 
add  labor_box real default 0


create table month_loans_insurance (employe_id int , 
									name nvarchar(max) , 
									loans real default 0 , 
									social_insurance real default 0 ,
									labor_box real default 0, 
									suspended real default 0 )


select * from head_payroll 



select * from month_deductions 


select * from month_loans_insurance 


select * from zktecoAll


select * from missions 

select * from employes 

select * from vacation_requests 
delete from vacation_requests 

select * from head_attendance where employe_id = 498
order by date ,employe_id 


where check_mission = 1 or check_vacation = 1


select * from month_administrative
select * from month_loans_insurance 

 
 select * from salaries 


CREATE PROCEDURE UpdateSocialInsuranceInHeadPayroll 
AS
BEGIN 
    UPDATE hp
    SET hp.social_insurance = ha.social_insurance
    FROM head_payroll hp
    INNER JOIN employes ha
    ON hp.employe_id = ha.employe_id
    
END;

CREATE PROCEDURE UpdateHeadPayroll
AS
BEGIN
    -- Update deduction_days, vacation_days, absent_days from month_deductions
    UPDATE hp
    SET 
        hp.deduction_days = md.deduction_days,
        hp.vacation_days = md.vacation_days,
        hp.absent_days = md.absent_days
    FROM head_payroll hp
    JOIN month_deductions md ON hp.employe_id = md.employe_id;

	-- Update admin_absent_value , admin_pen , admin_per_value , deductions from month_administrative
	update hp
	set hp.administrative_absent_value = ma.admin_absent_value,
		hp.administrative_pen = ma.admin_pen,
		hp.administrative_pen_value = ma.admin_per_value,
		hp.deductions = ma.deductions
		from head_payroll hp 
		JOIN month_administrative ma ON hp.employe_id = ma.employe_id;
	-- update loans , social_insurance , labor_box , suspended from month_loans_insurance 
	update hp 
	set hp.loans = mli.loans,
		hp.social_insurance = mli.social_insurance ,
		hp.labor_box = mli.labor_box ,
		hp.suspended = mli.suspended
		from head_payroll hp
		JOIN month_loans_insurance mli on hp.employe_id = mli.employe_id;




    -- Update late from head_attendance
    UPDATE hp
    SET hp.late = ha.check_per
    FROM head_payroll hp
    JOIN head_attendance ha ON hp.employe_id = ha.employe_id
    WHERE ha.name = 'Total';

    -- Ensure no NULL values in columns used for calculation
    UPDATE head_payroll
    SET 
        deduction_days = ISNULL(deduction_days, 0),
        vacation_days = ISNULL(vacation_days, 0),
        absent_days = ISNULL(absent_days, 0),
        late = ISNULL(late, 0);

    -- Update total_deduction
    UPDATE head_payroll
    SET total_deduction = deduction_days + vacation_days + absent_days + late;

    -- Update total_deduction_value
    UPDATE head_payroll
    SET total_deduction_value = (net_salary / 30) * total_deduction;

    -- Update total_net
    UPDATE head_payroll
    SET total_net = total_salary - total_deduction_value;





END;





 select * from head_payroll 
