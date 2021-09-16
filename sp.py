import requests
from requests.auth import HTTPBasicAuth

cert = 'path\to\certificate.cer'
user = 'mine\spadmin'
password = 'StrongPassword123!@#'

response = requests.get(
    url=r'http://win-teuk71i0lth:24454/',
    auth=HTTPBasicAuth(user, password))

print(response.status_code)
