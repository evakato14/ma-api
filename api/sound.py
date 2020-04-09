import statistics
import math


class Song:
    def __init__(self, title, track_id, album_id, album_art):
        self.title = title
        self.track_id = track_id
        self.album_id = album_id
        self.album_art = album_art
        self.audio_features = {}
        self.representative_distance = 0
        self.familiar_distance = 0
        self.accessibility_score = 0

    def get_representative_distance(self, compared_features):
        sum = 0
        for feature, _ in self.audio_features.items():
            dist = abs(self.audio_features[feature]-compared_features[feature])
            if feature == 'loudness':
                dist /= 60
            elif feature == 'tempo':
                dist /= 250
            sum += math.pow(dist, 2)
        self.representative_distance = math.sqrt(sum)

    def get_familiar_distance(self, compared_features):
        sum = 0
        for feature, _ in self.audio_features.items():
            dist = abs(self.audio_features[feature]-compared_features[feature])
            if feature == 'loudness':
                dist /= 60
            elif feature == 'tempo':
                dist /= 250
            sum += math.pow(dist, 2)
        self.familiar_distance = math.sqrt(sum)

    def get_accessibility_score(self, weight):
        representative_weight = weight
        familiar_weight = 1-weight
        self.accessibility_score = representative_weight * \
            self.representative_distance + familiar_weight*self.familiar_distance


class Album:
    def __init__(self, title, album_id, album_art):
        self.title = title
        self.album_id = album_id
        self.album_art = album_art


class Single:
    def __init__(self, title, album_id, album_art):
        self.title = title
        self.album_id = album_id
        self.album_art = album_art


def overall_sound(audio_features):
    center_audio_features = {}
    for feature in ['valence', 'danceability', 'energy', 'instrumentalness', 'speechiness', 'acousticness', 'loudness', 'tempo']:
        feature_values = []
        for data in audio_features:
            feature_values.append(data[feature])
        center_audio_features[feature] = statistics.median(feature_values)
    return center_audio_features
