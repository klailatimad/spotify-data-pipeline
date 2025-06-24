-- models/staging/stg_users.sql
SELECT
  user_id,
  age::INT AS age,
  country,
  preferred_genre,
  signup_date::DATE AS signup_date
FROM {{ ref('raw_users') }}