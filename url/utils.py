import base64
import hashlib
from models import Url

def parseURL(url):    
    url = url.replace('https://www.','')
    url = url.replace('http://www.','')
    url = url.replace('https://','')
    url = url.replace('http://','')
    url = url.replace('www.','')
    url = url.replace('.com','')
    url = genURL(url)
    return url


def genURL(url):
    hasher = hashlib.sha1(url)
    return base64.urlsafe_b64encode(hasher.digest()[0:10])

def shortenURL(actualUrl):
    shortURL = parseURL(actualUrl)
    created = None
    try:
        objUrl = Url.objects.get(shortURL=shortURL)
        created = False
    except Url.DoesNotExist:
        objUrl = Url(actualUrl=actualUrl,shortURL=shortURL)
        objUrl.save()
        created = True    
    return created, shortURL

    