
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
    -- Update the "extra_hours" column in head_payroll
    UPDATE hp
    SET 
        extra_hours = ha.extra_hours
    FROM head_payroll hp
    INNER JOIN head_attendance ha ON hp.employe_id = ha.employe_id
    WHERE ha.name = 'Total';
END;





CREATE PROCEDURE UpdateHeadPayrollExtra_days
AS
BEGIN 


update hp 
set extra_days = ha.check_extra_day 
from head_payroll hp 
INNER JOIN head_attendance ha on hp.employe_id = ha.employe_id 
where ha.name ='Total';
END;


















CREATE PROCEDURE UpdateExtraHoursValueInHeadPayroll
AS
BEGIN
	
    -- Update extra_hours_value
    UPDATE head_payroll 
    SET extra_hours_value = ((net_salary / 30) / 8) * 1.2 * extra_hours;

	-- Update extra_days_value 
	UPDATE head_payroll 
	set extra_days_value = (net_salary/30) * extra_days
    -- Update total_salary
    UPDATE head_payroll
    SET total_salary = net_salary + allowance + extra_hours_value;
END;




CREATE PROCEDURE UpdateHeadPayrollFromMonthDeductions
AS
BEGIN
  -- Update deduction_days, vacation_days, absent_days from month_deductions
    UPDATE hp
    SET 
        hp.deduction_days = md.deduction_days,
        hp.vacation_days = md.vacation_days,
        hp.absent_days = md.absent_days, 
		hp.late = md.late,
		hp.total_deduction = md.total_deduction
    FROM head_payroll hp
    JOIN month_deductions md ON hp.employe_id = md.employe_id;
     UPDATE head_payroll
    SET total_deduction_value = (net_salary / 30) * total_deduction;
	 UPDATE head_payroll
    SET total_net = total_salary - total_deduction_value;
END;





CREATE PROCEDURE UpdateHeadPayrollFromMonthAdministrative
AS
BEGIN
  -- Update deduction_days, vacation_days, absent_days from month_deductions
    UPDATE hp
    SET 
        hp.administrative_absent_value = md.admin_absent_value,
        hp.administrative_pen = md.admin_pen,
        hp.administrative_pen_value = md.admin_per_value, 
		hp.deductions = md.deductions
		
    FROM head_payroll hp
    JOIN month_administrative md ON hp.employe_id = md.employe_id;

END;


CREATE PROCEDURE UpdateHeadPayrollFromMonthLoansInsurance
AS
BEGIN
update hp 
set hp.loans = md.loans,
	hp.social_insurance = md.social_insurance,
	hp.labor_box = md.labor_box,
	hp.suspended = md.suspended
from head_payroll hp 
JOIN month_loans_insurance md on hp.employe_id = md.employe_id ;

END;





CREATE PROCEDURE UpdateHeadPayrollTotalSalary
AS 
BEGIN 
	-- update administrative_pen_value 
	update head_payroll 
	set administrative_pen_value = administrative_pen * (net_salary/30)

	update head_payroll 
	set total_net_salary = total_net - administrative_pen_value - deductions - loans - social_insurance - labor_box - suspended + extra_days_value

END;



