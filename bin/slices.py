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
from leuci_xyz import matrix3d as d3

samples,width,depth_samples = 50,10,10        


def slices(args): 
    #slices.py data.csv /home/rachel/phd/leuci-async/leuci-flow/pdbdata 2d_im
    pdb_path = args[1]
    PDBDIR = f"{args[2]}/"
    d2or3 = args[3]    # possible modes are: 2d_np, 3d_np, 2d_im, 3d_im, 2d_im_nay
    tag = args[4]
    df = pd.read_csv(pdb_path)            
    print(df)
    mman.MapsManager().set_dir(PDBDIR)
    coords_list = []
    i_count = 0
    df_len = len(df.index)    
    for i, row in df.iterrows():
        pdb = row['pdb_code']
        atom_key = row['KEY']
        print("Loading",pdb)
        pla = pl.PdbLoader(pdb,PDBDIR,cif=False)    
        po = pla.load_pdb()

        atoms = row[atom_key]
        print(i_count, "/",df_len,i,atoms)
        i_count += 1
        clp = atoms.split("(")    
        cen = clp[1][:-1]
        lin = clp[2][:-1]
        pla = clp[3][:-1]
        cens = cen.split("|")
        lins = lin.split("|")
        plas = pla.split("|")
        #central_atom = "A:707@C.A"
        cen_str = cens[0]+":"+cens[2]+"@"+cens[3]+".A"
        lin_str = lins[0]+":"+lins[2]+"@"+lins[3]+".A"
        pla_str = plas[0]+":"+plas[2]+"@"+plas[3]+".A"
        
        coords_list.append((pdb,cen_str,lin_str,pla_str,atoms))
        print("Added",pdb,cen_str,lin_str,pla_str,atoms)  

        print(coords_list)

        interpolation = "linear"    
        
        count = 0
        for pdb,cen,lin,pla,atoms in coords_list:
            count += 1
            print(count, "/", len(coords_list),pdb,cen,lin,pla)
            
            ml = mman.MapsManager().get_or_create(pdb,file=1,header=1,values=1)
            if not ml.success():
                print(pdb, "has not loaded ccp4 succesfully")
            else:
                mf = mfun.MapFunctions(pdb,ml.mobj,ml.pobj,interpolation,as_sd=2)
                cc = v3.VectorThree().from_coords(ml.pobj.get_coords_key(cen))
                ll = v3.VectorThree().from_coords(ml.pobj.get_coords_key(lin))
                pp = v3.VectorThree().from_coords(ml.pobj.get_coords_key(pla))            
                title_key = f"{pdb}_{cen_str}_{lin_str}_{pla_str}"
                if "2d" in d2or3:
                    vals2d = mf.get_slice(cc,ll,pp,width,samples,interpolation,deriv=0,ret_type="3d")
                    if d2or3 == "2d_np":
                        # 2d plot (s)
                        filename = f"2d_matrices_{pdb}_{count}_{tag}"
                        np.save(filename,vals2d.get_as_np())
                    elif d2or3 == "2d_im":                                                                        
                        filename = f"2d_image_{pdb}_{count}_{tag}.html"            
                        mplot = mph.MapPlotHelp(filename)                                                                
                        mplot.make_plot_slice_2d(vals2d,min_percent=0.9,max_percent=0.9,samples=samples,width=width,title=title_key)
                    elif d2or3 == "2d_im_nay":
                        print("fetching neighbours...")
                        naybs = mf.get_slice_neighbours(cc,ll,pp,width,samples,[0,0.5],log_level=1)                        
                        print("...fetched neighbours")
                        filename = f"2d_image_{pdb}_{count}_{tag}_nay.html"            
                        mplot = mph.MapPlotHelp(filename)                                                                
                        mplot.make_plot_slice_2d(vals2d,min_percent=0.9,max_percent=0.9,samples=samples,width=width,title=title_key,naybs=naybs)                        
                elif "3d" in d2or3:
                    vals3d,coords = mf.get_slice(cc,ll,pp,width,samples,interpolation,deriv=0,depth_samples=depth_samples,ret_type="3d")                                
                    if d2or3 == "3d_np":
                        filename3 = f"3d_matrices_{pdb}_{count}_{tag}"                                                                        
                        np.save(filename3,vals3d.get_as_np())
                    elif d2or3 == "3d_im":
                        filename = f"3d_image_{pdb}_{count}_{tag}.html"            
                        mplot = mph.MapPlotHelp(filename)                                                                
                        mplot.make_plot_slice_3d(vals3d,min_percent=0.9,max_percent=0.9,title=title_key)        
            
                    

#####################################################################################################                
if __name__ == "__main__":
    slices(sys.argv)           





