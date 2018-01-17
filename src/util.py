import sys
from os.path import dirname, join as pjoin

def eprint(*args, **kwargs):
    """Print to STDERR (e.g. to inform user of progress)."""
    print(*args, file=sys.stderr, **kwargs)

def reldir(path):
    """Get a relative path from the current file."""
    return pjoin(dirname(__file__), path)
