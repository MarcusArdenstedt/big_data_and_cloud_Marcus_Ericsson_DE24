SELECT 
    season
FROM 
    {{ ref('fct_tvseries') }}
WHERE season <= 0