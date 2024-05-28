CREATE PROCEDURE UpdateLateColumnInMonthDeductions
AS
BEGIN
    -- Update the "late" column in month_deductions
    UPDATE md
    SET 
        late = ha.check_per
    FROM month_deductions md
    INNER JOIN head_attendance ha ON md.employe_id = ha.employe_id
    WHERE ha.name = 'Total';
END;