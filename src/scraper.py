from pathlib import Path

import pandas as pd
import parsel

def parse_issue_page(html):
    sel = parsel.Selector(html)
    n = sel.xpath('//*[@id="panel-bib-links"]/p[2]/text()').get().split(' ')[0]
    right = sel.xpath('//*[@id="panel-bib-links"]/p[5]/a/text()').get()

    return {'n_pages': int(n), 'right': right}

def parse_list(html):
    sel = parsel.Selector(html)
    tr_sel_list = sel.css('.viewability-table tbody tr')
    issues = []
    for tr_sel in tr_sel_list:
        issue = {}
        print(tr_sel.css('a'))
        link = tr_sel.css('a').attrib['href']
        issue['link'] = link
        issue['id'] = link.split('/')[-1]
        issue['name'] = tr_sel.css('.IndItem::text').get()
        issues.append(issue)

    df = pd.DataFrame(issues)
    return df 

# def download_page(issue_id, n):
#     URL = 'https://babel.hathitrust.org/cgi/imgsrv/image?id={}&attachment=1&size=ppi%3A300&format=image%2Fjpeg&seq={}&tracker=D2%3A'
#     download_file(url, f"{product['jpgs']}/{i}.jpg")
