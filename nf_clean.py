"""
RSA 10/06/2023
This file can test the steps in nextflow in a debuggable way

"""

import os
import shutil


print("Cleaning work...")
shutil.rmtree("work")
os.mkdir("work")

print("Cleaning results...")
shutil.rmtree("results")
os.mkdir("results")

print("...complete")