{{ config(unique_key='symbol') }}

select distinct *
from {{ ref('gainers_seed')}}

{% if is_incremental() %}
where symbol not in (select symbol from {{ this }})
{% endif %}
