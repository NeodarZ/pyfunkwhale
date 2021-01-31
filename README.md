# PyFunkwhale

A simple funkwhale API client library

Since API is not frozen, this client library is written for the version
`1.0.1`.

# Install

Only for dev for the momement:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Use

First you to select an authentification method, two are actually available
Plain HTTP and OAuth2.

## Plain HTTP authentification

```
#!/usr/bin/env python
# -*- condig: utf-8 -*-

from pyfunkwhale.funkwhale import Funkwhale
from pyfunkwhale.client import InvalidTokenError

client_name = "pyfunkwhale"

redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

# This is your instance and login information
username = "demo"
password = "demo"
domain = "https://demo.funkwhale.audio"

authorization_endpoint = domain + "/authorize"
login_endpoint = domain + "/api/v1/oauth/token/"

login_endpoint = domain + "/api/v1/token/"

funkwhale = Funkwhale(
    client_name,
    redirect_uri,
    username,
    password,
    domain,
    login_endpoint,
)

artists = funkwhale.albums()

print(artists)
```

## OAuth2 Authorization Code flow

```
#!/usr/bin/env python
# -*- condig: utf-8 -*-

from pyfunkwhale.funkwhale import Funkwhale
from pyfunkwhale.client import InvalidTokenError

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

authorization_endpoint = domain + "/authorize"
login_endpoint = domain + "/api/v1/oauth/token/"

# Save the OAuth2 infos in file, this is ugly yup
token_filename = 'oauth_token.data'

# You need to handle the invalidity of a token and ask for a new one
def _ask_new_auth(funkwhale, message):
  print(message)
  authorization_code = input("Enter response code: ")
  funkwhale.client._set_token(authorization_code)

funkwhale = Funkwhale(
    client_name,
    redirect_uri,
    username,
    password,
    domain,
    login_endpoint,
    client_secret,
    scopes,
    client_id,
    authorization_endpoint,
    token_filename,
)

try:
  artists = funkwhale.artists()
except InvalidTokenError as e:
  _ask_new_auth(funkwhale, e.message)
  artists = funkwhale.artists()

print(artists)
```

## Examples

In case you ask, their is an example for downloading a song

```
r = funkwhale.listen("f9d02c64-bafa-43cb-8e1e-fa612e7c5dab")

with open('/tmp/test.mp3', 'wb') as f:
    for chunk in r.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)
```

# Features

List of features implemented or planned:

- [/] Auth
  - [x] OAuth2 Authorization Code flow
    - [x] Login
    - [x] Register an application
    - [x] Get an JWT token
  - [x] Simple Authentication
    - [x] Login
  - [ ] Create an account
  - [ ] Request a password request
  - [x] Retrieve user information
  - [x] Retrieve rate-limit information and current usage status
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
- [ ] libraries
  - [ ] List owned libraries
  - [ ] Create a new librarie
  - [ ] Retrieve a librarie
  - [ ] Update a librarie
  - [ ] Update a librarie
  - [ ] Delete a librarie and all associated password
- [ ] Uploads
  - [ ] List owned upload
  - [ ] Upload a new file in a library
  - [ ] Retrieve an upload
  - [ ] Delete a an upload
- [x] favorites
  - [x] List favorites
  - [x] Mark a given track as favorite
  - [x] Remove a given track from favorites
