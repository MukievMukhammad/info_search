import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import datetime
import os, os.path


def has_1000_words(text):
    text = text.replace('\n', ' ').replace('\r', '')
    return len(text.split()) >= 1000

def get_domain(ref):
    url_component = ref.split('/')
    return url_component[0] + '//' + url_component[2] + '/'

def get_inside_links(url):
    domain = get_domain(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    hrefs = []
    for a in soup.find_all(u'a'):
        try:
            if a.attrs:
                hrefs.append(a.attrs['href'])
        except Exception as e:
            print(e)
    # filter inside links
    links = list(filter(
        lambda ref:
        ref.startswith(domain) or
        ref.startswith('/'),
        hrefs))
    # "/some_link" -> "http://domain.com/some_link"
    for i in range(0, len(links)):
        if links[i].startswith('/'):
            links[i] = domain + links[i][1:]
    return links

def get_content(url):
    resp = requests.get(url)
    if 'pdf' in resp.headers['Content-Type']:
        return ''
    html = resp.text
    soup = BeautifulSoup(html)
    content = soup.text
    # remove new lins
    content = re.sub(r'\n\s*\n', r'\n', content.strip(), flags=re.M)
    return content

def is_100_pages(dir):
    return 100 < len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])

def mkdir_for_pages():
    new_dir = "./%s" % datetime.datetime.now()
    Path(new_dir).mkdir(parents=True, exist_ok=True)
    return new_dir


urls = ['https://news.tsu.ru/news/', 'https://kpfu.ru', 'https://mipt.ru/']

if __name__ == "__main__":
    new_dir = mkdir_for_pages()
    visited = []
    not_visited_urls = set([])
    idx = 0
    while True:
        if not not_visited_urls:
            not_visited_urls = set(urls) - set(visited)
        if is_100_pages(new_dir):
            break
        try:
            to_visit = not_visited_urls.pop()
        except Exception as e:
            print(e)
            break
        content = get_content(to_visit)
        visited.append(to_visit)
        urls += get_inside_links(to_visit)
        urls = list(set(urls))
        if(not has_1000_words(content)):
            # urls.remove(to_visit)
            continue
        # if len(urls) < 100:
        #     urls += get_inside_links(to_visit)
        #     urls = list(set(urls))
        txt_name = '%s.txt' % idx
        with open('./' + new_dir + '/' + txt_name, 'a') as f:
            f.write(content)

        with open('./' + new_dir + '/' + 'index.txt', 'a') as f:
            f.write('%s %s\n' % (idx, to_visit))

        idx += 1
