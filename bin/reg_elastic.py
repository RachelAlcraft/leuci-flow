#! /usr/bin/env python

import sys
import numpy as np
from skimage import data, util, transform, feature, measure, filters, metrics
from leuci_geo import reportmaker as rm
import math
import pandas as pd
#https://github.com/almarklein/pyelastix
#https://elastix.lumc.nl/download.php
import pyelastix


def get_moon_data():
    ############################################################################
# Data generation
# For this example, we generate a list of slightly tilted noisy images.

    img = data.moon()

    angle_list = [0, 5, 6, -2, 3, -4]
    center_list = [(0, 0), (10, 10), (5, 12), (11, 21), (21, 17), (43, 15)]

    img_list = [transform.rotate(img, angle=a, center=c)[40:240, 50:350]
                for a, c in zip(angle_list, center_list)]
    
    img_list = [util.random_noise(filters.gaussian(im, 1.1), var=5e-4, rng=seed)
                for seed, im in enumerate(img_list)]
    
    return img_list


def registration(args):

    # we are going to build up a data type that has these:
    #file name, image array, corners, tilted image, other tilted image
     
    dims = args[1]
    tag = args[2]
    filter = args[3]    
    csv_path = args[4]    
    paths = args[5:]
    print(dir,dims,tag,filter)
    ############################################################################
    # Data generation
    # ---------------
    #
    # For this example, we generate a list of slightly tilted noisy images.
        
    #all_data_array = []
    orig_img_list = []
    orig_img_titles = []
    img_deformed = []    
    
    if filter == "DATA":
        orig_img_list = get_moon_data()
        for im in orig_img_list:
            orig_img_titles.append("moon")            
    else:
        print(csv_path)                        
        for p in paths:    
            print(p)
            p = p.replace("\\","")
            p = p.replace("\"","")
            p = p.replace("\"","")
            print(p)
            nams = p.split('_')
            ttl = nams[3]        
            with open(p, 'rb') as fnp:
                a = np.load(fnp)                
                orig_img_titles.append(ttl)
                orig_img_list.append(a)
                                    
    ref_img = orig_img_list[0].copy()

    # Get params and change a few values
    params = pyelastix.get_default_params()
    params.MaximumNumberOfIterations = 200
    params.FinalGridSpacingInVoxels = 10

    for i in range(0,len(orig_img_list)):
        im = orig_img_list[i]
        im1_deformed, field = pyelastix.register(ref_img, im, params)
        img_deformed.append(im1_deformed)
        
    # Set up the output report
    rep = rm.ReportMaker("leuci-flow image registration elastic",f"elastic_reg_{dims}_{tag}_{filter}.html",remove_strip=False,cols=3)
    rep.addBoxComment("Contour orig")
    rep.addBoxComment("Surface orig")
    rep.addBoxComment("Surface tilted")
    
    super_a = None
    def_a = None
    loaded = False
    for i in range(len(orig_img_list)):
        im = orig_img_list[i]
        def_img = img_deformed[i]                
        rep.addLineComment(orig_img_titles[i])
        if filter != "DATA":
            rep.addContours(im[:, :, 0],overlay=True,colourbar=False)
                        
        rep.addSurface(im)        
        rep.addSurface(def_img)

        if not loaded:
            super_a = im.copy()
            def_a = def_img.copy()
            loaded = True
        else:
            super_a += im.copy()
            def_a += def_img.copy()
        
            
    rep.addLineComment("Superposition")
    rep.changeColNumber(3)    
    rep.addSurface(def_a, title="elastic registration")
    rep.addBoxComment("")        
    rep.addSurface(super_a, title="simple superposition")
    
    
    rep.printReport()
    
#####################################################################################################                
if __name__ == "__main__":
    registration(sys.argv)  
