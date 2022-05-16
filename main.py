import requests
import logging
import string
import random
from requests.auth import HTTPBasicAuth
import hashlib
import base64
import re
import time
import json
import web
import os

def replacer(match):
    return match.group(1).upper()

def generate_code_challenge(code_verifier):
    encoded_bytes = base64.b64encode(
        hashlib.sha256(str.encode(code_verifier)).digest())
    encoded_str = str(encoded_bytes, "utf-8")
    encoded_str = encoded_str.replace("=", "")
    encoded_str = encoded_str.replace("+", "-")
    encoded_str = encoded_str.replace("/", "_")
    return encoded_str


def fetch_auth_code(code_verifier):
    client_id = os.environ['CAME_CONNECT_CLIENT_ID']
    client_secret = os.environ['CAME_CONNECT_CLIENT_SECRET']
    username = os.environ['CAME_CONNECT_USERNAME']
    password = os.environ['CAME_CONNECT_PASSWORD']
    nonce = random_string(100)
    state = random_string(100)
    response_type = 'code'
    code_challenge = generate_code_challenge(code_verifier)
    code_challenge_method = 'S256'
    redirect_uri = 'https://www.cameconnect.net/role'

    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'username': username,
        'password': password
    }

    url = "https://app.cameconnect.net/api/oauth/auth-code?client_id={}&response_type={}&redirect_uri={}&state={}&nonce={}&code_challenge={}&code_challenge_method={}".format(
        client_id, response_type, redirect_uri, state, nonce, code_challenge, code_challenge_method)

    response = requests.post(
        url, data=data, auth=HTTPBasicAuth(client_id, client_secret))

    code = response.json()['code']
    state = response.json()['state']

    return code


def random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def fetch_bearer_token(client_id, client_secret, code, code_verifier):
    redirect_uri = 'https://www.cameconnect.net/role'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }

    url = "https://app.cameconnect.net/api/oauth/token"

    response = requests.post(
        url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    json = response.json()

    bearer = {
        'access_token': json['access_token'],
        'expires_in': json['expires_in']
    }

    return bearer


def fetch_token():
    code_verifier = random_string(100)
    code = fetch_auth_code(code_verifier)
    bearer = fetch_bearer_token(os.environ['CAME_CONNECT_CLIENT_ID'], os.environ['CAME_CONNECT_CLIENT_SECRET'], code, code_verifier)
    return bearer['access_token']

def fetch_sites(token):
    headers = {"Authorization": "Bearer " + token}
    sites = requests.get(
        'https://app.cameconnect.net/api/sites', headers=headers)
    return sites.json()

def fetch_devices(token):
    sites = fetch_sites(token)
    return sites.get('Data')[0].get('Devices')

def fetch_device_statuses(token):
    ids = fetch_all_device_ids(token)
    headers = {"Authorization": "Bearer " + token}
    url = "https://app.cameconnect.net/api/devicestatus?devices=[{}]".format(",".join(ids))

    res = requests.get(url, headers=headers)
    return res.json()

def fetch_commands_for_device(token, device_id):
    headers = {"Authorization": "Bearer " + token}
    url = "https://app.cameconnect.net/api/multiio/{}/commands".format(device_id)
    commands = requests.get(url, headers=headers)
    return commands.json()

def run_command_for_device(token, device_id, command_id):
    headers = {"Authorization": "Bearer " + token}
    url = "https://app.cameconnect.net/api/multiio/{}/commands/{}".format(device_id, command_id)
    res = requests.post(url, headers=headers)
    return res.json()

def fetch_all_device_ids(token):
    devices = fetch_devices(token)
    ids = []
    for device in devices:
        ids.append(str(device.get('Id')))
    return ids

urls = (
    '/devices/(.*)/command/(.*)', 'devices_command'
)
app = web.application(urls, globals())

class devices_command:
    def GET(self, device_id, command_id):
        token = fetch_token()
        res = run_command_for_device(token, device_id, command_id)
        web.header('Content-Type', 'application/json')
        return json.dumps(res)

if __name__ == "__main__":
    # TODO: Check env vars
     app.run()
