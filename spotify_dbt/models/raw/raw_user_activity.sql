-- models/raw/raw_user_activity.sql
SELECT * FROM {{ source('public', 'user_activity') }}
