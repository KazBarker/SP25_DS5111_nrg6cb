{{ config(materialized='table') }}

SELECT EN,FR
FROM DATA_SCIENCE.NRG6CB_RAW.NUMBERS
