import json
from urllib import request, parse

VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

def submit(secret, response, remoteip=None):
    data = {
        'secret': secret,
        'response': response
    }

    if remoteip:
        data['remoteip'] = remoteip

    encoded = parse.urlencode(data).encode()

    req = request.Request(VERIFY_URL, data=encoded)

    with request.urlopen(req) as resp:
        json_resp = json.loads(resp.read().decode('utf-8'))

        if json_resp['success']:
            return (True, None)
        else:
            return (False, json_resp['error-codes'])