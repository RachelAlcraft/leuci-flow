"""
RSA 10/06/2023
This file can test the steps in nextflow in a debuggable way

"""

import os
import shutil

try:
    os.mkdir("results")
    os.mkdir("work")
except:
    pass


print("Cleaning work...")
shutil.rmtree("work")
os.mkdir("work")

print("Cleaning results...")
shutil.rmtree("results")
os.mkdir("results")

print("...complete")