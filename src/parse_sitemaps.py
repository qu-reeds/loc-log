# parse naivelocus.com/sitemap.xml

import re
import requests
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
        UpdateMap(n, entries)
        return
    else:
        r.raise_for_status()

def ProcessSitemaps():
    """Initialise or update entries from sitemaps."""
    sitemaps = PullSiteMapURLs()
    for s in sitemaps:
        ProcessSitemap(s)
