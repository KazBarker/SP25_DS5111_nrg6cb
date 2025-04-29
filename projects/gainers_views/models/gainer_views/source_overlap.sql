with total_daily as (
	select date_time, source, count(*) as ticker_count
	from {{ source('snowflake', 'snowflake_gainer_details') }}
	group by date_time, source
),
overlapping as (
	select date_time, symbol
	from {{ source('snowflake', 'snowflake_gainer_details') }}
	group by date_time, symbol
	having count(*) > 1
),
only_overlapping as (
	select tt.date_time, tt.source, tt.symbol
	from {{ source('snowflake', 'snowflake_gainer_details') }} tt
	join overlapping oo
	on tt.date_time = oo.date_time
	and tt.symbol = oo.symbol
),
overlapping_daily as (
	select date_time, source, count(*) as overlapping_ticker_count
	from only_overlapping
	group by date_time, source
)

select tt.source, avg(oo.overlapping_ticker_count / tt.ticker_count) as avg_proportion_overlapping
from total_daily tt
join overlapping_daily oo
on tt.date_time = oo.date_time
and tt.source = oo.source
group by tt.source
