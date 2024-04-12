import re
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import time
import json


spotify_client_id = "5c787e0eccd246ba9c4500f755bff00b"
spotify_client_secret = "a9b2fc8b4eac4f219aaa8dd852e98b1c"
spotify_user_id = "spotify:user:daeshaunmorrison"
spotify_playlist_id = "spotify:playlist:47FWzqz1PwNyKaIApQjF9H"
spotify_playlist_id ="spotify:playlist:6k6gktoOhlHLrGXr8M8Psy"
genius_key = "dZCHAObV2X7ZCH4QN2bewuX7lAVoVHedaot3cNn8l_dpwtSwWEaK1cHg8TrbhDtq"
genius_token='4Os3tEbxKSqR_gE76OqwUY3TTQVO11MVLDy14ZmmrC4AS0SygKak8dpgZy3wb5pe'
genius = lyricsgenius.Genius(genius_token)

def clean_lyrics(txt):
    no_brackets = re.sub(r'\[.*?\]', '', txt)
    return no_brackets

class GetLyrics():
    
    def __init__(self, spotify_client_id, spotify_client_secret, user_id, playlist_id, genius_key):
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        self.user_id = user_id
        self.playlist_id = playlist_id
        self.genius_key = genius_key
        
    def get_playlist_info(self):
        token = SpotifyClientCredentials(client_id=self.spotify_client_id, client_secret=self.spotify_client_secret)
        sp = spotipy.Spotify(client_credentials_manager=token)
        playlist = sp.user_playlist_tracks(self.user_id, self.playlist_id)
        self.playlist = playlist
        return self.playlist
    
    def get_track_names(self):
        track_names = []
        for song in range(len(self.playlist['items'])):
            track_names.append(self.playlist['items'][song]['track']['name'])
        self.track_names = track_names
        return self.track_names
    
    def get_track_artists(self):
        track_artists = []
        for song in range(len(self.playlist['items'])):
            track_artists.append(self.playlist['items'][song]['track']['artists'][0]['name'])
        self.track_artists = track_artists
        return self.track_artists
        

    def get_lyrics(self):
        playlist = GetLyrics.get_playlist_info(self)
        track_names = GetLyrics.get_track_names(self)
        track_artists = GetLyrics.get_track_artists(self)
        song_lyrics = {}

        for i in range(len(track_names)):
            time.sleep(3)
            print("\n")
            print(f"Working on track {i}: {track_names[i]} {track_artists[i]}.")
            try:
                song = genius.search_song(track_names[i], artist=track_artists[i])
            except:
                print("Timed out\n\n\n\n\n")
                time.sleep(8)
                song = genius.search_song(track_names[i], artist=track_artists[i])
            
            if song is None or song.lyrics is None:
                print(f"Track {i} is not in the Genius database.")
            else:
                lyrics_clean = clean_lyrics(song.lyrics)
                #print(f"Retrieved track {i} lyrics! {lyrics_clean}")
                song_lyrics[i] = {'artist': track_artists[i], 'song': track_names[i], 'lyrics': lyrics_clean}

        return song_lyrics


songs = GetLyrics(spotify_client_id, spotify_client_secret, spotify_user_id, spotify_playlist_id, genius_key)
song_lyrics = songs.get_lyrics()

# Write artist-song-lyrics data to a JSON file
with open("lyric_retrival\\lyrics.json", "w") as json_file:
    json.dump(song_lyrics, json_file, indent=4)