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


def data(args): 
    pdb_path = args[1]
    PDBDIR = f"{args[2]}/"    
    tag = args[3]   
    pdb = ""
    with open(pdb_path,"r") as r:
        pdb = r.read()        
    print(pdb,PDBDIR)        
    pla = pl.PdbLoader(pdb,PDBDIR,cif=False)    
    po = pla.load_pdb()
    gm = pg.GeometryMaker([po])
    geos = ['SG:{SG@1}[dis|<3.5]','SG:{(N),(O)}[dis|<3.5]','SG:{(N),(O)}:{SG@1}']
    df = gm.calculateGeometry(geos,log=0)
    print("----- filter -----")    
    df = df.loc[(df['occ_SG:{(N),(O)}:{SG@1}'] == 1) ]
    #file_outputcsv = f"sg_csv_{pdb}.csv"
    file_outputcsv = f"data_{tag}_{pdb}.csv"
    df["KEY"] = df['info_SG:{(N),(O)}:{SG@1}']
    df.to_csv(file_outputcsv)

    print("Saved to", file_outputcsv)

#####################################################################################################                
if __name__ == "__main__":
    data(sys.argv)           





