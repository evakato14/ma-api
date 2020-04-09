import spotipy
import random
from .sound import overall_sound

audio_feature_keys = ['valence', 'danceability', 'energy',
                      'instrumentalness', 'speechiness', 'acousticness', 'loudness', 'tempo']


def get_user_sound_data(auth_token, time_range):
    all_songs = []
    track_audio_features = []
    spotify = spotipy.Spotify(auth=auth_token)
    results = spotify.current_user_top_tracks(time_range=time_range, limit=50)
    random_two_songs = random.sample(results['items'], 2)
    for _, item in enumerate(results['items']):
        all_songs.append(item['id'])
    audio_feature_data = spotify.audio_features(all_songs)
    for track in audio_feature_data:
        track_audio_features.append(
            {key: track[key] for key in audio_feature_keys})
    return overall_sound(track_audio_features), random_two_songs
