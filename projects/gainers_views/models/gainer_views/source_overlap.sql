select date_time, source, count(*) as test_counts
from {{ source('snowflake', 'snowflake_gainer_details') }}
group by date_time, source
