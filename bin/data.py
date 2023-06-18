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


def data(args): 
    pdb_path = args[1]
    PDBDIR = f"{args[2]}/"    
    tag = args[3]
    filter = args[4]
    pdb = ""
    with open(pdb_path,"r") as r:
        pdb = r.read()        
    print(pdb,PDBDIR)        
    pla = pl.PdbLoader(pdb,PDBDIR,cif=False)    
    po = pla.load_pdb()
    gm = pg.GeometryMaker([po])    
    if filter == "PI": #pi electrons around phnylaline
        geos = ['CE2:CD1[aa|PHE]','CE2:CD2[aa|PHE]','CE2:CD1:CD2']
        df = gm.calculateGeometry(geos,log=0)
        print("----- filter -----")    
        df = df.loc[(df['occ_CE2:CD1:CD2'] == 1) ]
        df["KEY"] = df['info_CE2:CD1:CD2']
    elif filter == "TAU": #pi electrons around tyrosine
        geos = ['CA:N[aa|CYS]','CA:C','CA:N:C']
        #geos = ['CA:N','CA:C','CA:N:C']
        df = gm.calculateGeometry(geos,log=0)
        print("----- filter -----")    
        df = df.loc[(df['occ_CA:N:C'] == 1) ]
        df["KEY"] = df['info_CA:N:C']
    elif filter == "DATA": #pi electrons around tyrosine
        geos = ['CA:N','CA:C','CA:N:C']
        #geos = ['CA:N','CA:C','CA:N:C']
        df = gm.calculateGeometry(geos,log=0)
        print("----- filter -----")    
        df = df.loc[(df['occ_CA:N:C'] == 1) ]
        df["KEY"] = df['info_CA:N:C']
    elif filter == "PB": #peptide bond
    # split this into a data frame per row to save memory
        geos = ['C:N+1[aa|CYS]','C:CA','C:O','C:CA:N+1']
        #geos = ['C:N+1','C:CA','C:O','C:CA:N+1']
        df = gm.calculateGeometry(geos,log=0)
        print("----- filter -----")    
        df = df.loc[(df['occ_C:CA:N+1'] == 1) ]
        df["KEY"] = df['info_C:CA:N+1']
    
    for i, row in df.iterrows():            
        #print(row)
        row_df = pd.DataFrame([row])
        ky = row["KEY"]
        row_df.columns = df.columns
        print("-----------------")
        print(row_df)
        print("-----------------")
        file_outputcsv = f"data_{tag}_{filter}_{pdb}_{ky}.csv"        
        row_df.to_csv(file_outputcsv,columns=df.columns,index=False)
        print("Saved to", file_outputcsv)

#####################################################################################################                
if __name__ == "__main__":
    data(sys.argv)           





