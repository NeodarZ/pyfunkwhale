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
        """

        arguments = locals()

        params = self._build_params(arguments)

        return self.client.call(f'/artists/{_id}', 'get', params).json()

    def artist_librairies(self, _id: int, page: int = None,
                          page_size: int = None):
        """
        List available user libraries containing work from this artist
        """

        arguments = locals()

        params = self._build_params(arguments)

        return self.client.call(
                f'/artists/{_id}/libraries/', 'get', params).json()
