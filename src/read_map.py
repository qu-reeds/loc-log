from os import listdir
from util import reldir
import pandas as pd
from datetime import datetime as dt

def GetLocDate(loc_id):
    """Retrieve the date for a given locus."""
    for tsv in listdir(reldir('../log/map/')):
        tsvpath = reldir('../log/map/') + tsv
        df = pd.read_csv(tsvpath, sep='\t')
        if loc_id in list(df.ID):
            d = df.loc[df['ID'] == loc_id].datetime
            if len(d) > 1:
                raise ValueError(f"Duplicate loci found: {loc_id}")
            t = dt.strptime(d.tolist()[0].split('T')[0], "%Y-%m-%d")
            return t.year, t.month, t.day
