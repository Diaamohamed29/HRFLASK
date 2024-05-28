

-- DELETE TIRGGER FOR EMPLOYES TABLE --

CREATE TRIGGER trg_delete_employe
ON employes
AFTER DELETE
AS
BEGIN
    -- Delete from vacations table
    DELETE FROM vacations
    WHERE employe_id IN (SELECT employe_id FROM deleted);
	-- DELETE from missions 
	DELETE from missions 
	where employe_id in (select employe_id from deleted);

	-- DELETE from vacation requests table 
	delete from vacation_requests 
	where employe_id in (select employe_id from deleted);

    -- Delete from salaries table
    DELETE FROM salaries
    WHERE employe_id IN (SELECT employe_id FROM deleted);


	-- Delete from month_deductions 
	DELETE FROM month_deductions 
	where employe_id in (select employe_id from deleted);


	-- Delete from month_administrative
	DELETE FROM month_administrative
	where employe_id in (select employe_id from deleted);

	-- DELETE from month_loans_insurance 
	DELETE FROM month_loans_insurance 
	where employe_id in (select employe_id from deleted);







END;

GO














CREATE TRIGGER trg_insert_employe
ON employes
AFTER INSERT
AS
BEGIN
IF EXISTS (SELECT 1 FROM employes e WHERE e.employe_id IN (SELECT employe_id FROM inserted))
    -- Insert into vacations table
    INSERT INTO vacations (employe_id, name)
    SELECT employe_id, name FROM inserted;
    
	-- insert into user_ table 
	INSERT INTO user_(username) 
	SELECT employe_id from inserted ;

    -- Insert into salaries table
    INSERT INTO salaries (employe_id, name, department, job_role, net_salary, allowance)
    SELECT employe_id, name, department, job_role, net_salary, allowance FROM inserted;


	-- insert into month_administrative
	insert into month_administrative (employe_id ,name)
	select employe_id,name from inserted ; 

	-- insert into month_deduction 
	insert into month_deductions (employe_id,name) 
	select employe_id,name from inserted ;

	
	-- insert into month_loans_insurance table 
	insert into month_loans_insurance (employe_id,name,social_insurance) 
	select employe_id,name,social_insurance from inserted ;




END;

GO


CREATE TRIGGER updateVacationsDays 
on vacation_requests
AFTER INSERT, UPDATE
AS
BEGIN
    -- Update for new inserts
    IF EXISTS (SELECT 1 FROM INSERTED WHERE status = 1)
    BEGIN
        UPDATE v
        SET 
            v.normal_days = v.normal_days - ISNULL(avd.used_normal_days, 0),
            v.casual_days = v.casual_days - ISNULL(avd.used_casual_days, 0)
        FROM 
            vacations v
        INNER JOIN 
            (
                SELECT 
                    employe_id,
                    SUM(CASE WHEN vac_type = 'normal' THEN no_of_days ELSE 0 END) AS used_normal_days,
                    SUM(CASE WHEN vac_type = 'casual' THEN no_of_days ELSE 0 END) AS used_casual_days
                FROM 
                    INSERTED
                WHERE 
                    status = 1
                GROUP BY 
                    employe_id
            ) AS avd ON v.employe_id = avd.employe_id;
    END

END;






















