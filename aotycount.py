#!/usr/bin/env python3

import sys
from collections import defaultdict
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def main(year: str) -> None:
    item_count = defaultdict(list)
    spellings = dict()
    for list_url in aoty_lists(year):
        for item, list_title in aoty_list(list_url):
            print(list_title)
            # Save the first spelling
            if item not in spellings:
                spellings[item.lower()] = item
            item_count[item.lower()].append(list_title)
    for name in sorted(item_count.keys(), reverse=True, key=lambda k: len(item_count[k])):
        lists = item_count[name]
        print(f"[{len(lists)}] {spellings[name]} [{', '.join(lists)}]")


def aoty_lists(year: str) -> list[str]:
    url = 'https://aoty.hubmed.org/'
    soup = _get(url)
    for el in soup.select('.item .meta a'):
        if el.text.startswith(year):
            yield urljoin(url, el.attrs['href'])


def aoty_list(url: str) -> list[str]:
    soup = _get(url)
    title = soup.select_one('a.title').text
    for el in soup.select('.albumlist li'):
        [artist, album] = el.select("span[itemprop='name']")
        yield f"{artist.text} - {album.text}", title


def _get(url: str) -> requests.Response:
    html = requests.get(url).text
    return BeautifulSoup(html, 'html.parser')


if __name__ == "__main__":
    year = sys.argv[1]
    main(year)
