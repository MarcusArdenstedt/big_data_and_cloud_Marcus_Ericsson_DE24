WITH info AS (SELECT * FROM {{ ref('info') }}),
serie AS (SELECT * FROM {{ ref('serie') }}),
fct AS (SELECT * FROM {{ ref('fct_tvseries') }})

SELECT
    s.show_name,
    f.season,
    f.number,
    i.rating_average,
FROM fct AS f
LEFT JOIN serie AS s 
ON f.id_serie = s.id_serie 
LEFT JOIN info AS i 
ON f.id_info = i.id_info
ORDER BY 
    s.show_name ASC
