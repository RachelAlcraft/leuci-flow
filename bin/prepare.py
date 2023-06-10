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


def slices(args): 
    pdb = args[1]
    PDBDIR = f"{args[2]}/"    
    print(pdb,PDBDIR)

    mman.MapsManager().set_dir(PDBDIR)
    print("Loading",pdb)
    pla = pl.PdbLoader(pdb,PDBDIR,cif=False)    
    po = pla.load_pdb()        
    ml = mman.MapsManager().get_or_create(pdb,file=1,header=1,values=1)
            
#####################################################################################################                
if __name__ == "__main__":
    slices(sys.argv)           





