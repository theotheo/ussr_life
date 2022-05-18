import pandas as pd

from ploomber import DAG
from ploomber.tasks import PythonCallable, TaskGroup, DownloadFromURL
from ploomber.products import File

from tasks.scrape import parse_issue_page, download_issue

# NOTE: you may add extra arguments to the function, they'll show up in the cli
def make():
    dag = DAG(executor='parallel')

    # name = 'download_list'
    # url = 'https://catalog.hathitrust.org/Record/007449702'
    # product_path = f'products/raw/list.html' 
    # download_list_task = DownloadFromURL(url, File(product_path), dag, name)
    

    # name = f'parse_list'
    # product_path = f'products/interim/list.csv'
    # parse_list_task = PythonCallable(parse_list, File(product_path), dag, name)
    
    df = pd.read_csv('products/interim/list.csv')

    for i, row in df.iterrows():
        url = row['link']
        issue_id = row['id']
        name = f'download_issue_page_{issue_id}'
        product_path = f'products/raw/pages/{issue_id}.html' 
        download_page_task = DownloadFromURL(url, File(product_path), dag, name)
        

        name = f'parse_issue_page_{issue_id}'
        product_path = f'products/interim/pages/{issue_id}.json' 

        parse_issue_page_task = PythonCallable(parse_issue_page, File(product_path), dag, name, params={'issue_id': issue_id})

        name = f'download_issue_{issue_id}'
        product_path = f'products/raw/issues/{issue_id}' 
        download_issue_task = PythonCallable(download_issue, File(product_path), dag, name)

        download_page_task >> parse_issue_page_task >> download_issue_task

    return dag


