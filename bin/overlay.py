#! /usr/bin/env python

import sys
import glob
import numpy as np
from leuci_map import mapplothelp as mph
from leuci_xyz import matrix3d as d3


def overlay(args):
 
    dir = args[1]
    dims = args[2]
    paths = glob.glob(f"{dir}/{dims}_*.npy")

    samples,width,depth_samples = 50,10,10  


    outdir = f"image_overlay_{dims}.txt"
    outdirnp = f"image_overlay_{dims}"

    np_mat = np.array([0])

    with open(outdir,"w") as f:
        f.write(dir + "\n")
        for p in paths:    
            with open(p, 'rb') as fnp:
                a = np.load(fnp)
                if np_mat.shape == (1,):
                    np_mat = a
                else:
                    np_mat += a
                f.write(p + "\n")
    np.save(outdirnp,np_mat)
    filename = f"image_overlay_{dims}.html"
    mplot = mph.MapPlotHelp(filename)                
    np_d3 = d3.Matrix3d(1,1,1)
    np_d3.set_from_np(np_mat)
    print(np_d3)
    if dims == "2d":
        mplot.make_plot_slice_2d(np_d3,min_percent=0.9,max_percent=0.9,samples=samples,width=width,title="overlay 2d")
    elif dims == "3d":
        mplot.make_plot_slice_3d(np_d3,min_percent=0.9,max_percent=0.9,title="overlay 3d")        
#####################################################################################################                
if __name__ == "__main__":
    overlay(sys.argv)  


        

