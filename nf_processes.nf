#!/usr/bin/env nextflow

params.set_tag = "small"
params.filter = "PI"
params.pdb_file = './inputs/set_tag_small.csv'

//params.pdbdir = "/home/rachel/phd/leuci-async/leuci-flow/pdbdata"
params.pdbdir = "/workspace/leuci-flow/pdbdata"
//params.pdbdir = "/home/ralcraft/phd/leuci-flow/pdbdata"

params.outdir = "results"
params.outcsv = "results_csv"
params.outnpy = "results_npy"
params.outhtml = "results_html"



process EXISTS {        
    input:
    val pdb
         
    output:
    path "exists.csv", optional: true
         
    script:    
    """
    exists.py $pdb $params.pdbdir
    """    
}

process DATA {        
    publishDir params.outcsv, mode:'copy'
    input:
    path pdb_exists
         
    output:
    path "data*.csv" optional true
         
    script:    
    """
    data.py $pdb_exists $params.pdbdir $params.set_tag $params.filter
    """    
}

process SLICES2D {    
    publishDir params.outnpy, mode:'copy'
    input:
    path pdb_csv
         
    output:
    path "2d_matrices_*" optional true    
         
    script:    
    """
    slices.py $pdb_csv $params.pdbdir 2d_np $params.set_tag $params.filter
    """    
} 

process SLICES3D {    
    publishDir params.outnpy, mode:'copy'
    input:
    path pdb_csv
         
    output:
    path "3d_matrices_*" optional true    
         
    script:    
    """
    slices.py $pdb_csv $params.pdbdir 3d_np $params.set_tag $params.filter
    """    
}

process OVERLAY2D{
    publishDir params.outdir, mode:'copy'
    input:
    path y
    val mat_dir
     
    output:
    path 'image_overlay_2d*' optional true
     
    script:     
    """     
    overlay.py $mat_dir 2d $params.set_tag $params.filter
    """
}

process OVERLAY3D{
    publishDir params.outdir, mode:'copy'
    input:
    path y
    val mat_dir
     
    output:
    path 'image_overlay_3d*' optional true
     
    script:     
    """     
    overlay.py $mat_dir 3d $params.set_tag $params.filter
    """
}

process IMAGES2D {    
    publishDir params.outhtml, mode:'copy'
    input:
    path pdb_csv
         
    output:
    path "2d_image_*" optional true    
         
    script:    
    """
    slices.py $pdb_csv $params.pdbdir 2d_im $params.set_tag $params.filter
    """    
}

process IMAGES2D_NAY {    
    publishDir params.outhtml, mode:'copy'
    input:
    path pdb_csv
         
    output:
    path "2d_image_*" optional true    
         
    script:    
    """
    slices.py $pdb_csv $params.pdbdir 2d_im_nay $params.set_tag $params.filter
    """    
}

process IMAGES3D {    
    publishDir params.outhtml, mode:'copy'
    input:
    path pdb_csv
         
    output:
    path "3d_image_*" optional true    
         
    script:    
    """
    slices.py $pdb_csv $params.pdbdir 3d_im $params.set_tag $params.filter
    """    
}



workflow {
    
    pdbs0_ch = Channel
                .fromPath(params.pdb_file) \
                | splitCsv(header:true,sep:",") \
                | map{row->tuple(row.pdbs)}                     
    
    pdbs_ch = EXISTS(pdbs0_ch.flatten())
    
    data_ch = DATA(pdbs_ch.flatten())
    
    mat_ch = Channel.fromPath(params.outnpy)

    //slices2_ch = SLICES2D(data_ch)
    //OVERLAY2D(slices2_ch.collect().flatten(),mat_ch)
                        
    //slices3_ch = SLICES3D(data_ch)
    //OVERLAY3D(slices3_ch.collect().flatten(),mat_ch)
        
    // This is very slow but very useful
    //images2_ch = IMAGES2D_NAY(data_ch)
                
    // Optional but unlikely - neighbours better and 3d for every image just too much data
    //images2_ch = IMAGES2D(data_ch)
    //images3_ch = IMAGES3D(data_ch)        
    
    
}