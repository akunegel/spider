import requests, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
visited = set()

def recursiveScrape(url, path, flag, depth):
    if depth == 0 or url in visited:
        return
    
    visited.add(url)
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except:
        print(f"Error: Failed to fetch {url}.")
        return
    
    scrapePage(url, path)

    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.find_all('a', href=True):
        link = a['href']
        full_link = urljoin(url, link)
        parsed = urlparse(full_link)

        if parsed.scheme in ['http', 'https'] and full_link not in visited:
            recursiveScrape(full_link, path, flag, depth - 1)


def scrapePage(url, path):
    
    try:
        r = requests.get(url=url, headers=headers, timeout=10)
        r.raise_for_status()
    except:
        print(f'Error : failed fetching site {url}.')
        exit(1)

    soup = BeautifulSoup(r.content, "html.parser")
    images = soup.find_all("img")

    for image in images:
        src_url = image.get('src')
        if not src_url:
            continue

        full_url = urljoin(url, src_url)

        try:
            img = requests.get(full_url, headers=headers, timeout=10)
            img.raise_for_status()

            filename = os.path.basename(urlparse(full_url).path)
            if not filename:
                filename = 'image_' + str(hash(full_url)) + '.jpg'

            file_path = os.path.join(path, filename)
            with open(file_path, 'wb') as f:
                for chunk in img.iter_content(1024):
                    f.write(chunk)
            
            print(f'Downloaded {src_url} successfully')

        except:
            print(f'Error : failed downloading {src_url}')


        


