import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from spotipy_random import get_random

from typing import Set, Dict, List, Optional

API_ID = "YOUR SPOTIFY ID HERE"
API_Secret = "YOUR SECRET HERE"


def delete_track(songs: dict, track_name: str) -> None:

    keys = list(songs.keys())

    for name in keys:

        if track_name in name:

            songs.pop(name)


class SpotipyInstance:

    def __init__(self, user: bool, scope: Optional[str] = None):

        if user:

            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                        client_id=API_ID,
                                                        client_secret=API_Secret,
                                                        redirect_uri="https://localhost:8888/callback"))

        else:

            sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
                                                client_id=API_ID,
                                                client_secret=API_Secret))

        self.sp = sp

    def get_artist_songs(self, artist_name: str) -> Dict[str, Dict]:

        artist_id = self.sp.search(q=artist_name, type="artist",
                                   limit=1)["artists"]["items"][0]["id"]

        artist_albums = self.sp.artist_albums(artist_id)["items"]

        songs = {}

        for album in artist_albums:

            for song in self.sp.album_tracks(album["id"])["items"]:

                songs[song["name"]] = song

        return songs

    def get_recommendations(self, songs: List[Dict]) -> List[Dict]:

        ids = [song["id"] for song in songs]

        return self.sp.recommendations(seed_tracks=ids, limit=9)["tracks"]

    def get_targets(self) -> tuple[Dict, Dict]:

        start_song: dict = get_random(self.sp, type="track", market="US")
        end_song: dict = get_random(self.sp, type="track", market="US")

        """
        while "en" not in start_song["artists"][0]["external_urls"]["spotify"]:
        
            time.sleep(0.2)

            start_song: dict = get_random(self.sp, type="track", market="US")

        while "en" not in end_song["artists"][0]["external_urls"]["spotify"]:
        
            time.sleep(0.2)

            end_song: dict = get_random(self.sp, type="track", market="US")
        """

        return start_song, end_song

