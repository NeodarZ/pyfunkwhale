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
        params = {}
        for k, v in arguments.items():
            if k != 'self' and v is not None:
                params[k] = v

        return params

    def artists(self):
        return self.client.call('/artists/', 'get').json()
