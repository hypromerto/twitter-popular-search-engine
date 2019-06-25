import requests, base64

base_url = 'https://api.twitter.com/'

def authorization(client_key, client_secret):

    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    access_token = auth_resp.json()['access_token']

    return access_token

def fetch_tweets(client_key, client_secret, search_parameter):

    access_token = authorization(client_key, client_secret)
    search_headers = { 

        'Authorization': 'Bearer {}'.format(access_token)
    }

    search_params = {

        'q': search_parameter,
        'result_type': 'popular',
        'count': 100,
        "include_entities": True
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)

    search_resp = requests.get(search_url, headers = search_headers, params = search_params)

    return search_resp



