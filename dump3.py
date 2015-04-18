import requests  
from lxml import html  
import sys  
import urlparse

response = requests.get('http://ru.aliexpress.com/item/New-European-style-famous-classic-Fashion-Women-Ladies-Matching-Brand-Purse-Long-Leather-Handbags-Zipper-Top/1576292162.html')  
parsed_body = html.fromstring(response.text)

# Grab links to all images
images = parsed_body.xpath('//img/@src')  
if not images:  
    sys.exit("Found No Images")

# Convert any relative urls to absolute urls
images = [urlparse.urljoin(response.url, url) for url in images]  
print 'Found %s images' % len(images)

# Only download first 10
for url in images[0:20]:  
    r = requests.get(url)
    f = open('downloaded_images/%s' % (url.split('/')[-1]), 'w')
    f.write(r.content)
    f.close()