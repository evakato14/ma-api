from flask import Blueprint, jsonify, request
from . import db
from .models import SongRating
from .spotify_main import spotify_main

main = Blueprint('main', __name__)


@main.route('/add_rating', methods=['POST'])
def add_rating():
    rating_data = request.get_json()

    new_rating = SongRating(
        song_id=rating_data['song_id'], rating=rating_data['rating'])

    db.session.add(new_rating)
    db.session.commit()

    return 'Done', 201


@main.route('/ratings')
def ratings():
    song_rating_list = SongRating.query.all()
    song_ratings = []

    for song_rating in song_rating_list:
        song_ratings.append(
            {'song_id': song_rating.song_id, 'rating': song_rating.rating})

    return jsonify({'ratings': song_ratings})


@main.route('/audio_features', methods=['GET'])
def audio_features():
    spotify_data = spotify_main(
        request.args['artist'], request.args['token'], request.args['range'], request.args['weight'])

    artist_audio_features = spotify_data['artist_overall_sound']
    artist_album_types = spotify_data['artist_album_types']
    user_audio_features = spotify_data['user_overall_sound']
    user_two_songs = spotify_data['user_two_songs']
    recommended_tracks = [
        song.__dict__ for song in spotify_data['recommended_tracks']]

    return jsonify({'artist_audio_features': artist_audio_features,
                    'artist_album_types': artist_album_types,
                    'user_audio_features': user_audio_features,
                    'user_two_songs': user_two_songs,
                    'recommended_tracks': recommended_tracks})
