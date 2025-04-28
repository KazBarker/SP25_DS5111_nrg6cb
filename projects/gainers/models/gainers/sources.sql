{{ config(
	materialized='incremental',
	unique_key='source'
) }}

select distinct *
from {{ ref('sources_seed')}}

{% if is_incremental() %}
where source not in (select source from {{ this }})
{% endif %}
