## How to get access token, refresh_token

#### 1. Get your strava permanent details
Go to: https://www.strava.com/settings/api
then create a file 'secrets.py' and paste:

    client_id=53310
    key_secret="21f581c2f0ghcac3d2953d1a958f9f4dbc92b042"

#### 2. Insert following in your browser

    https://www.strava.com/oauth/authorize?client_id=53310&redirect_uri=http://localhost&response_type=code&scope=read,activity:read_all,activity:write

#### 3. Collect code appearing in url bar after request

code=bab43b9f5a0d7c3a90931b70d07ca0a306f232e2

#### 4. Insert following in postman type POST
    https://www.strava.com/oauth/token?client_id=53310&client_secret=21f581c2f0ghcac3d2953d1a958f9f4dbc92b042&code=bab43b9f5a0d7c3a90931b70d07ca0a306f232e2&grant_type=authorization_code

#### 5. Collect access and refresh tokens
From the json reply, collect access and refresh tokens, then paste the following in your 'secrets.py':

    client_id=53310
    key_secret="21f581c2f0ghcac3d2953d1a958f9f4dbc92b042"
    refresh_token="b07a4be1c561e0edik61d6f6ba9c4b8b4e8be84d"
    access_token="f538bd3986f23bcf57e84a3a54734d498c6a1dc7"

#### 6. Experiment requests
    http GET "https://www.strava.com/api/v3/segments/explore?bounds=[36.372975, -94.220234, 36.415949, -94.183670]&activity_type=&min_cat=&max_cat=" "Authorization: Bearer b07a4be1c561e0edik61d6f6ba9c4b8b4e8be84d"