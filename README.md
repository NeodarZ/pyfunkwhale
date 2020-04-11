# PyFunkwhale

A simple funkwhale API client library

Since API is not frozen, this client library is written for the version
`0.20.1`.

# Install

Only for dev for the momement:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Use

This client library use th OAuth2 Authorization Code flow and ask to the user
to authorize this app. I'm not ok with how I do this for the moment. If you
have suggestion about how to do this, I will gladly accept to discuse it.
And you can also send me suggestions for other parts of this module ;)

Example usage:

```
#!/usr/bin/env python
# -*- condig: utf-8 -*-

from pyfunkwhale.funkwhale import Funkwhale

client_name = "pyfunkwhale"

redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

# Obviously dont copy past and check the doc for how to get it:
# https://docs.funkwhale.audio/developers/authentication.html#create-an-app
client_id = "IFQuq6iB7Ta5LVxCUV8ibo65x588bgtI4rsa46cgm"
client_secret = "RMurKpQsoaZKbVpbse5o2wrJ5E4dMbvDs54JMsK5fDY5AK2QP8tJxoN7ApjryoCdWBUk02dExNTxzgUOZHFmSRcYdbJXbkLghXn6mvQMs9J8uIMpFIrehBp"

# This is your instance and login information
# This example is based on https://docs.funkwhale.audio/swagger/
username = "demo"
password = "demo"
domain = "https://demo.funkwhale.audio"

scopes = "read"

authorization_endpoint = "https://demo.funkwhale.audio/authorize"
token_endpoint = "https://demo.funkwhale.audio/api/v1/oauth/token/"


# Save the OAuth2 infos in file, this is ugly yup
token_filename = 'oauth_token.data'

funkwhale = Funkwhale(client_name, redirect_uri, client_id, client_secret,
                scopes, username, password, domain, authorization_endpoint,
                token_endpoint, token_filename)

artists = funkwhale.artists()

print(artists)

# In case you ask, their is an example for downloading a song
r = funkwhale.listen("f9d02c64-bafa-43cb-8e1e-fa612e7c5dab")

with open('/tmp/test.mp3', 'wb') as f:
    for chunk in r.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)
```

# Features

List of features implemented or planned:

- [x] Login
  - [x] Login with OAuth2 Authorization Code flow
- [x] Artists
  - [x] List artists
  - [x] Retrieve a single artist
  - [x] List available user libraries containing work from this artist
- [x] Albums
  - [x] List albums
  - [x] Retrieve a single album
  - [x] List available user libraries containing work from this album
- [x] Tracks
  - [x] List tracks
  - [x] Retrieve a single tracks
  - [x] List available user libraries containing work from this track
- [x] Download the audio file matching the given track uuid
- [x] License
  - [x] List licences
  - [x] Retrieve a single license
- [ ] favorites
  - [ ] Mark a given track as favorite
  - [ ] Remove
