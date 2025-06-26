import os
import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# -------------------
# SET THESE VALUES
# -------------------
SPOTIPY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

genres = ['pop', 'rock', 'hip-hop', 'edm', 'jazz', 'indie', 'classical', 'metal', 'reggae', 'country']
tracks_per_genre = 100  # Up to 1,000 total

all_tracks = []

for genre in genres:
    print(f"\nCollecting tracks for genre: {genre}")
    collected = 0
    offset = 0

    while collected < tracks_per_genre:
        results = sp.search(q=f"genre:{genre}", type="track", limit=50, offset=offset)
        items = results.get('tracks', {}).get('items', [])
        if not items:
            break

        for track in items:
            all_tracks.append({
                'track_id': track['id'],
                'track_name': track['name'],
                'artist_id': track['artists'][0]['id'],
                'artist_name': track['artists'][0]['name'],
                'duration_ms': track['duration_ms'],
                'genre': genre,
                'popularity': track['popularity']
            })
            collected += 1
            if collected >= tracks_per_genre:
                break

        offset += 50

# Save to CSV in 'data' folder
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(all_tracks)
df.to_csv("data/spotify_tracks.csv", index=False)
print(f"\n✅ Saved {len(df)} songs to data/spotify_tracks.csv")
