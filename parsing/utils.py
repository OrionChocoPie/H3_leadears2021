import re
import requests
from bs4 import BeautifulSoup


def get_lat_lon(url):
    lat, lon = None, None

    html = requests.get(url).text
    soup = BeautifulSoup(html)

    quotes = soup.find_all("img", class_="_7a3fb80146--image--2X3m2")
    for quote in quotes:
        parts = quote.get("src").split("/?ll=")
        if len(parts) == 2:
            lon, lat = parts[1].split("&")[0].split(",")
            break

    return lat, lon


def get_lat_lon_extended(url):
    lat, lot = None, None

    html = requests.get(url).text
    soup = BeautifulSoup(html)

    lng_pattern = re.compile('"lng":\d{2}.\d+')
    lat_pattern = re.compile('"lat":\d{2}.\d+')
    for script in soup.find_all("script"):
        lng_text = lng_pattern.findall(str(script))
        lat_text = lat_pattern.findall(str(script))

        if lng_text != []:
            lng_text = lng_text[0]
            lat_text = lat_text[0]

            lot = lng_text.split(":")[1]
            lat = lat_text.split(":")[1]

    return lat, lot