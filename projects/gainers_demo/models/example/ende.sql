{{ config(materialized='table') }}

SELECT EN,DE
FROM DATA_SCIENCE.NRG6CB_RAW.NUMBERS
