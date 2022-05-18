import json
from pathlib import Path

import pandas as pd
import requests
from src import scraper
from src.util import download_file


def download_list(product):
    URL = 'https://catalog.hathitrust.org/Record/007449702'
    r = requests.get(URL)
    Path(product).write_bytes(r.content)

def parse_list(upstream, product):
    html = Path(upstream['download_list']).read_text()
    df = scraper.parse_list(html)
    df.to_csv(product, index=False)

def parse_issue_page(upstream, product, issue_id):
    html = Path(upstream.first).read_text()
    page = scraper.parse_issue_page(html)
    page['id'] = issue_id
    Path(product).write_text(json.dumps(page))
    
def download_issue(upstream, product):
    URL = 'https://babel.hathitrust.org/cgi/imgsrv/image?id={}&attachment=1&size=ppi%3A300&format=image%2Fjpeg&seq={}&tracker=D2%3A'

    text = Path(upstream.first).read_text()
    issue = json.loads(text)
    for i in range(1, issue['n_pages'] + 1):
        url = URL.format(issue['id'], i)
        Path(product).mkdir(exist_ok=True)
        download_file(url, f"{product}/{i}.jpg")
