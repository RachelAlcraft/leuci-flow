#! /usr/bin/env python

import sys
import os
from leuci_geo import pdbloader as pl
from leuci_geo import pdbgeometry as pg
from leuci_map import mapsmanager as mman
from leuci_map import mapfunctions as mfun
from leuci_xyz import vectorthree as v3
from leuci_map import mapplothelp as mph
import numpy as np
import pandas as pd


def dataall(args): 
    #$pdb_csvs $params.outcsv $params.set_tag $params.filter    
    CSVDIR = f"{args[1]}/"    
    tag = args[2]
    filter = args[3]
    pdb_csvs = args[4:]#args[1]
    print(pdb_csvs)
    pdb = ""
    dfs = []
    for pdb_csv in pdb_csvs:
        with open(pdb_csv,"r") as r:
            df = pd.read_csv(pdb_csv)
            dfs.append(df)

    df_res = pd.concat(dfs)
    file_outputcsv = f"all_data_{tag}_{filter}_{pdb}.csv"        
    df_res.to_csv(file_outputcsv,columns=df.columns,index=False)
    print("Saved to", file_outputcsv)
            
    
    

#####################################################################################################                
if __name__ == "__main__":
    dataall(sys.argv)           





