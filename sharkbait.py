#!/usr/bin/env python3

from time import sleep
from urllib.error import HTTPError
import requests

def get_malware_urls():
    urlhaus = "https://urlhaus-api.abuse.ch/v1/urls/recent/"
    url_list = []

    try:
        response = requests.get(urlhaus)
        response.raise_for_status()
        jsonResponse = response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    for x in jsonResponse['urls']:
        url_list.append(x['url'])

    return(url_list)


def main():
    urls = get_malware_urls()

    for url in urls:
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise SystemExit(err)
        sleep(5)


if __name__ == '__main__':
    main()