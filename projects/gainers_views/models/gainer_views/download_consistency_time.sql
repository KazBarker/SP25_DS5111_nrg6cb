with source_downloads as (
	select source as gainer_source, date_time
	from {{ source('snowflake', 'snowflake_gainer_details') }}
	group by gainer_source, date_time
),
load_times as (
	select time, date_time 
	from {{ source('snowflake', 'snowflake_downloads') }}
	group by time, date_time
),	
incomplete_output as (
	select ll.time, ss.gainer_source, count(*) as counts
	from source_downloads ss
	join load_times ll
	on ss.date_time = ll.date_time
	group by ll.time, ss.gainer_source
	order by ll.time
),
max_downloads as (
	select time, max(counts) as max_counts
	from incomplete_output
	group by time
)

select oo.time, oo.gainer_source, oo.counts / mm.max_counts as proportion_successful, oo.counts as total_downloads 
from incomplete_output as oo
join max_downloads mm
on oo.time = mm.time
order by oo.time, proportion_successful desc
