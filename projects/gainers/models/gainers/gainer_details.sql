{{ config(
	materialized='incremental',
) }}

select *
from {{ ref('gainer_details_seed')}}
