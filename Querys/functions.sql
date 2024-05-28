








-- payroll functions 


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
		hp.social_insurance = ISNULL(mli.social_insurance, 0) ,
		hp.labor_box = mli.labor_box ,
		hp.suspended = mli.suspended
		from head_payroll hp
		JOIN month_loans_insurance mli on hp.employe_id = mli.employe_id;




    -- Update late from head_attendance
		UPDATE hp
		SET hp.late = CASE 
						 WHEN ha.check_per >= 4 THEN (ha.check_per - 4) * 0.25
						 ELSE 0
					  END
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

	-- update administrative_pen_value 
	update head_payroll 
	set administrative_pen_value = administrative_pen * (net_salary/30)

	update head_payroll 
	set total_net_salary = total_net - administrative_pen_value - deductions - loans - social_insurance - labor_box - suspended



END;






