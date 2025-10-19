WITH serie AS (SELECT * FROM {{ ref('src_tvseries') }})

SELECT
    {{dbt_utils.generate_surrogate_key(['s.show_name', 's.links_show'])}} AS id_serie,
    MAX(s.show_name) AS "show_name",
    MAX(s.links_show) AS "links_show"
FROM
    serie AS s
GROUP BY s.show_name, s.links_show