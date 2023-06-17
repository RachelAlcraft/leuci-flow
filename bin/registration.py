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
        
    all_data_array = []
    
    print(csv_path)
    #img_list = []
    loaded = False
    super_a = None
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
                super_a = a
                loaded = True
            else:
                super_a += a
            #img_list.append(a)
            all_data_array.append([ttl,a])
                
    #ref_img = img_list[0].copy()
    ref_img = all_data_array[0][1].copy()
    
    maxmax = -100
    minmin = 100
    for i in range(0,len(all_data_array)):
        imm = all_data_array[i][1]
        maxmax = max(maxmax,imm.max())
        minmin = min(minmin,imm.min())

    data_range = maxmax-minmin

    psnr_ref = metrics.peak_signal_noise_ratio(ref_img, all_data_array[1][1],data_range=data_range)

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
    for i in range(len(all_data_array)):
        img = all_data_array[i][1]
        harris_img = feature.corner_harris(img)
        print("----- CORNERS -----")        
        corners = feature.corner_peaks(harris_img, threshold_rel=0.001, min_distance=min_dist)
        print(corners)        
        #all_data_array[i].append(corners)
        # make corners up
        all_data_array[i].append([[25,25],[25,28],[30,30]])
        
    
    

    

    ############################################################################
    # The Harris corners detected in the first image are chosen as
    # references. Then the detected points on the other images are
    # matched to the reference points.

    img0 = all_data_array[0][1]
    coords0 = all_data_array[0][2]
    for i in range(len(all_data_array)):        
        coords1 = all_data_array[i][2]
        if len(coords1)> 1:
            coords0 = all_data_array[i][2]
            img0 = all_data_array[0][1]
            break
    
    #matching_corners = []
    for i in range(len(all_data_array)):
        img1 = all_data_array[i][1]
        coords1 = all_data_array[i][2]
        mc = match_locations(img0, img1, coords0, coords1, min_dist)
        #matching_corners.append(mc)
        all_data_array[i].append(mc)
        #for mmc in mc:
        #    print(type(mmc),mmc.shape,mmc,)
        
    ############################################################################
    # Once all the points are registered to the reference points, robust
    # relative affine transformations can be estimated using the RANSAC method.
    src = np.array(coords0)
        
    #trfm_list = []
    count = 0
    #for dst in matching_corners:
    for i in range(len(all_data_array)):
        dst = np.array(all_data_array[i][3])
        try:
            rnsc = measure.ransac((dst, src),transform.EuclideanTransform, min_samples=len(coords0),residual_threshold=2, max_trials=5000)
            if rnsc[0] is not None:
                all_data_array[i].append(rnsc[0].params)
                #trfm_list.append(rnsc[0].params)            
            else:
                all_data_array[i].append(np.array([float("Nan")]))
                #trfm_list.append(np.array([float("Nan")]))
        except Exception as e:
            #trfm_list.append(np.array([float("Nan")]))
            print(e)
            all_data_array[i].append(np.array([float("Nan")]))
        
        count += 1

        
    #fig, ax_list = plt.subplots(len(img_list), 2, figsize=(9,2*len(img_list)), sharex=True, sharey=True)
    #im_zipped = zip(img_list, trfm_list)

    good_images = []
    bad_images = []

    # Set up the output report
    rep = rm.ReportMaker("leuci-flow image registration",f"image_reg_{dims}_{tag}_{filter}.html",remove_strip=False,cols=3)
    rep.addBoxComment("Contour orig")
    rep.addBoxComment("Surface orig")
    rep.addBoxComment("Surface tilted")
    
    #for idx, (im, trfm) in enumerate(im_zipped):
    for i in range(len(all_data_array)):
        im = all_data_array[i][1]
        trfm = all_data_array[i][4]
        coords = all_data_array[i][2]
        
        if not math.isnan(trfm.max()):
            try:
                tr_im = transform.warp(im, trfm)
                print(i,len(tr_im[0]))             
                rep.addLineComment(all_data_array[i][0])
                rep.addContours(im[:, :, 0],overlay=True,colourbar=False)
                rep.addPoints2d([coords],overlay=False,hue="limegreen")
                rep.addSurface(im)        
                rep.addSurface(tr_im)
                good_images.append(all_data_array[i])
            except:
                print("error tilting",i)
                bad_images.append(all_data_array[i])
        else:
            bad_images.append(all_data_array[i])
        

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
    height, width,depth = ref_img.shape
    out_shape = height + 2 * margin, width + 2 * margin
    glob_trfm = np.eye(3)
    glob_trfm[:2, 2] = -margin, -margin

    ############################################################################
    # Finally, the relative position of the other images in the global
    # domain are obtained by composing the global transformation with the
    # relative transformations:
    rep.addLineComment("Superposition")
    rep.changeColNumber(3)
    if len(good_images) > 0:
        global_img_list = []
        for i in range(len(good_images)):
            im = good_images[i][1]
            trfm = good_images[i][4]
            global_img_list.append(transform.warp(img, trfm.dot(glob_trfm),
                                        output_shape=out_shape,
                                        mode="constant", cval=np.nan))
                        

        
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
    rep.addSurface(super_a, title="simple superposition")
        
    
    rep.changeColNumber(3)
    rep.addLineComment("Bad images")
    for im in bad_images:
        ikm = im[1]
        tl = im[0]
        rep.addSurface(ikm,title=tl)
    rep.addBoxComment("")
    rep.addBoxComment("")
    
    rep.printReport()
    
#####################################################################################################                
if __name__ == "__main__":
    registration(sys.argv)  
