

------------ WORKING SELECTION PAST WEEK From MONDAY to SUNDAY -----------------

select * from learn where 
date_added < DATE_TRUNC('week', NOW())
    AND
date_added >= DATE_TRUNC('week', NOW()) - interval '7 day' 

order by date_added;

