import requests

def ping_url(url):

    reqs = requests.get(url)

    return reqs.status_code