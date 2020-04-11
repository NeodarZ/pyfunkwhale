#!/usr/bin/env python

from pyfunkwhale.client import Client


class Funkwhale(object):

    def __init__(self, client_name, redirect_uri, client_id,
                 client_secret, scopes, username, password, domain,
                 authorization_endpoint, token_endpoint, token_filename):
        self.client = Client(
                client_name, redirect_uri, client_id, client_secret,
                scopes, username, password, domain, authorization_endpoint,
                token_endpoint, token_filename)

    def _build_params(self, arguments):
        """
        Build params dict for python-requests. Not that all key who start
        with an underscore are treated as par of the endpoint uri and are not
        as uri parameters.
        """
        params = {}
        for k, v in arguments.items():
            if k != 'self' and v is not None and not k.startswith("_"):
                params[k] = v

        return params

    def artists(self, q: str = None, ordering: str = None,
                playable: bool = None, page: int = None,
                page_size: int = None) -> dict:
        """
        List artists

        Parameters
        ----------
        q : str, optional
            Search query used to filter artists
        ordering : str, optional
            Ordering for the results, prefix with - for DESC ordering
            Available values: creation_date, id, name
        playable : bool, optional
            Filter/exclude resources with playable artits
        page : int, optional
            Default value: 1
        page_size : int, optional
            Default value: 25

        Raises
        ------
        ValueError
            If `ordering` are set with wrong values
        """

        arguments = locals()

        ordering_field = ['creation_date', 'id', 'name']
        if ordering is not None and ordering not in ordering_field:
            raise ValueError("The ordering field {} is not in the ordering"
                             "fields accepted".format(ordering))

        params = self._build_params(arguments)

        return self.client.call('/artists/', 'get', params).json()

    def artist(self, _id: int, refresh: bool = False):
        """
        Retrieve a single artist

        Parameters
        ----------
        _id : int
            Object ID
        refresh : bool, optional
            Trigger an ActivityPub fetch to refresh local data
        """

        arguments = locals()

        params = self._build_params(arguments)

        return self.client.call(f'/artists/{_id}', 'get', params).json()

    def artist_libraries(self, _id: int, page: int = None,
                         page_size: int = None):
        """
        List available user libraries containing work from this artist

        Parameters
        ----------
        _id : int
            Object ID
        page : int, optional
            Default value: 1
        page_size : int, optional
            Default value: 25
        """

        arguments = locals()

        params = self._build_params(arguments)

        return self.client.call(
                f'/artists/{_id}/libraries/', 'get', params).json()

    def albums(self, q: str = None, artist: int = None, ordering: str = None,
               playable: bool = None, page: int = None,
               page_size: int = None) -> dict:
        """
        List albums


        Parameters
        ----------
        q : str, optional
            Search query used to filter albums
        artist : int, optional
            Only include albums by the requested artist
        ordering : str, optional
            Ordering for the results, prefix with - for DESC ordering
            Available values: creation_date, release_date, title
        playable : bool, optional
            Filter/exclude resources with playable albums
        page : int, optional
            Default value: 1
        page_size : int, optional
            Default value: 25

        Raises
        ------
        ValueError
            If `ordering` are set with wrong values
        """

        arguments = locals()

        ordering_field = ['creation_date', 'release_date', 'title']
        if ordering is not None and ordering not in ordering_field:
            raise ValueError("The ordering field {} is not in the ordering"
                             "fields accepted".format(ordering))

        params = self._build_params(arguments)

        return self.client.call('/albums/', 'get', params).json()

    def album(self, _id: int, refresh: bool = False):
        """
        Retrieve a single album

        Parameters
        ----------
        _id : int
            Object ID
        refresh : bool, optional
            Trigger an ActivityPub fetch to refresh local data
        """

        arguments = locals()

        params = self._build_params(arguments)

        return self.client.call(f'/albums/{_id}', 'get', params).json()

    def album_libraries(self, _id: int, page: int = None,
                        page_size: int = None):
        """
        List available user libraries containing work from this album

        Parameters
        ----------
        _id : int
            Object ID
        page : int, optional
            Default value: 1
        page_size : int, optional
            Default value: 25
        """

        arguments = locals()

        params = self._build_params(arguments)

        return self.client.call(
                f'/albums/{_id}/libraries/', 'get', params).json()

    def tracks(self, q: str = None, artist: int = None, ordering: str = None,
               playable: bool = None, page: int = None,
               page_size: int = None) -> dict:
        """
        List tracks

        Parameters
        ----------
        q : str, optional
            Search query used to filter tracks
        artist : int, optional
            Only include tracks by the requested artist
        favorites : bool, optional
            filter/exclude tracks favorited by the current user
        album : int, optional
            Only include tracks from the requested album
        license : str, optional
            Only include tracks with the given license
        ordering : str, optional
            Ordering for the results, prefix with - for DESC ordering
            Available values: creation_date, release_date, title
        playable : bool, optional
            Filter/exclude resources with playable tracks
        page : int, optional
            Default value: 1
        page_size : int, optional
            Default value: 25

        Raises
        ------
        ValueError
            If `ordering` are set with wrong values
        """

        arguments = locals()

        ordering_field = ['creation_date', 'release_date', 'title']
        if ordering is not None and ordering not in ordering_field:
            raise ValueError("The ordering field {} is not in the ordering"
                             "fields accepted".format(ordering))

        params = self._build_params(arguments)

        return self.client.call('/tracks/', 'get', params).json()

    def track(self, _id: int, refresh: bool = False):
        """
        Retrieve a single track

        Parameters
        ----------
        _id : int
            Object ID
        refresh : bool, optional
            Trigger an ActivityPub fetch to refresh local data
        """

        arguments = locals()

        params = self._build_params(arguments)

        return self.client.call(f'/tracks/{_id}', 'get', params).json()

    def track_libraries(self, _id: int, page: int = None,
                        page_size: int = None):
        """
        List available user libraries containing work from this track

        Parameters
        ----------
        _id : int
            Object ID
        page : int, optional
            Default value: 1
        page_size : int, optional
            Default value: 25
        """

        arguments = locals()

        params = self._build_params(arguments)

        return self.client.call(
                f'/tracks/{_id}/libraries/', 'get', params).json()

    def listen(self, _uuid, to: str = None, upload: str = None):
        """
        Download the audio file matching the given track uuid

        Given a track uuid (and not ID), return the first found audio file
        accessible by the user making the request.

        In case of a remote upload, this endpoint will fetch the audio file
        from the remote and cache it before sending the response.

        Parameters
        ----------
        _uuid : str
            Track uuid
        to : str, optional
            If specified, the endpoint will return a transcoded version of the
            original audio file.
            Since transcoding happens on the fly, it can significantly
            increase response time, and it's recommended to request transcoding
            only for files that are not playable by the client.
            This endpoint support bytess-range requests.
            Available values : ogg, mp3
        upload: str, optional
            If specified, will return the audio for the given upload uuid.
            This is useful for tracks that have multiple uploads available.

        Raises
        ------
        ValueError
            If `to` are set with wrong values
        """

        arguments = locals()

        to_fields = ['ogg', 'mp3']
        if to is not None and to not in to_fields:
            raise ValueError("The to field {} is not in the to"
                             "fields accepted".format(to))

        params = self._build_params(arguments)

        return self.client.call(f'/listen/{_uuid}', 'get', params)
