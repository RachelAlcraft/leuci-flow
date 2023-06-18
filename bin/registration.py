#! /usr/bin/env python

import sys
import numpy as np
from skimage import data, util, transform, feature, measure, filters, metrics
from leuci_geo import reportmaker as rm
import math
import pandas as pd


def match_locations(img0, img1, coords0, coords1, radius=5, sigma=3):    
    y, x = np.mgrid[-radius:radius + 1, -radius:radius + 1]
    weights = np.exp(-0.5 * (x ** 2 + y ** 2) / sigma ** 2)
    weights /= 2 * np.pi * sigma * sigma

    match_list = []
    for r0, c0 in coords0:
        roi0 = img0[r0 - radius:r0 + radius + 1, c0 - radius:c0 + radius + 1]
        roi1_list = [img1[r1 - radius:r1 + radius + 1,
                          c1 - radius:c1 + radius + 1] for r1, c1 in coords1]
        # sum of squared differences
        ssd_list = [np.sum(weights * (roi0 - roi1) ** 2) for roi1 in roi1_list]
        match_list.append(coords1[np.argmin(ssd_list)])

    return np.array(match_list)

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
    orig_corners_list = []
    super_a = None
    loaded = False
    if filter == "DATA":
        orig_img_list = get_moon_data()
        for im in orig_img_list:
            orig_img_titles.append("moon")
            if not loaded:
                super_a = im.copy()
                loaded = True
            else:
                super_a += im.copy()
    else:
        print(csv_path)
        #img_list = []
        
        
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
                if not loaded:
                    super_a = a.copy()
                    loaded = True
                else:
                    super_a += a.copy()
                orig_img_titles.append(ttl)
                orig_img_list.append(a)
                
                
    #ref_img = img_list[0].copy()
    ref_img = orig_img_list[0].copy()
    
    
    maxmax = -100
    minmin = 100
    for imm in orig_img_list:        
        maxmax = max(maxmax,imm.max())
        minmin = min(minmin,imm.min())

    data_range = maxmax-minmin

    psnr_ref = metrics.peak_signal_noise_ratio(ref_img, orig_img_list[0],data_range=data_range)

    ############################################################################
    # Image registration
    # ------------------
    #
    # .. note::
    #    This step is performed using the approach described in
    #    :ref:`sphx_glr_auto_examples_transform_plot_matching.py`, but any other
    #    method from the :ref:`sphx_glr_auto_examples_registration` section can be
    #    applied, depending on your problem.
    #
    # Reference points are detected over all images in the list.

    min_dist = 5
    #corner_list = []
    for i in range(len(orig_img_list)):
        img = orig_img_list[i]
        harris_img = feature.corner_harris(img)
        print("----- CORNERS -----")        
        corners = feature.corner_peaks(harris_img, threshold_rel=0.001, min_distance=min_dist)        
        print(corners)                
        # make corners up
        if filter == "DATA":
            orig_corners_list.append(corners)
        else:
            fake_corners=np.array([[25,25],[25,28],[24,26]])        
            orig_corners_list.append(fake_corners)
        
        
    
    

    

    ############################################################################
    # The Harris corners detected in the first image are chosen as
    # references. Then the detected points on the other images are
    # matched to the reference points.

    img0 = orig_img_list[0]
    coords0 = orig_corners_list[0]
    #for i in range(len(orig_img_list)):        
    #    coords1 = orig_corners_list[i]
    #    if len(coords1)> 1:
    #        coords0 = all_data_array[i][2]
    #        img0 = all_data_array[0][1]
    #        break
    
    orig_matching_corners = []
    for i in range(len(orig_img_list)):
        img1 = orig_img_list[i]
        coords1 = orig_corners_list[i]
        mc = match_locations(img0, img1, coords0, coords1, min_dist)        
        orig_matching_corners.append(mc)        
        #for mmc in mc:
        #    print(type(mmc),mmc.shape,mmc,)
        
    ############################################################################
    # Once all the points are registered to the reference points, robust
    # relative affine transformations can be estimated using the RANSAC method.
    src = np.array(coords0)
        
    orig_trfm_list = []
    count = 0
    #for dst in matching_corners:
    for i in range(len(orig_img_list)):
        print(i,"ransac")
        #dst = np.array(orig_matching_corners[i])
        dst = orig_matching_corners[i]
        try:                        
            rnsc = measure.ransac((dst, src),transform.EuclideanTransform, min_samples=2,residual_threshold=2, max_trials=100)                
            if rnsc[0] is not None:
                print("...",i,"ransac",rnsc[0])
                orig_trfm_list.append(rnsc[0].params)
                #trfm_list.append(rnsc[0].params)            
            else:
                print("...",i,"ransac none")
                orig_trfm_list.append(np.array([float("Nan")]))
                #trfm_list.append(np.array([float("Nan")]))
        except Exception as e:
            #trfm_list.append(np.array([float("Nan")]))
            print("...",i,e,"ransac")
            orig_trfm_list.append(np.array([float("Nan")]))
        
        count += 1

        
    #fig, ax_list = plt.subplots(len(img_list), 2, figsize=(9,2*len(img_list)), sharex=True, sharey=True)
    #im_zipped = zip(img_list, trfm_list)

    bad_titles = []
    bad_images = []

    # Set up the output report
    rep = rm.ReportMaker("leuci-flow image registration",f"image_reg_{dims}_{tag}_{filter}.html",remove_strip=False,cols=3)
    rep.addBoxComment("Contour orig")
    rep.addBoxComment("Surface orig")
    rep.addBoxComment("Surface tilted")
    
    #for idx, (im, trfm) in enumerate(im_zipped):
    for i in range(len(orig_img_list)):
        im = orig_img_list[i]
        trfm = orig_trfm_list[i]
        coords = orig_corners_list[i]
        mcoords = orig_matching_corners[i]
        
        if not math.isnan(trfm.max()):
            try:
                tr_im = transform.warp(im, trfm)
                print(i,len(tr_im[0]))             
                rep.addLineComment(orig_img_titles[i])
                if filter != "DATA":
                    rep.addContours(im[:, :, 0],overlay=True,colourbar=False)
                
                rep.addPoints2d([coords],overlay=True,hue="limegreen")
                rep.addPoints2d([mcoords],overlay=False,hue="cyan")
                rep.addSurface(im)        
                rep.addSurface(tr_im)
                #good_images.append(all_data_array[i])
            except Exception as e:
                print("error tilting",i,e)
                bad_images.append(im)
                bad_titles.append(orig_img_titles[i])
        else:
            bad_images.append(im)
            bad_titles.append(orig_img_titles[i])
        

    ############################################################################
    # Image assembling
    # ----------------
    #
    # A composite image can be obtained using the positions of the
    # registered images relative to the reference one. To do so, we define
    # a global domain around the reference image and position the other
    # images in this domain.
    #
    # A global transformation is defined to move the reference image in the
    # global domain image via a simple translation:
    margin = 50
    try:
        height, width,depth = ref_img.shape
    except:
        height, width = ref_img.shape
    out_shape = height + 2 * margin, width + 2 * margin
    glob_trfm = np.eye(3)
    glob_trfm[:2, 2] = -margin, -margin

    ############################################################################
    # Finally, the relative position of the other images in the global
    # domain are obtained by composing the global transformation with the
    # relative transformations:
    rep.addLineComment("Superposition")
    rep.changeColNumber(3)
    if len(bad_images) != len(orig_img_list):
        global_img_list = []
        for i in range(len(orig_img_list)):
            img = orig_img_list[i]
            trfm = orig_trfm_list[i]
            try:
                warped = transform.warp(img, trfm.dot(glob_trfm),
                                        output_shape=out_shape,
                                        mode="constant", cval=np.nan)
            
                global_img_list.append(warped)
            
            except Exception as e:
                print(e)
                        

        
        all_nan_mask = np.all([np.isnan(img) for img in global_img_list], axis=0)
        global_img_list[0][all_nan_mask] = 1.

        composite_img = np.nanmean(global_img_list, 0)
        psnr_composite = metrics.peak_signal_noise_ratio(
            ref_img,
            composite_img[margin:margin + height,
                        margin:margin + width],
            data_range=data_range)

        rep.addSurface(composite_img, title="image registration")
    rep.addBoxComment("")    
    #if filter == "DATA":
    #    rep.addBoxComment("")    
    #else:
    rep.addSurface(super_a, title="simple superposition")
    
        
    
    rep.changeColNumber(3)
    rep.addLineComment("Bad images")
    for i in range(len(bad_images)):
        ikm = bad_images[i]
        tl = bad_titles[i]
        rep.addSurface(ikm,title=tl)
    rep.addBoxComment("")
    rep.addBoxComment("")
    
    rep.printReport()
    
#####################################################################################################                
if __name__ == "__main__":
    registration(sys.argv)  
