import sys

def eprint(*args, **kwargs):
    """Print to STDERR (e.g. to inform user of progress)."""
    print(*args, file=sys.stderr, **kwargs)
