"""
RSA 10/06/2023
This file can test the steps in nextflow in a debuggable way

"""

import exists as be
import data as bd
import slices as bs
import overlay as bo
import registration as br
import math


#be.exists(["", "4nir", "/home/rachel/phd/leuci-async/leuci-flow/pdbdata"])
#bd.data(["", "exists.csv", "/home/rachel/phd/leuci-async/leuci-flow/pdbdata","small","PI"])
#bs.slices(["", "exists.csv", "/home/rachel/phd/leuci-async/leuci-flow/pdbdata", "2d_np"])
#bo.overlay(["","/home/rachel/phd/leuci-async/leuci-flow/results","2d","small","PI"])
#bo.overlay(["", "3d", "small", "PI", "3d_matrices_4nir_0_small_PI.npy", "3d_matrices_4nir_5_small_PI.npy", "3d_matrices_4nir_7_small_PI.npy"])

cmdsl = "registration.py 2d small TAU all_data_small_TAU_.csv 2d_matrices_1ejg_\(A\|CYS\|3\|CA\|32\)\(A\|CYS\|3\|N\|31\)\(A\|CYS\|3\|C\|33\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|16\|CA\|221\)\(A\|CYS\|16\|N\|220\)\(A\|CYS\|16\|C\|222\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|40\|CA\|554\)\(A\|CYS\|40\|N\|553\)\(A\|CYS\|40\|C\|555\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|26\|CA\|367\)\(A\|CYS\|26\|N\|366\)\(A\|CYS\|26\|C\|368\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|32\|CA\|443\)\(A\|CYS\|32\|N\|442\)\(A\|CYS\|32\|C\|444\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|4\|CA\|42\)\(A\|CYS\|4\|N\|41\)\(A\|CYS\|4\|C\|43\)_small_TAU.npy"
#cmdsl = "registration.py 2d data DATA all_data_small_TAU_.csv 2d_matrices_1ejg_\(A\|CYS\|32\|CA\|443\)\(A\|CYS\|32\|N\|442\)\(A\|CYS\|32\|C\|444\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|26\|CA\|367\)\(A\|CYS\|26\|N\|366\)\(A\|CYS\|26\|C\|368\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|3\|CA\|32\)\(A\|CYS\|3\|N\|31\)\(A\|CYS\|3\|C\|33\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|16\|CA\|221\)\(A\|CYS\|16\|N\|220\)\(A\|CYS\|16\|C\|222\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|4\|CA\|42\)\(A\|CYS\|4\|N\|41\)\(A\|CYS\|4\|C\|43\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|40\|CA\|554\)\(A\|CYS\|40\|N\|553\)\(A\|CYS\|40\|C\|555\)_small_TAU.npy"


cmds = cmdsl.split(" ")

br.registration(cmds)




if False:
    tags = ["small","ec","em","xray"]
    for tag in tags:
        with open("inputs/set_tag_xray.csv","r") as r:
            pdbs = r.readlines()
            for i in range(1,len(pdbs)):
                pdb = pdbs[i].strip()
                if len(pdb) == 4:
                    print("####",i,"/",len(pdbs),"fetching",pdb,"####")
                    be.exists(["", pdb, "/home/rachel/phd/leuci-async/leuci-flow/pdbdata"])





