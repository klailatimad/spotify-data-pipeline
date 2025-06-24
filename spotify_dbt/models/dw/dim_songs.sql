-- models/dw/dim_songs.sql
SELECT DISTINCT
  track_id,
  track_name,
  artist_id,
  artist_name,
  duration_ms,
  genre,
  popularity
FROM {{ ref('stg_songs') }}