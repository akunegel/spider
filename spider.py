from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from tqdm import tqdm
import requests
import os
import time
import sys
import urllib.parse

def parseArgs() -> tuple:
    flags = []
    path = "./data/"
    l = 5
    i = 1
    url = sys.argv[-1]
    
    while i < len(sys.argv) - 1:
        arg = sys.argv[i]
        if arg.startswith('-'):
            if 'p' in arg and 'l' in arg:
                print("Error: -p and -l cannot be in the same flag argument.")
                exit(1)
                
            skip_to_next = False
            
            for j in range(1, len(arg)):
                flag = arg[j]
                if flag not in 'rlp':
                    print("Error: flag not recognized, only -r, -l, -p allowed.")
                    exit(1)
                if flag in flags:
                    print(f"Error: duplicate flag -{flag} detected.")
                    exit(1)
                    
                flags.append(flag)
                
                if flag == 'p':
                    if i + 1 >= len(sys.argv) - 1 or sys.argv[i + 1].startswith('-'):
                        print("Error: argument for -p not found or path is missing. Must follow directly after -p.")
                        exit(1)
                    path = sys.argv[i + 1]
                    i += 1
                    skip_to_next = True
                    
                elif flag == 'l':
                    if i + 1 >= len(sys.argv) - 1 or sys.argv[i + 1].startswith('-'):
                        print("Error: argument for -l not found or path is missing. Must follow directly after -l.")
                        exit(1)
                    try:
                        l = int(sys.argv[i + 1])
                    except ValueError:
                        print("Error: argument for -l must be a number.")
                        exit(1)
                    i += 1
                    skip_to_next = True
            
            if skip_to_next:
                continue
            
        i += 1
    
    return flags, path, l, url


def spider():
    """
        The spider program allow you to extract all the images from a website, recursively, by providing a url as a parameter.
        Usage : python3 spider.py [-rlp] URL
        
        Flags :
            -r : recursively downloads the images in a URL received as a parametere.
            -l [N] : indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
            -p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
        
        To use -p and -l flags, both must be following different '-' and followed by their respective argument.
        By default, the program will download the following extensions : jpg/jpeg, png, gif, bmp.
    """
    
    if (len(sys.argv) == 1):
        print("Expected an URL as argument. Usage : python3 spider.py [-rlp] URL ")
        exit(1)
    
    flags, path, l, url = parseArgs()
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

    try:
        request = Request(url, headers=headers)
        html = urlopen(request)
        bs = BeautifulSoup(html.read(), 'html.parser')
        
        img_tags = bs.find_all('img')
        print(f"Found {len(img_tags)} image tags")
        
        count = 0
        
        for img in tqdm(img_tags):
            img_url = None
            for attr in ['src', 'data-src', 'data-original', 'data-lazy-src']:
                if img.get(attr):
                    img_url = img.get(attr)
                    break
            
            if not img_url:
                continue
                
            if img_url.startswith('/'):
                parsed_url = urllib.parse.urlparse(url)
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                img_url = base_url + img_url
            elif not img_url.startswith(('http://', 'https://')):
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                else:
                    parsed_url = urllib.parse.urlparse(url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    base_path = parsed_url.path
                    if '.' in base_path.split('/')[-1]:
                        base_path = '/'.join(base_path.split('/')[:-1]) + '/'
                    else:
                        if not base_path.endswith('/'):
                            base_path += '/'
                    img_url = urllib.parse.urljoin(base_url + base_path, img_url)
            
            image_name = os.path.basename(urllib.parse.urlparse(img_url).path)
            if not image_name:
                image_name = f"image_{count}.jpg"
            
            supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            file_ext = os.path.splitext(image_name)[1].lower()
            
            if not file_ext or file_ext not in supported_extensions:
                image_name = f"image_{count}.jpg"
            
            try:
                response = requests.get(img_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    file_path = os.path.join(path, image_name)
                    
                    base_name, ext = os.path.splitext(image_name)
                    counter = 1
                    while os.path.exists(file_path):
                        file_path = os.path.join(path, f"{base_name}_{counter}{ext}")
                        counter += 1
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded: {image_name}")
                    count += 1
                else:
                    print(f"Failed to download {img_url}: Status code {response.status_code}")
                    
            except Exception as e:
                print(f"Error downloading {img_url}: {e}")
                
        print(f"Successfully downloaded {count} images to {path}")
        
    except Exception as e:
        print(f"Error accessing URL: {e}")

if __name__ == "__main__":
    spider()