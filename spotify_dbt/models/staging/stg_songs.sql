-- models/staging/stg_songs.sql
SELECT
  track_id,
  track_name,
  artist_id,
  artist_name,
  duration_ms::INT AS duration_ms,
  genre,
  popularity::INT AS popularity
FROM {{ ref('raw_songs') }}
