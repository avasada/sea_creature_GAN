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
        if "thumbs" in img:
            download(img, path)

            
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)
    # response will be provided in JSON format
    return response.text
    
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
        

get_newspapers('https://www.marinespecies.org/deepsea/photogallery.php')
    

'''
# import necessary libraries
import re
from bs4 import *
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

'''
'''
#download images from each url
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
        #if str('jp2') in str(img):
        # for each image, download it
        download(img, path)
'''

'''
# function to extract html document from given url
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)
    # response will be provided in JSON format
    return response.text
  

def get_newspapers(url):
    url_to_scrape = url
    # create document
    html_document = getHTMLdocument(url_to_scrape)
    # create soap object
    soup = bs(html_document, 'html.parser')
  
    newspapers = []
    
    for link in soup.find_all('a'):
    #<a href="photogallery.php?album=4281"><img class="photogallery_thumb" src="https://images.marinespecies.org/thumbs/80781_porifera.jpg?w=150" width="150" height="113" style="border-width: 0px;" alt="Porifera" title="Porifera"><br></a>
        # display the actual urls
        link_to_paper = link.get('src')
        #if "images.marinespecies.org/thumbs" in link_to_paper:
            #newspapers.append(link_to_paper)
        print(link_to_paper)
        #print(link.get('href'))

    #remove duplicate links because for soem reason 2 of eahc were downloaded
    newspapers = list(set(newspapers))
    for url in newspapers:
        main(url, "seacreature_images")

get_newspapers('https://www.marinespecies.org/deepsea/photogallery.php')
'''
'''
 
urls_to_scrape = ['https://www.marinespecies.org/deepsea/photogallery.php']

for url in urls_to_scrape:
    get_newspapers(url)
'''
'''
#download images from each url
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
        download(img, path)
  

urls_to_scrape = ['https://www.marinespecies.org/deepsea/photogallery.php?album=3680']

# function to extract html document from given url
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)
    # response will be provided in JSON format
    return response.text
  

def get_newspapers(url):
    url_to_scrape = url
    # create document
    html_document = getHTMLdocument(url_to_scrape)
    # create soap object
    soup = bs(html_document, 'html.parser')
  
    newspapers = []
    
    for link in soup.find_all('img'):
        # display the actual urls
        link_to_paper = link.get('href')
        newspapers.append(link_to_paper)
        #print(link.get('href'))

    #remove duplicate links because for soem reason 2 of eahc were downloaded
    newspapers = list(set(newspapers))
    for url in newspapers:
        main(url, "seacreature_images")
 
for url in urls_to_scrape:
    get_newspapers(url)
    #get/download images
'''