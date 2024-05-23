









-- head office attendance functions 




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
        zktecoAll z ON e.employe_id = z.employe_id AND c.date = z.date
    WHERE 
        c.date BETWEEN @start_date AND @end_date;
	  -- Add a row for each employee with total values
    INSERT INTO head_attendance (employe_id, name, job_role, date, day, check_in, check_out, check_in_per, check_out_per, extra_hours,check_vacation,check_mission,check_per)
    SELECT 
        employe_id,
        'Total', -- Placeholder for name (you can adjust this according to your requirements)
        'Total', -- Placeholder for job_role
        NULL, -- NULL date since this represents the total row
        NULL, -- NULL day since this represents the total row
        NULL,
        NULL,
        SUM(check_in_per),
        SUM(check_out_per),
        SUM(extra_hours),
		SUM(check_vacation),
		SUM(check_mission),
		SUM(check_per) 
    FROM 
        head_attendance
    WHERE 
        date BETWEEN @start_date AND @end_date
    GROUP BY 
        employe_id;
	update head_attendance 
	set extra_hours = 0 
	where extra_hours is NULL
END;




CREATE PROCEDURE UpdateVacationRequestsInHeadAttendance
AS
BEGIN
    UPDATE head_attendance
    SET 
        check_vacation = 1
    FROM head_attendance ha
    JOIN vacation_requests vr ON ha.employe_id = vr.employe_id AND ha.date BETWEEN vr.from_date AND vr.to_date;
END;



CREATE PROCEDURE UpdateMissionsInHeadAttendance
AS
BEGIN
    UPDATE head_attendance
    SET 
        check_mission = ISNULL(m.status, 0)
    FROM head_attendance ha
    LEFT JOIN missions m ON ha.employe_id = m.employe_id AND ha.date = m.date;
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
        END;

    -- Then update the total rows with the sum of check_per
    UPDATE ha
    SET ha.check_per = totals.sum_check_per 
    FROM head_attendance ha
    INNER JOIN (
        SELECT employe_id, SUM(check_per) AS sum_check_per
        FROM head_attendance
        WHERE name != 'total' AND job_role != 'total'
        GROUP BY employe_id
    ) AS totals
    ON ha.employe_id = totals.employe_id
    WHERE ha.name = 'total' AND ha.job_role = 'total';
END;



-- payroll functions 

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



