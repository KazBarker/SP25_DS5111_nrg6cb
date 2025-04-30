with source_downloads as (
	select source as gainer_source, date_time
	from {{ source('snowflake', 'snowflake_gainer_details') }}
	group by gainer_source, date_time
),
reformatted as (
	select date_time, to_timestamp(cast(date_time as string), 'YYYYMMDDHH24MI') as tstamp
	from {{ source('snowflake', 'snowflake_downloads') }}
),
load_days as (
	select date_time, tstamp, extract(dayofweek from tstamp) as weekday 
	from reformatted
	group by date_time, tstamp
),	
incomplete_output as (
	select ll.weekday, ss.gainer_source, count(*) as counts
	from source_downloads ss
	join load_days ll
	on ss.date_time = ll.date_time
	group by ll.weekday, ss.gainer_source
	order by ll.weekday
),
max_downloads as (
	select weekday, max(counts) as max_counts
	from incomplete_output
	group by weekday
)

select oo.weekday, oo.gainer_source, oo.counts / mm.max_counts as proportion_successful, oo.counts as total_downloads 
from incomplete_output as oo
join max_downloads mm
on oo.weekday = mm.weekday
order by oo.gainer_source, oo.weekday
