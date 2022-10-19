import requests
from bs4 import BeautifulSoup
import re

auth = ('qa', 'te5tc0munn1tyrock5')
url = 'http://198.199.91.139:8333'
expr = re.compile(r'build_(\d+).build$')


def get_subdirs_urls(url, **req_kwargs):
    resp = requests.get(url, **req_kwargs)
    if resp.ok:
        resp_text = resp.text
    else:
        resp.raise_for_status()
    soup = BeautifulSoup(resp_text, 'html.parser')
    dirs = [f'{url}/{x.get("href")}' for x in soup.findAll('a') if x.get('href').endswith('/')]
    return dirs


def get_latest_build_for_subdir(url, **req_kwargs):
    resp = requests.get(url, **req_kwargs)
    if resp.ok:
        resp_text = resp.text
    else:
        resp.raise_for_status()
    soup = BeautifulSoup(resp_text, 'html.parser')
    buids = [f'{url}{x.get("href")}' for x in soup.findAll('a') if x.get('href').endswith('build')]
    latest = max(buids, key=lambda x: int(expr.findall(x)[0]))
    return latest


def download_and_save_latest(url, **req_kwargs):
    # This is also a stub that will do everything in curdir and file name will match actual on remote
    resp = requests.get(url, auth=auth, stream=True)
    if resp.ok:
        with open(resp.url.split('/')[-1], 'wb+') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                f.write(chunk)
    else:
        resp.raise_for_status()


if __name__ == '__main__':
    print("This is just a sample")
    for x in get_subdirs_urls(url, auth=auth):
        download_and_save_latest(get_latest_build_for_subdir(x, auth=auth))
