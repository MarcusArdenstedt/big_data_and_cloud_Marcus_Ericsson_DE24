with stg_tvseries AS (SELECT * FROM {{ source('tv_series', 'stg_series') }})

SELECT 
   id,
   CAST(airdate AS date) AS "airdate",
   COALESCE(
      strftime(try_strptime(airtime, '%H:%M:%S'), '%H:%M'), 
      strftime(try_strptime(airtime, '%H:%M'), '%H:%M')) AS "airtime",
   airstamp,
   CAST(runtime AS INT) AS "runtime",
   rating__average AS "rating_average",
   image__medium AS "image_medium",
   image__original AS "image_original",
   summary
FROM 
 stg_tvseries