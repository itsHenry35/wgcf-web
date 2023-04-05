import requests
import subprocess
import random
import string
import datetime


def genstring(k):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))


def genkey():
    return subprocess.run(['wg', 'genkey'], capture_output=True).stdout.decode().strip()


def pubkey(privkey):
    return subprocess.run(['wg', 'pubkey'], input=privkey.encode(), capture_output=True).stdout.decode().strip()

def register(url, model, ua, apiversion):
  key1 = genkey()
  key = pubkey(key1)
  install_id = genstring(11)
  payload = {
        'key': key,
        'install_id': install_id,
        'fcm_token': f'{install_id}:APA91b{genstring(134)}',
        'referer': '1.1.1.1',
        'warp_enabled': True,
        'tos': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00'),
        'model': model,
        'type': 'Windows',
        'locale': 'en_US',
    }
  headers = {
        'User-Agent': ua,
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'api.cloudflareclient.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Length': '500',
    }
  result = requests.post(f'{url}/{apiversion}/reg', json=payload, headers=headers)
  return result.json(), key1


def get_config(account, privkey):
  return f"""[Interface]
PrivateKey = {privkey}
Address = {account['config']['interface']['addresses']['v4']}
Address = {account['config']['interface']['addresses']['v6']}
DNS = 1.1.1.1
DNS = 2606:4700:4700::1111

[Peer]
PublicKey = {account['config']['peers'][0]['public_key']}
Endpoint = {account['config']['peers'][0]['endpoint']['host']}
AllowedIPs = 0.0.0.0/0
AllowedIPs = ::/0"""

def get_wgcf(method, extra):
  baceurl = "https://api.cloudflareclient.com"
  apiversion = "v0a1922"
  Useragent = "okhttp/3.12.1"
  account, privatekey = register(baceurl, "Cloudflare Warp Web", Useragent, apiversion)
  accesstoken = account['token']

  match method:
    case "free":
      return get_config(account, privatekey)
    case "teams":
      raise Exception("Teams not supported yet!")
    case "plus":
      headers = {
        'User-Agent': Useragent,
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'api.cloudflareclient.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Authorization' : f'Bearer {accesstoken}',
        'Content-Type': 'application/json; charset=UTF-8',
      }
      payload = {
         "License": extra}
      id = account['id']
      result = requests.put(f'{baceurl}/{apiversion}/reg/{id}/account', json=payload, headers=headers).json()
      if "errors" in result:
        raise Exception(result["errors"])
      else:
        return get_config(account, privatekey)
    case _:
      return "Request invalid!"
    
if __name__ == '__main__':
  print(get_wgcf("plus", ""))