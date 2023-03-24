

------------ WORKING SELECTION PAST WEEK From MONDAY to SUNDAY -----------------

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



