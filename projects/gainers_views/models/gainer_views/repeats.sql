select source, symbol, count(*) as counts
from {{ source('snowflake', 'snowflake_gainer_details') }}
group by source, symbol
order by counts desc
