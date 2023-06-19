----------- INITIAL TABLE INSERT FIRST ROW -----------
INSERT INTO 
    learn (subject, duration, date_added, comment)
VALUES
    ('FLASK', 41 , '2023-04-3', 'Test Data' ),
    ('ML', 23 , '2023-04-4', 'test Data Ignore' ),
    ('SQL', 56 , '2023-04-5', 'No Cmment' ),
    ('PHP', 46 , '2023-04-6', 'No Cmment' ),
    ('CSS', 23 , '2023-04-7', 'No Cmment' ),
    ('HTML', 46 , '2023-04-8', 'No Cmment' ),
    ('POSTGRES', 46 , '2023-04-9', 'No Cmment' );



------------ WORKING SELECTION PAST WEEK From MONDAY to SUNDAY -----------------
----  'week' rounds down to that Monday's date

select *
from learn
where date_added < DATE_TRUNC('week', NOW())
    AND date_added >= DATE_TRUNC('week', NOW()) - interval '7 day'
order by date_added;
 
---------- GET THE SUM of HOURS FROM LAST WEEK WORK ----------------
select sum(duration) as DURATION_WEEK from learn where 
date_added < DATE_TRUNC('week', NOW())
    AND
date_added >= DATE_TRUNC('week', NOW()) - interval '7 day' 
;

--------- PERCENT COMPLETE 1020 minutes a week / 17 HOURS -----------

select date_added from learn order by date_added;

select date_added from  learn where date_added < DATE_TRUNC('week', now()) ORDER BY date_added; 

select date_added from  learn where date_added >= DATE_TRUNC('week', NOW()) - interval '7 day'
order by date_added ;

select date_added from learn where  date_added = DATE_TRUNC('week', NOW()) order by date_added;

SELECT DATE_TRUNC('week', TIMESTAMP '2017-03-17 02:09:30');



