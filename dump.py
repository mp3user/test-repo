"""
dumpimages.py
    Downloads all the images on the supplied URL, and saves them to the
    specified output file ("/test/" by default)

Usage:
    python dumpimages.py http://example.com/ [output]
"""

from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

url = "http://www.aliexpress.com/snapshot/6088811040.html"
def main(url, out_folder="~/test/"):
    """Downloads all the images at 'url' to ~/test/"""
    soup = bs(urlopen(url))
    parsed = list(urlparse.urlparse(url))

    for image in soup.findAll("img"):
        print "Image: %(src)s" % image
        image_url = urlparse.urljoin(url, image['src'])
        filename = image["src"].split("/")[-1]
        outpath = os.path.join(out_folder, filename)
        urlretrieve(image_url, outpath)

def _usage():
    print "usage: python dumpimages.py http://example.com [outpath]"

if __name__ == "__main__":
    url = sys.argv[-1]
    out_folder = "~/test/"
    if not url.lower().startswith("http"):
        out_folder = sys.argv[-1]
        url = sys.argv[-2]
        if not url.lower().startswith("http"):
            _usage()
            sys.exit(-1)
    main(url, out_folder)