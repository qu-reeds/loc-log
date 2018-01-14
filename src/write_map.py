from os.path import dirname, join as pjoin, isdir, exists
from util import eprint
import pandas as pd

# n => map number (integer)
# entries => list of string pairs (URL, date last mod.)
def UpdateMap(n, entries):
    """Update the map directory corresponding to n,
    with the entries provided, if necessary."""
    map_dir = pjoin(dirname(__file__), '../log/map/')
    map_fname = pjoin(map_dir, f'{n}.tsv')
    if not isdir(map_dir):
        raise ValueError('Directory missing, cancelling.')
    if exists(map_fname):
        df = pd.read_csv(map_fname, sep='\t')
        if len(entries) == len(df.index):
            # no update to be made
            eprint(f"  - No new loci.")
            return
        else:
            # this is an update, check if entries are already on file
            up_df = pd.DataFrame([x for x in entries \
                    if x[0] not in list(df.ID)], \
                    columns=['ID', 'datetime'])
            eprint("  - Adding {len(up_df.index)} new loci to map '{n}'.")
            up_df.to_csv(map_fname, mode='a', sep='\t', \
                    index=False, encoding='utf-8', header=False)
    else:
        eprint(f"  - Writing {len(entries)} new loci to map '{n}'.")
        df = pd.DataFrame(entries, columns=['ID','datetime'])
        df.to_csv(map_fname, sep='\t', index=False, encoding='utf-8')
