#!/usr/bin/env python
# -*- conding: utf-8 -*-

import json
import re
from time import time
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import InvalidScopeError
from requests.models import Response

from pyfunkwhale.utils import read_file, write_file

class InvalidTokenError(Exception):

    def __init__(self, client):
        self.message = client.authorization_url

    def __str__(self):
        return self.message


class Client(object):

    def __init__(
        self, client_name: str, redirect_uri: str, username: str,
        password: str, domain: str, login_endpoint: str,
        client_secret: str = None, scopes: str = None, client_id: str = None,
        authorization_endpoint: str = None, token_filename: str = None
    ):
        """
        Client initialization.

        If the login_endpoint contain the path 'oauth' then the OAuth2
        Authorization Code flow will be used instead of the plain HTTP login.

        Parameters
        ----------
        client_name: str
            The name of the client using the API
        redirect_uri: str
            The redirect URI to use on the API
        username: str
            The username to use for login
        password: str
            The password to use for login
        login_endpoint: str
            The API login endpoint to use
        client_secret: str
            OAuth2 only. The client secret
        scopes: str
            OAuth2 only. The scopes of the client
        client_id: str
            OAuth2 only. The client id to use (A one registred on the API)
        authorization_endpoint: str
            OAuth2 only. The authorization endpoint to use on the API
        token_filename: str
            OAuth2 only. The token filename where to save the token
        """
        self.client_name = client_name
        self.redirect_uri = redirect_uri
        self.token = None

        self.username = username
        self.password = password
        self.domain = domain

        self.login_endpoint = login_endpoint

        if 'oauth' not in self.login_endpoint:
            self.session = requests.Session()
            self.session.auth = (username, password)

            self.session.get(self.domain + '/api/v1/token/')
        else:
            self.client_secret = client_secret
            self.scopes = scopes
            self.client_id = client_id
            self.authorization_endpoint = authorization_endpoint
            self.token_filename = token_filename
            self.oauth_client = OAuth2Session(
                            self.client_id,
                            redirect_uri=self.redirect_uri,
                            scope=self.scopes)
            self.authorization_url, self.state = self.oauth_client. \
                authorization_url(
                                self.authorization_endpoint)
            self._connect()

    def _connect(self):
        """
        Use saved token or ask a new one to the API.
        """
        try:
            self.token = json.loads(read_file(self.token_filename))
            self._refresh_token()
        except FileNotFoundError:
            raise InvalidTokenError(self)

    def _set_token(self, authorization_code: str = None):
        """
        Use the authorization_code to fetch the new token.
        """
        if (
                getattr(self, 'authorization_code', False)
                and not authorization_code
        ):
            raise InvalidTokenError(self)
        self.authorization_code = authorization_code

        self.token = self.oauth_client.fetch_token(
                                self.login_endpoint,
                                code=self.authorization_code,
                                client_secret=self.client_secret)
        write_file(self.token_filename, self.token)

    def _refresh_token(self):
        """
        Check if the token is expired in 60 seconds and if True will ask a new
        token from the instance.
        """
        if self.token is None:
            raise InvalidTokenError(self)
        if time() - 60 > self.token["expires_at"]:
            try:
                self.token = self.oauth_client.refresh_token(
                    self.login_endpoint,
                    refresh_token=self.token["refresh_token"],
                    client_id=self.client_id,
                    client_secret=self.client_secret)
                write_file(self.token_filename, self.token)
            except InvalidScopeError:
                raise InvalidTokenError(self)

    def _force_refresh_token(self):
        """
        Force the refresh of the OAuth2 token
        """
        self._set_token()
        write_file(self.token_filename, self.token)

    def _get_JWT_token(self) -> dict:
        """
        Get a JWT token.
        """
        data = {"username": self.username, "password": self.password}
        return self.call('/token', 'post', data=data).json()

    def call(self, endpoint: str, method: str, params: dict = None,
             data: dict = None, headers: dict = None) -> Response:
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
        pyfunkwhale.client.InvalidTokenError
            If current token is invalid
        """
        if getattr(self, 'oauth_client', False):
            self._refresh_token()
            if headers is None:
                headers = {'Authorization': self.token['token_type'] + ' ' +
                           self.token['access_token']}

            _call = getattr(self.oauth_client, method)

            endpoint = re.sub(r'^\/', '', endpoint)

            r = _call(self.domain + '/api/v1/' + endpoint, headers=headers,
                    params=params, data=data)

            if r.status_code == 401:
                raise InvalidTokenError(self)

            r.raise_for_status()
        else:
            _call = getattr(self.session, method)
            r = _call(self.domain + '/api/v1/' + endpoint, headers=headers,
                    params=params, data=data)

            r.raise_for_status()

        return r
