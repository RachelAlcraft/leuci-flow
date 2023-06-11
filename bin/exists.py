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


def exists(args): 
    pdb = args[1]
    PDBDIR = f"{args[2]}/"    
    filename = f"exists.csv"
    print(pdb,filename)

    mman.MapsManager().set_dir(PDBDIR)    
    pla = pl.PdbLoader(pdb,PDBDIR,cif=False)    
    po = pla.load_pdb()        
    ml = mman.MapsManager().get_or_create(pdb,file=1,header=1,values=1)
    if ml.success():
        with open(filename,"w") as f:
            f.write(pdb)        
            
#####################################################################################################                
if __name__ == "__main__":
    exists(sys.argv)           





