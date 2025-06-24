-- models/raw/raw_songs.sql
SELECT * FROM {{ source('public', 'songs') }}
