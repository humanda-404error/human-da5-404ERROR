use prj_404error;
select *from weather;

SELECT COUNT(*) 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'prj_404error' 
  AND TABLE_NAME = 'population';
  
describe population;
describe weather;


select *from population;
select *from weather;

show table status like 'population';

truncate table population;
truncate table weather;

ALTER TABLE population
CHANGE COLUMN 자치구명 자치구 VARCHAR(20);