-- models/staging/stg_user_activity.sql
SELECT
  event_id,
  user_id,
  track_id,
  timestamp::TIMESTAMP AS timestamp,
  duration_ms::INT AS duration_ms,
  completed::BOOLEAN AS completed,
  skipped::BOOLEAN AS skipped,
  device_type,
  location
FROM {{ ref('raw_user_activity') }}
