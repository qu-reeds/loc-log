from threading import Thread, enumerate
from requests import get
from time import sleep
from functools import reduce

UPDATE_INTERVAL = 0.01

class URLThread(Thread):
    def __init__(self, url):
        super(URLThread, self).__init__()
        self.url = url
        self.response = None

    def run(self):
        self.response = get(self.url)

def MultiGet(uris, timeout=1.5):
    """Send and collect responses on parallel GET requests."""
    def alive_count(lst):
        alive = map(lambda x: 1 if x.isAlive() else 0, lst)
        return reduce(lambda a,b: a+b, alive)
    threads = [URLThread(uri) for uri in uris]
    for thread in threads:
        thread.start()
    while alive_count(threads) > 0 and timeout > 0.0:
        timeout = timeout - UPDATE_INTERVAL
        sleep(UPDATE_INTERVAL)
    return [(x.url, x.response) for x in threads]

def GetLoci(IDs):
    """Build URLs from IDs and run GET requests on them."""
    loci_uris = [f"https://naivelocus.tumblr.com/post/{ID}/" for ID in IDs]
    got_loci = MultiGet(loci_uris)
    return got_loci
