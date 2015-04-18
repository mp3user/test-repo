import requests  
from lxml import html  
import sys  
import urlparse

response = requests.get('http://www.ebay.com/itm/60-Sticks-VANILLA-Darshan-Incense-SPREADING-LOVE-CHARM-Fragrance-of-India/110956010840?_trksid=p2047675.c100005.m1851&_trkparms=aid%3D222007%26algo%3DSIC.MBE%26ao%3D1%26asc%3D23772%26meid%3D7849502070513636948%26pid%3D100005%26prg%3D10164%26rk%3D2%26rkt%3D6%26sd%3D310989119280&rt=nc')  
parsed_body = html.fromstring(response.text)


images = parsed_body.xpath('//img/@src')  
if not images:  
    sys.exit("Found No Images")


images = [urlparse.urljoin(response.url, url) for url in images]  
print 'Found %s images' % len(images)

for url in images[0:25]:  
    r = requests.get(url)
    f = open('downloaded_images/%s' % url.split('/')[-1], 'w')
    f.write(r.content)
    f.close()