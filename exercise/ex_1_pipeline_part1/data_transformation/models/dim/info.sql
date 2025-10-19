WITH info AS (SELECT * FROM {{ ref('src_tvseries_info') }}),
serie AS (SELECT * FROM  {{ ref('src_tvseries') }})

SELECT 
    {{dbt_utils.generate_surrogate_key(['s.name', 'f.summary'])}} AS id_info,
    s.name,
    MAX({{if_null_zero('f.rating_average')}}) AS "rating_average",
    MAX(f.runtime) AS "runtime",
    {{if_null('f.summary')}} AS 'summary',
    MAX({{if_null('f.image_medium')}}) AS "image_medium",
    MAX({{if_null('f.image_original')}}) AS "image_original"
FROM 
    info as f  
INNER JOIN serie as s 
    ON f.id = s.id
GROUP BY s.name, f.summary 