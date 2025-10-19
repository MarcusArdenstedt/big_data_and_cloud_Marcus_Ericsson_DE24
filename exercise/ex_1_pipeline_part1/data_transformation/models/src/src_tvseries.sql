WITH stg_tvseries AS (SELECT * FROM {{ source('tv_series', 'stg_series') }})

SELECT
    id,
    name,
    _links__show__name AS "show_name",
    CAST(season AS INT) AS "season",
    CAST(number AS INT) AS "number",
    CAST(type AS VARCHAR) AS "type",
    _links__show__href AS "links_show"
FROM 
    stg_tvseries


