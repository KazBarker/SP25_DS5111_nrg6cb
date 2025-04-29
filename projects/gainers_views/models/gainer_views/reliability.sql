with source_downloads as (
	select source, date_time
	from {{ source('snowflake', 'snowflake_gainer_details') }}
	group by source, date_time
),
download_counts as (
	select source, count(*) as download_count
	from source_downloads
	group by source
),
max_downloads as (
	select max(download_count) as max_downloads
	from download_counts
)

select
cc.source, cc.download_count, cc.download_count / mm.max_downloads as reliability_score
from download_counts cc
cross join max_downloads mm
