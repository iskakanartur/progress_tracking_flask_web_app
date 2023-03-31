

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



