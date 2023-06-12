"""
RSA 10/06/2023
This file can test the steps in nextflow in a debuggable way

"""

import bin.exists as be
import bin.slices as bs
import bin.overlay as bo


#be.exists(["", "5i9s", "/home/rachel/phd/leuci-async/leuci-flow/pdbdata"])
#bs.slices(["", "exists.csv", "/home/rachel/phd/leuci-async/leuci-flow/pdbdata", "2d_np"])
#bo.overlay(["","/home/rachel/phd/leuci-async/leuci-flow/results","2d","small"])

if True:
     with open("inputs/set_tag_ec.csv","r") as r:
        pdbs = r.readlines()
        for i in range(1,len(pdbs)):
            pdb = pdbs[i].strip()
            if len(pdb) == 4:
                print("fetching",pdb)
                be.exists(["", pdb, "/home/rachel/phd/leuci-async/leuci-flow/pdbdata"])





