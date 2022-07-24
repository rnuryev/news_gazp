from csv import excel
from statistics import mode
import requests
from lxml import etree, html
from datetime import datetime
import itertools
import time
import pathlib


def get_news(url, attempts=5):
    news_list = []
    attempt = 0
    while attempt < attempts:
        try:
            page = requests.get(url)
        except:
            attempt += 1
            time.sleep(3)
            continue
        break
    root = html.fromstring(page.content.decode('utf-8'))
    tree = etree.ElementTree(root)
    xpath_list = []

    for e in root.iter():
        xpath_list.append(tree.getpath(e))
    news_xpath_list = []
    date = '2012/1/2/'
    for path in xpath_list:
        result = tree.xpath(path)
        if result[0].get('class'):
            if ('news-listing__item' in result[0].get('class')) and ('h3' in path):
                news_xpath_list.append(path)
            elif ('news-listing__day-date' in result[0].get('class')) and ('h2' in path):
                date = result[0].text
        else:
            continue
    for path in news_xpath_list:
        result = tree.xpath(path)
        value = result[0].text
        if value:
            news_list.append((date, value))
        else:
            news_list.append((date, ''))
    return news_list


def get_url_list():
    url_list = []
    
    years = [str(year) for year in range(2012, datetime.now().year + 1, 1)]
    months = [str(mnt) for mnt in range(1, 13, 1)]
    days = [str(day) for day in range(1, 32, 1)]

    for y, m, d in itertools.product(years, months, days):
        if (int(y) == datetime.now().year) \
                    and (int(m) == datetime.now().month) \
                        and (int(d) == datetime.now().day):
                    break
        else:
            url_list.append(f'https://www.mk.ru/news/{y}/{m}/{d}/')
    return url_list

def news_parse(target_folder, file_name, urls, timeout_evry_url=20):
    
    folder_path = pathlib.Path(target_folder)
    folder_path.mkdir(parents=True, exist_ok=True)
    
    file_path = folder_path / file_name
    
    # with open(file_path, 'w', encoding='utf-8') as f:
    #     f.write('date;title')
    #     f.write('\n')
    
    url_count = 0
    total_count = 0
    
    for url in urls:
        news = get_news(url)
        
        url_count += 1
       
        with open(file_path, 'a', encoding='utf-8') as f:
            for row in news:
                try:
                    f.write(';'.join(row))
                    f.write('\n')
                except TypeError as e:
                    print(f'Error on row: {row}')
                    raise e
        
        total_count += url_count
        
        print(f'Обработано ссылок: {url_count} из {len(urls)}')

        if total_count % timeout_evry_url == 0:
            time.sleep(3)
    
        
if __name__ == '__main__':
    
    target_folder = 'data'
    file_name = 'news.csv'
    
    
    url_list = get_url_list()
    
    news_parse(target_folder, file_name, url_list[len(url_list)-30:], 50)



