-- new comment
-- New: Simple extraction of source data
INSERT OVERWRITE TABLE tmp_simple_extract
SELECT 
  user_id,
  event_time
FROM ods_user_logs
WHERE to_date(event_time) = date_sub(current_date(), 1)
PARTITION (dt = date_sub(current_date(), 1));

