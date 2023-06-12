"""
RSA 10/06/2023
This file can test the steps in nextflow in a debuggable way

"""

import os
import shutil


dirs = ["results","results_csv","results_html","results_npy","work"]

make,clean = True,True

try:
    os.mkdir("pdbdata")
except:
    pass

if make:
    for dir in dirs:
        try:
            os.mkdir(dir)        
        except:
            pass

if clean:
    for dir in dirs:
        try:
            print("Cleaning ",dir,"...")
            shutil.rmtree(dir)
            os.mkdir(dir)
        except:
            pass        
    