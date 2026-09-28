from abc import ABC, abstractmethod

from core.errors import BaseError
from core.modules import Service
from core.schemas import Album, AlbumShort, Artist, ArtistShort, Track, TrackShort


class Search(Service, ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def search_tracks(self, query: str) -> list[TrackShort]:
        pass

    @abstractmethod
    def search_albums(self, query: str) -> list[AlbumShort]:
        pass

    @abstractmethod
    def search_artists(self, query: str) -> list[ArtistShort]:
        pass

    @abstractmethod
    def get_track(self, id: str) -> Track | BaseError:
        pass

    @abstractmethod
    def get_album(self, id: str) -> Album | BaseError:
        pass

    @abstractmethod
    def get_artist(self, id: str) -> Artist | BaseError:
        pass
