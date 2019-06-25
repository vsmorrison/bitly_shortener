import requests
import argparse
from settings import TOKEN


def make_bitlink(token, target_link):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    json = {
        'long_url': target_link
    }
    response = requests.post(url, headers=headers, json=json)
    response.raise_for_status()
    return response.json()


def get_clicks(token, bitlink):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(bitlink)
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    payload = {
        'unit': 'day',
        'units': -1
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def check_link(token, link):
    link_start = 7
    link_end = 20
    if link.startswith('bit.ly', link_start, link_end):
        short_link = ''
        clicks = (get_clicks(token, link[link_start:]))
        return short_link, clicks
    else:
        short_link = make_bitlink(TOKEN, link)
        clicks = get_clicks(TOKEN, short_link['id'])
        return short_link['link'], clicks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='Ваша ссылка')
    args = parser.parse_args()
    try:
        short_link, clicks = check_link(TOKEN, args.link)
        print(short_link)
        print('Количество кликов: ', clicks['total_clicks'])
    except requests.exceptions.HTTPError as error:
        exit(error)

