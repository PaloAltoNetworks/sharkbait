#!/usr/bin/env python3

import random
from random import randint
from time import sleep
from urllib.error import HTTPError
import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import urllib3
import logging
import logging.handlers

RANDOMNESS = 5
LOGFILE = '/tmp/sharkbait.log'

def get_malware_urls():
    urlhaus = "https://urlhaus-api.abuse.ch/v1/urls/recent/"
    url_list = []

    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(urlhaus, timeout=5, verify=False)
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

def get_payload(url):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, timeout=5, verify=False)
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as e:
        # print(e)
        status = 0
        pass
    except requests.exceptions.ChunkedEncodingError as e:
        # print(e)
        status = 0
        pass
    else:
        status = response.status_code

    return(status)


def get_logger():
    format = '%(asctime)s | %(levelname)s | %(message)s'
    # datefmt = '%b %d %H:%M:%S'
    logger = logging.getLogger('sharkbait_logger')
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=LOGFILE, 
        encoding='utf-8',
        when='D',
        interval=1, 
        backupCount=6
    )
    handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def main():
    logger = get_logger()
    urls = get_malware_urls()
    while True:
        num_urls = len(urls)
        random_url = urls[random.randint(0, (num_urls - 1))]
        result = get_payload(random_url)
        if result == 200:
            logger.warning(random_url + " | " + str(result) + " | " + "Malware download successful")
        elif result == 503:
            logger.info(random_url + " | " + str(result) + " | " + "Malware URL blocked")
        elif result == 404:
            logger.info(random_url + " | " + str(result) + " | " + "Not found")
        elif result == 0:
            logger.info(random_url + " | " + str(result) + " | " + "Malware download blocked")
        else:
            logger.info(random_url + " | " + str(result) + " | " + "Unknown error")
        sleep(random.randint(1, RANDOMNESS))


if __name__ == '__main__':
    main()
