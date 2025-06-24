-- models/dw/fact_user_listening.sql
{{ config(
    materialized='incremental',
    unique_key='event_id'
) }}

SELECT
    ua.event_id,
    ua.user_id,
    ua.track_id,
    ua.timestamp,
    ua.duration_ms,
    ua.completed,
    ua.skipped,
    ua.device_type,
    ua.location,
    s.track_name,
    s.artist_name,
    s.genre,
    u.age,
    u.country,
    u.preferred_genre
FROM {{ ref('stg_user_activity') }} ua
JOIN {{ ref('stg_users') }} u ON ua.user_id = u.user_id
JOIN {{ ref('stg_songs') }} s ON ua.track_id = s.track_id

{% if is_incremental() %}
WHERE ua.timestamp > (SELECT MAX(timestamp) FROM {{ this }})
{% endif %}