-- models/dw/dim_users.sql
SELECT DISTINCT
  user_id,
  age,
  country,
  preferred_genre,
  signup_date
FROM {{ ref('stg_users') }}