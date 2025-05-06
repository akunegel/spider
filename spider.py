import sys, os
from parsing import parseArgs
from scrape import scrapePage, recursiveScrape

def spider() -> list:
    """
        The spider program allow you to extract all the images from a website, recursively, by providing a url as a parameter.
        Usage : python3 spider.py [-rlp] URL
        
        Flags :
            -r : recursively downloads the images in a URL received as a parametere.
            -l [N] : indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
            -p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
        
        By default, the program will download the following extensions : jpg/jpeg, png, gif, bmp.
    """
    args = sys.argv
    flags, url, r, path, recursive = parseArgs(args)

    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Created download directory at: {path}")
        except Exception as e:
            print(f"Failed to create directory {path}.")
            exit(1)

    if (recursive == False):
        scrapePage(url, path)
    else:
        flags.remove('r')
        recursiveScrape(url, path, flags, int(r))

if __name__ == "__main__":
    spider()