with min_max as (
	select symbol, min(price) as min_price, max(price) as max_price
	from {{ source('snowflake', 'snowflake_gainer_details') }}
	group by symbol
)

select symbol, min_price, max_price, max_price - min_price as price_range
from min_max
order by price_range desc
