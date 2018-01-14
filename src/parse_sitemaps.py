# parse naivelocus.com/sitemap.xml

import time
import re
import requests
from util import eprint
from bs4 import BeautifulSoup as bs
from write_map import UpdateMap

def PullSitemapURLs():
    """Get all sitemaps for naivelocus.com."""
    r = requests.get('http://naivelocus.com/sitemap.xml')
    if r.status_code == 200:
        soup = bs(r.content, features="xml")
        locs = [x.text for x in soup.find_all('loc')]
        return locs
    else:
        r.raise_for_status()

def ProcessSitemap(url):
    """Retrieve URL and date for all entries in sitemap."""
    n = re.findall(r'(\d+)\.xml', url)[0]
    r = requests.get(url)
    if r.status_code == 200:
        soup = bs(r.content, features="xml")
        entries = [(x.find('loc').text.split('/')[4], x.find('lastmod').text) \
            for x in soup.find_all('url') if x.find('changefreq') is None]
        eprint(f"  - {len(entries) loci found}")
        UpdateMap(n, entries)
        return
    else:
        r.raise_for_status()

def ProcessSitemaps():
    """Initialise or update entries from sitemaps."""
    start_t = time.time()
    sitemaps = PullSitemapURLs()
    eprint(f"Found {len(sitemaps)} maps.")
    for i in range(0, len(sitemaps)):
        eprint(f"Processing map {i+1}:")
        ProcessSitemap(sitemaps[i])
    eprint(f"Done (in {round(time.time() - start_t)} seconds).")
