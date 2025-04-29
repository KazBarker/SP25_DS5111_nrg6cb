with unique_per_timestamp as (
	select date_time, symbol
	from {{ source('snowflake', 'snowflake_gainer_details') }}
	group by date_time, symbol
)

select symbol, count(*) as counts
from unique_per_timestamp
group by symbol
order by counts desc, symbol
