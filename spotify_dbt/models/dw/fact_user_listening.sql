-- models/dw/fact_user_listening.sql
SELECT
  ua.event_id,
  ua.user_id,
  u.country,
  ua.track_id,
  s.artist_name,
  ua.timestamp,
  ua.duration_ms,
  ua.completed,
  ua.skipped,
  ua.device_type,
  ua.location
FROM {{ ref('stg_user_activity') }} ua
JOIN {{ ref('stg_users') }} u ON ua.user_id = u.user_id
JOIN {{ ref('stg_songs') }} s ON ua.track_id = s.track_id