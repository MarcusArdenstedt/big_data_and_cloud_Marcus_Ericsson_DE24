SELECT 
    show_name
FROM 
    {{ ref('serie') }}
WHERE LOWER(trim(show_name)) not in ('game of thrones', 'stranger things', 'the lord of the rings: the rings of power')