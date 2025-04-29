{{ config(unique_key='date_time') }}

select distinct *
from {{ ref('downloads_seed')}}

{% if is_incremental() %}
where date_time not in (select date_time from {{ this }})
{% endif %}
