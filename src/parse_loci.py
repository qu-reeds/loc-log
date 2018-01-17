# NB: 57171896200 is the first post ID using mdash as a source link signifier
from multi_get import GetLoci
from os import listdir as ls
from util import reldir
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs
from write_loc import WriteLocus

def GetAllLociIDs():
    """Read all the loci into a sorted array."""
    ids = []
    for tsv in ls(reldir('../log/map/')):
        ids.extend(pd.read_csv(reldir('../log/map/')+tsv, sep='\t').ID)
    ids.sort()
    return ids

def GetAllLoci():
    """Retrieve loci [HTML payloads]."""
    ids = GetAllLociIDs()
    loci = GetLoci(ids)
    return loci

def GetTwoLoci():
    """Debug: return just the first 2 from GetAllLoci."""
    ids = GetAllLociIDs()[0:2]
    loci = GetLoci(ids)
    return loci

# def GetTwentyNewLoci():
    # """Going slower: return a batch of 20 from GetAllLoci,
    # after verifying this does work for 2 with GetTwoLoci.
    # """
    # TODO: add a helper function to determine which IDs are still to come

def ProcessLoci(loci):
    for locus in loci:
        procloc = ProcessLocus(locus)
        WriteLocus(**procloc)
    return

def ProcessLocus(locus):
    """Retrieve title, source title, source URL, and whether DOI was found."""
    loc_id = locus[0].split('/')[4]
    s = BeautifulSoup(locus[1].content, "lxml").find('article')
    t = s.find('a', attrs={'class':'headlink'}).text
    p = s.find_all('p')[-1].find('a')
    src = p.text
    href = parse_qs(urlparse(p.get('href')).query)['z'][0]
    DOI = s.text.find('DOI') > -1
    doi = s.text.find('doi') > -1
    return {'ID': loc_id, 'title': t, 'source': src,
            'url': href, 'has_doi': DOI|doi}
