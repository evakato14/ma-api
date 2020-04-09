import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .sound import Song, Album, Single

audio_feature_keys = ['valence', 'danceability', 'energy',
                      'instrumentalness', 'speechiness', 'acousticness', 'loudness', 'tempo']


def get_artist_data(artist_uri):
    all_songs = []
    all_albums = []
    all_singles = []
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials())

    artist_popularity = spotify.artist(artist_uri)['popularity']

    offset = 0
    search = True
    albums = []
    while search:
        results = spotify.artist_albums(
            artist_uri, album_type='album,single', limit='50', country='US', offset=offset)['items']
        if len(results) < 50:
            search = False
        else:
            offset += 50
        albums.extend(results)

    for album in albums:
        album_popularity = spotify.album(album['id'])['popularity']
        # I'm not gonna lie, this tree is super messy but I just want the singles to work
        if album_popularity >= 0.6*artist_popularity or album['album_type'] == 'single':
            if album['album_type'] == 'album':
                all_albums.append(
                    Album(album['name'], album['id'], album['images'][0]['url']))
            else:
                if album_popularity >= 0.4*artist_popularity and album['name'] not in [song.title for song in all_songs]:
                    all_singles.append(
                        Single(album['name'], album['id'], album['images'][0]['url']))
            if album['album_type'] == 'album' or (album['album_type'] == 'single' and album_popularity >= 0.4*artist_popularity):
                for track in spotify.album_tracks(album['id'], limit=50)['items']:
                    # Avoid repeat songs, such as singles released prior to an album release
                    if track['name'] not in [song.title for song in all_songs]:
                        all_songs.append(
                            Song(track['name'], track['id'], album['id'], album['images'][0]['url']))

    for i in range(0, len(all_songs), 50):
        track_audio_features = spotify.audio_features(
            [song.track_id for song in all_songs][i:i+50])
        for track_audio_feature in track_audio_features:
            for song in all_songs:
                if track_audio_feature['id'] == song.track_id:
                    song.audio_features = {
                        audio_feature: track_audio_feature[audio_feature] for audio_feature in audio_feature_keys}

    album_types = {'albums': [album.__dict__ for album in all_albums], 'singles': [
        single.__dict__ for single in all_singles]}

    return all_songs, album_types
