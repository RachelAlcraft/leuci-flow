#!/usr/bin/env nextflow

//#################################################################
params.set_tag = "small"
params.filter = "PI"
params.pdb_file = './inputs/set_tag_small.csv'
params.pdbdir = "/home/git/leuci-flow/pdbdata"
//params.pdbdir = "/home/rachel/phd/leuci-async/leuci-flow/pdbdata"
//params.pdbdir = "/workspace/leuci-flow/pdbdata"
//params.pdbdir = "/home/ralcraft/phd/leuci-flow/pdbdata"
params.outdir = "results"
params.outcsv = "results_csv"
params.outnpy = "results_npy"
params.outhtml = "results_html"
//#################################################################
// Processes to include from the shared module
include { EXISTS } from './nf_processes'
include { DATA } from './nf_processes'
include { SLICES2D } from './nf_processes'
include { SLICES3D } from './nf_processes'
include { OVERLAY2D } from './nf_processes'
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
    
    mat_ch = Channel.fromPath(params.outnpy)

    slices2_ch = SLICES2D(data_ch)
    OVERLAY2D(slices2_ch.collect().flatten(),mat_ch)
                        
    slices3_ch = SLICES3D(data_ch)
    OVERLAY3D(slices3_ch.collect().flatten(),mat_ch)
        
    // This is very slow but very useful
    images2_ch = IMAGES2D_NAY(data_ch)
                
    // Optional but unlikely - neighbours better and 3d for every image just too much data
    //images2_ch = IMAGES2D(data_ch)
    //images3_ch = IMAGES3D(data_ch)                
}
//#################################################################