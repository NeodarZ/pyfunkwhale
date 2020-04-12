#!/usr/bin/env python
# -*- conding: utf-8 -*-

import json
import re
from time import time
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import InvalidScopeError
from requests.models import Response

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
        """
        Ask the user to go on the authorization page of the funkwhale instance
        and then wait the response code for fetch the token generated.
        """
        print("For authorizate this app go to:\n{}".format(
                self.authorization_url))
        self.authorization_code = input("Enter response code: ")

        self.token = self.oauth_client.fetch_token(
                                self.token_endpoint,
                                code=self.authorization_code,
                                client_secret=self.client_secret)

    def _refresh_token(self):
        """
        Check if the token is expired in 60 seconds and if True will ask a new
        token from the instance.
        """
        if time() - 60 > self.token["expires_at"]:
            try:
                self.token = self.oauth_client.refresh_token(
                    self.token_endpoint,
                    refresh_token=self.token["refresh_token"],
                    client_id=self.client_id,
                    client_secret=self.client_secret)
            except InvalidScopeError:
                self._get_token()
            write_file(self.token_filename, self.token)

    def call(self, endpoint: str, method: str, params: dict = None,
             data: dict = None) -> Response:
        """
        Call the API

        Parameters
        ----------
        endpoint : str
            The endpoint to call on the API
        method : str
            The HTTP method to use for calling the endpoint
        params : dict, optional
            The uri params for a GET method
        data : dict, optional
            The uri data for a POST method

        Raises
        ------
        requests.exceptions.HTTPError
            If their is an error during requesting the API.
        """
        self._refresh_token()
        headers = {'Authorization': self.token['token_type'] + ' ' +
                   self.token['access_token']}

        call = getattr(self.oauth_client, method)

        endpoint = re.sub(r'^\/', '', endpoint)

        r = call(self.domain + '/api/v1/' + endpoint, headers=headers,
                 params=params, data=data)

        r.raise_for_status()

        return r
