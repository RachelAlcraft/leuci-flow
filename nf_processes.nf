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
    input:
    path pdb_exists
         
    output:
    path "data*.csv" optional true
         
    script:    
    """
    data.py $pdb_exists $params.pdbdir $params.set_tag $params.filter
    """    
}

process DATA_ALL {        
    publishDir params.outcsv, mode:'copy'
    input:
    path pdb_csvs
         
    output:
    path "all_data*.csv" optional true
         
    script:    
    """
    alldata.py $params.outcsv $params.set_tag $params.filter $pdb_csvs
    """    
}

process SLICES2D {    
    //publishDir params.outnpy, mode:'copy'
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
    //publishDir params.outnpy, mode:'copy'
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
    path pdb_nps
         
    output:
    path 'image_overlay_2d*' optional true
     
    script:     
    """     
    overlay.py 2d $params.set_tag $params.filter $pdb_nps
    """
}

process OVERLAY3D{
    publishDir params.outdir, mode:'copy'
    input:
    path pdb_nps
         
    output:
    path 'image_overlay_3d*' optional true
     
    script:     
    """     
    overlay.py 3d $params.set_tag $params.filter $pdb_nps
    """
}

process IMAGE_REG_2D{
    publishDir params.outdir, mode:'copy'
    input:
    path all_csv
    path pdb_nps
         
    output:
    path 'image_reg_2d*' optional true
     
    script:     
    """     
    registration.py 2d $params.set_tag $params.filter $all_csv $pdb_nps
    """
}

process ELASTIC_REG_2D{
    publishDir params.outdir, mode:'copy'
    input:
    path all_csv
    path pdb_nps
         
    output:
    path 'elastic_reg_2d*' optional true
     
    script:     
    """     
    reg_elastic.py 2d $params.set_tag $params.filter $all_csv $pdb_nps
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



