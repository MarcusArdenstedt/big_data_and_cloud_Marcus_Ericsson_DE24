WITH src_info AS (SELECT * FROM {{ ref('src_tvseries_info') }}),
src_serie AS (SELECT * FROM {{ ref('src_tvseries') }})

SELECT 
    {{dbt_utils.generate_surrogate_key(['se.name', 'sif.summary'])}} AS id_info,
    {{dbt_utils.generate_surrogate_key(['se.show_name', 'se.links_show'])}} AS id_serie,
    se.season,
    se.number,
    {{if_null('sif.airtime')}} AS "airtime",
    sif.airdate
FROM 
    src_info AS sif 
INNER JOIN src_serie AS se 
    ON sif.id = se.id 