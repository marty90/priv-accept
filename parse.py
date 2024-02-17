import json
import pandas as pd
from urllib.parse import urlparse


def extract_domain(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            return parsed_url.netloc
        else:
            return None
    except Exception:
        return None


def main():
    f = open('./output.json', 'r')
    data = json.load(f)
    df = pd.DataFrame(columns=['url', 'landing_page', 'has_found_banner',
                      'cookie_first', 'cookie_click', 'cookie_internal','domains_first','domains_click'])

    # parsing cookies data
    cookie_first = [{'domain': cookie['domain'], 'expires': cookie['expires'],
                     'size': cookie['size'], 'name': cookie['name']} for cookie in data['first']['cookies']['cookies']]
    cookie_click = [{'domain': cookie['domain'], 'expires': cookie['expires'],
                           'size': cookie['size'], 'name': cookie['name']} for cookie in data['second']['cookies']['cookies']]
    
    if data['internal'] is not None:
        cookie_internal = [{'domain': cookie['domain'], 'expires': cookie['expires'],
                                  'size': cookie['size'], 'name': cookie['name']} for cookie in data['internal']['cookies']['cookies']]
    else:
        cookie_internal = []

    # parsing domains
    domains_first = list({extract_domain(
        url) for url in data['first']['urls'] if extract_domain(url) is not None})
    domains_click = list({extract_domain(
        url) for url in data['click']['urls'] if extract_domain(url) is not None})
    
    new_row = {
    'url': data['stats']['target'],
    'landing_page': data['stats']['after-click-landing-page'],
    'has_found_banner': data['stats']['has-found-banner'],
    'cookie_first': cookie_first,
    'cookie_click': cookie_click,
    'cookie_internal': cookie_internal,
    'domains_first': domains_first,
    'domains_click': domains_click
}

    # Append the new row to the DataFrame
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv('./output.csv', index=False)

if __name__ == '__main__':
    main()
