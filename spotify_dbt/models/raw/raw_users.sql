-- models/raw/raw_users.sql
SELECT * FROM {{ source('public', 'users') }}
