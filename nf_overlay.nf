#!/usr/bin/env nextflow

//#################################################################
params.set_tag = "small"
params.pdb_file = './inputs/set_tag_small.csv'
params.filter = "TAU"
//params.pdbdir = "~/git/leuci-flow/pdbdata"
params.pdbdir = "/home/rachel/phd/leuci-async/leuci-flow/pdbdata"
//params.pdbdir = "/workspaces/leuci-flow/pdbdata"
//params.pdbdir = "/home/ralcraft/phd/leuci-flow/pdbdata"
params.outdir = "results"
params.outcsv = "results_csv"
params.outnpy = "results_npy"
params.outhtml = "results_html"
//#################################################################
// Processes to include from the shared module
include { EXISTS } from './nf_processes'
include { DATA } from './nf_processes'
include { DATA_ALL } from './nf_processes'
include { SLICES2D } from './nf_processes'
include { SLICES3D } from './nf_processes'
include { OVERLAY2D } from './nf_processes'
include { IMAGE_REG_2D } from './nf_processes'
include { OVERLAY3D } from './nf_processes'
include { IMAGES2D } from './nf_processes'
include { IMAGES2D_NAY } from './nf_processes'
include { IMAGES3D } from './nf_processes'
//#################################################################
workflow {
    
    pdbs0_ch = Channel
                .fromPath(params.pdb_file) \
                | splitCsv(header:true,sep:",") \
                | map{row->tuple(row.pdbs)}                     
    
    pdbs_ch = EXISTS(pdbs0_ch.flatten())
    
    data_ch = DATA(pdbs_ch.flatten()).flatten()

    all_csv_ch = DATA_ALL(data_ch.collect())
        
    slices2_ch = SLICES2D(data_ch)
    OVERLAY2D(slices2_ch.flatten().collect())
    IMAGE_REG_2D(all_csv_ch,slices2_ch.flatten().collect())
                        
    //slices3_ch = SLICES3D(data_ch)
    //OVERLAY3D(slices3_ch.flatten().collect())
        
    // ### This is very slow but very useful
    //images2_ch = IMAGES2D_NAY(data_ch)
                
    // ### Optional but unlikely - neighbours better and 3d for every image just too much data
    //images2_ch = IMAGES2D(data_ch)
    //images3_ch = IMAGES3D(data_ch)                
}
//#################################################################