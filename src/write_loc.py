from os.path import join as pjoin, isdir, exists
from os import makedirs
from read_map import GetLocDate
from util import reldir, eprint
import pandas as pd

def WriteLocus(ID, title, source, url, has_doi):
    """Update the locus directory corresponding to n,
    with the entries provided, if necessary.
    """
    loc_y, loc_m, _ = GetLocDate(int(ID))
    if loc_m < 10: loc_m = '0' + str(loc_m)
    else: loc_m = str(loc_m)
    loc_y_dir = reldir(f'../log/loci/{loc_y % 100}')
    loc_m_dir = pjoin(loc_y_dir, loc_m)
    loc_meta = pjoin(loc_m_dir, 'loci.tsv')
    code_def = WriteLocus.__code__
    col_names = list(code_def.co_varnames)[0:code_def.co_argcount]
    if not isdir(loc_y_dir):
        makedirs(loc_y_dir)
    if not isdir(loc_m_dir):
        makedirs(loc_m_dir)
        col_header = '\t'.join(col_names)
        with open(loc_meta, 'w') as f:
            f.write(col_header + '\n')
    # check if locus is already on file
    df = pd.read_csv(loc_meta, sep='\t')
    if int(ID) not in list(df.ID):
        dset = [ID, title, source, url, str(has_doi)]
        up_df = pd.DataFrame([dset], columns=col_names)
        up_df.to_csv(loc_meta, mode='a', sep='\t', \
                index=False, encoding='utf-8', header=False)
