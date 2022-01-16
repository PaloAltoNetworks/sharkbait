#!/usr/bin/env python3

import random
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

    random.shuffle(url_list)
    return(url_list)


def main():
    urls = get_malware_urls()

    for url in urls:
        print("Downloading: " + url)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(http_err)
            pass
        except requests.exceptions.ConnectionError as conn_err:
            print(conn_err)
            pass
        sleep(5)


if __name__ == '__main__':
    main()