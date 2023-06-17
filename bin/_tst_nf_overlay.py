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

cmdsl = "registration.py 2d small TAU all_data_small_TAU_.csv 2d_matrices_1ejg_\(A\|ALA\|45\|CA\|618\)\(A\|ALA\|45\|N\|617\)\(A\|ALA\|45\|C\|619\)_small_TAU.npy 2d_matrices_1ejg_(A|ARG|10|CA|122)(A|ARG|10|N|121)(A|ARG|10|C|123)_small_TAU.npy 2d_matrices_1ejg_\(A\|ARG\|17\|CA\|231\)\(A\|ARG\|17\|N\|230\)\(A\|ARG\|17\|C\|232\)_small_TAU.npy 2d_matrices_1ejg_\(A\|ALA\|27\|CA\|377\)\(A\|ALA\|27\|N\|376\)\(A\|ALA\|27\|C\|378\)_small_TAU.npy"# 2d_matrices_1ejg_\(A\|ALA\|24\|CA\|338\)\(A\|ALA\|24\|N\|337\)\(A\|ALA\|24\|C\|339\)_small_TAU.npy 2d_matrices_1ejg_\(A\|ALA\|9\|CA\|112\)\(A\|ALA\|9\|N\|111\)\(A\|ALA\|9\|C\|113\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|16\|CA\|221\)\(A\|CYS\|16\|N\|220\)\(A\|CYS\|16\|C\|222\)_small_TAU.npy 2d_matrices_1ejg_\(A\|ALA\|38\|CA\|531\)\(A\|ALA\|38\|N\|530\)\(A\|ALA\|38\|C\|532\)_small_TAU.npy 2d_matrices_1ejg_\(A\|ASN\|46\|CA\|628\)\(A\|ASN\|46\|N\|627\)\(A\|ASN\|46\|C\|629\)_small_TAU.npy 2d_matrices_1ejg_\(A\|ASP\|43\|CA\|585\)\(A\|ASP\|43\|N\|584\)\(A\|ASP\|43\|C\|586\)_small_TAU.npy 2d_matrices_1ejg_\(A\|GLY\|37\|CA\|524\)\(A\|GLY\|37\|N\|523\)\(A\|GLY\|37\|C\|525\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|3\|CA\|32\)\(A\|CYS\|3\|N\|31\)\(A\|CYS\|3\|C\|33\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|26\|CA\|367\)\(A\|CYS\|26\|N\|366\)\(A\|CYS\|26\|C\|368\)_small_TAU.npy 2d_matrices_1ejg_\(A\|ASN\|14\|CA\|191\)\(A\|ASN\|14\|N\|190\)\(A\|ASN\|14\|C\|192\)_small_TAU.npy 2d_matrices_1ejg_\(A\|GLY\|42\|CA\|578\)\(A\|GLY\|42\|N\|577\)\(A\|GLY\|42\|C\|579\)_small_TAU.npy 2d_matrices_1ejg_\(A\|ILE\|33\|CA\|453\)\(A\|ILE\|33\|N\|452\)\(A\|ILE\|33\|C\|454\)_small_TAU.npy 2d_matrices_1ejg_\(A\|GLY\|31\|CA\|436\)\(A\|GLY\|31\|N\|435\)\(A\|GLY\|31\|C\|437\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|4\|CA\|42\)\(A\|CYS\|4\|N\|41\)\(A\|CYS\|4\|C\|43\)_small_TAU.npy 2d_matrices_1ejg_\(A\|GLU\|23\|CA\|323\)\(A\|GLU\|23\|N\|322\)\(A\|GLU\|23\|C\|324\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|40\|CA\|554\)\(A\|CYS\|40\|N\|553\)\(A\|CYS\|40\|C\|555\)_small_TAU.npy 2d_matrices_1ejg_\(A\|ILE\|34\|CA\|472\)\(A\|ILE\|34\|N\|471\)\(A\|ILE\|34\|C\|473\)_small_TAU.npy 2d_matrices_1ejg_\(A\|CYS\|32\|CA\|443\)\(A\|CYS\|32\|N\|442\)\(A\|CYS\|32\|C\|444\)_small_TAU.npy 2d_matrices_1ejg_\(A\|GLY\|20\|CA\|288\)\(A\|GLY\|20\|N\|287\)\(A\|GLY\|20\|C\|289\)_small_TAU.npy 2d_matrices_1ejg_\(A\|PHE\|13\|CA\|171\)\(A\|PHE\|13\|N\|170\)\(A\|PHE\|13\|C\|172\)_small_TAU.npy 2d_matrices_1ejg_\(A\|ILE\|35\|CA\|491\)\(A\|ILE\|35\|N\|490\)\(A\|ILE\|35\|C\|492\)_small_TAU.npy 2d_matrices_1ejg_\(A\|LEU\|18\|CA\|255\)\(A\|LEU\|18\|N\|254\)\(A\|LEU\|18\|C\|256\)_small_TAU.npy 2d_matrices_1ejg_\(A\|PRO\|41\|CA\|564\)\(A\|PRO\|41\|N\|563\)\(A\|PRO\|41\|C\|565\)_small_TAU.npy 2d_matrices_1ejg_\(A\|PRO\|36\|CA\|510\)\(A\|PRO\|36\|N\|509\)\(A\|PRO\|36\|C\|511\)_small_TAU.npy 2d_matrices_1ejg_\(A\|PRO\|19\|CA\|274\)\(A\|PRO\|19\|N\|273\)\(A\|PRO\|19\|C\|275\)_small_TAU.npy 2d_matrices_1ejg_\(A\|PRO\|5\|CA\|52\)\(A\|PRO\|5\|N\|51\)\(A\|PRO\|5\|C\|53\)_small_TAU.npy 2d_matrices_1ejg_\(A\|SER\|6\|CA\|66\)\(A\|SER\|6\|N\|65\)\(A\|SER\|6\|C\|67\)_small_TAU.npy 2d_matrices_1ejg_\(A\|THR\|30\|CA\|422\)\(A\|THR\|30\|N\|421\)\(A\|THR\|30\|C\|423\)_small_TAU.npy 2d_matrices_1ejg_\(A\|THR\|21\|CA\|295\)\(A\|THR\|21\|N\|294\)\(A\|THR\|21\|C\|296\)_small_TAU.npy 2d_matrices_1ejg_\(A\|TYR\|29\|CA\|401\)\(A\|TYR\|29\|N\|400\)\(A\|TYR\|29\|C\|402\)_small_TAU.npy 2d_matrices_1ejg_\(A\|VAL\|15\|CA\|205\)\(A\|VAL\|15\|N\|204\)\(A\|VAL\|15\|C\|206\)_small_TAU.npy 2d_matrices_1ejg_\(A\|THR\|39\|CA\|541\)\(A\|THR\|39\|N\|540\)\(A\|THR\|39\|C\|542\)_small_TAU.npy 2d_matrices_1ejg_\(A\|SER\|11\|CA\|146\)\(A\|SER\|11\|N\|145\)\(A\|SER\|11\|C\|147\)_small_TAU.npy 2d_matrices_1ejg_\(A\|TYR\|44\|CA\|597\)\(A\|TYR\|44\|N\|596\)\(A\|TYR\|44\|C\|598\)_small_TAU.npy 2d_matrices_1ejg_\(A\|THR\|28\|CA\|387\)\(A\|THR\|28\|N\|386\)\(A\|THR\|28\|C\|388\)_small_TAU.npy"
cmds = cmdsl.split(" ")
#cmds = ["","2d","small","TAU","all_data_small_TAU_.csv"]
#for i in [3,2,1,5,0,4]:#range(0,6):
#    cmds.append(f"2d_matrices_1ejg_{i}_small_TAU.npy")
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





