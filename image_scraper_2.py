import re
from bs4 import *
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as BSHTML
import urllib

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    return urls

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    if os.path.isfile(filename) == True:
        pass
    else:
        # download the body of response by chunk, not immediately
        response = requests.get(url, stream=True)
        # get the total file size
        file_size = int(response.headers.get("Content-Length", 0))
        # get the file name
        #filename = os.path.join(pathname, url.split("/")[-1])
        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            for data in progress.iterable:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                progress.update(len(data))

def main(url, path):
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        print(img)
        #if "thumbs" in img:
            #download(img, path)

            
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)
    # response will be provided in JSON format
    return response.text

urls = []

def get_images(url):
    
    page = urllib.request.urlopen(url)
    soup = BSHTML(page)
    images = soup.findAll('img')

    
    for img in images:
        img_url = img.attrs.get("data-cbp-src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin("https://oceanexplorer.noaa.gov/", img_url)
        if 'okeanos' in img_url:
            urls.append(img_url)
        
        #try:
            #pos = img_url.index("?")
            #img_url = img_url[:pos]
        #except ValueError:
            #pass
        # finally, if the url is valid
        #if is_valid(img_url):
            #urls.append(img_url)
        
    #return urls
        

url = "https://oceanexplorer.noaa.gov/image-gallery/welcome.html"

get_images(url)

for url in urls:
    download(url, "seacreature_images")
    
'''    
def get_newspapers(url):
    page = urllib.request.urlopen(url)
    soup = BSHTML(page)
    images = soup.findAll('img')
    
    newspapers = []
    
    for a in soup.find_all('a', href=True):
        link_to_paper = a['href']
        if "photogallery.php?album" in link_to_paper:
            link_to_paper = "https://www.marinespecies.org/deepsea/" + link_to_paper
            newspapers.append(link_to_paper)
            
    newspapers = list(set(newspapers))
    
    for url in newspapers:
        main(url, "seacreature_images")
        
        #for url in newspapers:
           #main(url, "seacreature_images")

url = "https://oceanexplorer.noaa.gov/image-gallery/welcome.html#"

main(url, "seacreature_images")
'''
