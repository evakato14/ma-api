from .artist_api import get_artist_data
from .user_api import get_user_sound_data
from .sound import Song, overall_sound


def spotify_main(artist_uri, auth_token, time_range, weight):
    user_sound_data = get_user_sound_data(auth_token, time_range)
    user_overall_sound = user_sound_data[0]
    artist_data = get_artist_data(artist_uri)
    artist_songs = artist_data[0]
    artist_overall_sound = overall_sound(
        [song.audio_features for song in artist_songs])
    for song in artist_songs:
        song.get_representative_distance(artist_overall_sound)
        song.get_familiar_distance(user_overall_sound)
        song.get_accessibility_score(float(weight))

    ranked_songs = sorted(
        artist_songs, key=lambda song: song.accessibility_score, reverse=False)
    # for song in ranked_songs:
    #print(song.title, song.accessibility_score)

    return {'artist_overall_sound': artist_overall_sound,
            'artist_album_types': artist_data[1],
            'user_overall_sound': user_sound_data[0],
            'user_two_songs': user_sound_data[1],
            'recommended_tracks': ranked_songs[:10]}
