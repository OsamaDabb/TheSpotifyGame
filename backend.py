import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from spotipy_random import get_random

import numpy as np

from typing import Set, Dict, List, Optional

import time


def delete_track(songs: dict, track_name: str) -> None:

    keys = list(songs.keys())

    for name in keys:

        if track_name in name:

            songs.pop(name)


class SpotipyInstance:

    def __init__(self, user: bool, scope: Optional[str] = None):

        if user:

            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                        client_id="390d1f202e0a4040b843778169ffd71d",
                                                        client_secret="f72cb245bc3842868e034743c3c7a4f1",
                                                        redirect_uri="https://localhost:8888/callback"))

        else:

            sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
                                                client_id="390d1f202e0a4040b843778169ffd71d",
                                                client_secret="f72cb245bc3842868e034743c3c7a4f1"))

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

    def get_recommendations(self, song: Dict) -> List[Dict]:

        return self.sp.recommendations(seed_tracks=[song["id"]])["tracks"]

    def get_targets(self) -> tuple[Dict, Dict]:

        start_song: dict = get_random(self.sp, type="track")
        end_song: dict = get_random(self.sp, type="track")

        return start_song, end_song

