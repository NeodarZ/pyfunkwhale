#!/usr/bin/env python
# -*- conding: utf-8 -*-

import json
from time import time
from requests_oauthlib import OAuth2Session

from pyfunkwhale.utils import read_file, write_file


class Client(object):

    def __init__(self, client_name, redirect_uri, client_id,
                 client_secret, scopes, username, password, domain,
                 authorization_endpoint, token_endpoint,
                 token_filename):
        self.client_name = client_name
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.token = None

        self.username = username
        self.password = password
        self.domain = domain

        self.authorization_endpoint = authorization_endpoint
        self.token_endpoint = token_endpoint
        self.token_filename = token_filename
        self.oauth_client = OAuth2Session(
                        self.client_id,
                        redirect_uri=self.redirect_uri,
                        scope=self.scopes)
        self.authorization_url, self.state = self.oauth_client. \
            authorization_url(
                            self.authorization_endpoint)

        try:
            self.token = json.loads(read_file(token_filename))
            self._refresh_token()
        except FileNotFoundError:
            self._get_token()
            write_file(token_filename, self.token)

    def _get_token(self):
        print("For authorizate this app go to:\n{}".format(
                self.authorization_url))
        self.authorization_code = input("Enter response code: ")

        self.token = self.oauth_client.fetch_token(
                                self.token_endpoint,
                                code=self.authorization_code,
                                client_secret=self.client_secret)

    def _refresh_token(self):
        if time() - 60 > self.token["expires_at"]:
            self.token = self.oauth_client.refresh_token(
                self.token_endpoint,
                refresh_token=self.token["refresh_token"],
                client_id=self.client_id,
                client_secret=self.client_secret)
            write_file(self.token_filename, self.token)

    def call(self, endpoint, method):
        self._refresh_token()
        headers = {'Authorization': self.token['token_type'] + ' ' +
                   self.token['access_token']}

        call = getattr(self.oauth_client, method)

        r = call(
            self.domain + '/api/v1/' + endpoint,
            headers=headers)

        return r
