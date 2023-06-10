#!/usr/bin/env nextflow

params.pdbs = ['5i9s', '5k7o', '5k7r', '5k7s', '6cl7', '6lav', '6law', '6pkp', '6pkq', '6pkr', '6pkt', '6s2n', '6v8r', '7jsy', '7mrp', '7skw', '7skx', '7sw1', '7sw2', '7sw5', '7sw6', '7sw8', '7uly']
params.pdbdir = "/home/rachel/phd/leuci-async/leuci-flow/pdbdata"
params.outdir = "results"

process PREPARE {    
    publishDir params.outdir, mode:'copy'
    input:
    val pdb
         
    output:
    val pdb
         
    script:    
    """
    prepare.py $pdb $params.pdbdir
    """    
} 

process SLICES2D {    
    publishDir params.outdir, mode:'copy'
    input:
    val pdb
         
    output:
    path "2d_*.npy"
         
    script:    
    """
    slices.py $pdb $params.pdbdir 2d_np
    """    
} 

process SLICES3D {    
    publishDir params.outdir, mode:'copy'
    input:
    val pdb
         
    output:
    path "3d_*.npy"
         
    script:    
    """
    slices.py $pdb $params.pdbdir 3d_np
    """    
}

process IMAGES2D {    
    publishDir params.outdir, mode:'copy'
    input:
    val pdb
             
    output:
    path "2d_*.html"
         
    script:    
    """
    slices.py $pdb $params.pdbdir 2d_html
    """    
} 

process IMAGES3D {    
    publishDir params.outdir, mode:'copy'
    input:
    val pdb
         
    output:
    path "3d_*.html"
         
    script:    
    """
    slices.py $pdb $params.pdbdir 3d_html
    """    
}

process OVERLAY2D{
    publishDir params.outdir, mode:'copy'
    input:
    path y
    val mat_dir
     
    output:
    path 'image_overlay_2d.*'
     
    script:     
    """     
    overlay.py $mat_dir 2d
    """
}

process OVERLAY3D{
    publishDir params.outdir, mode:'copy'
    input:
    path y
    val mat_dir
     
    output:
    path 'image_overlay_3d.*'
     
    script:     
    """     
    overlay.py $mat_dir 3d
    """
}

workflow {
    pdbs0_ch = Channel.from(params.pdbs)    
    pdbs_ch = PREPARE(pdbs0_ch.flatten())    
    slices2_ch = SLICES2D(pdbs_ch.flatten())
    images2_ch = IMAGES2D(pdbs_ch.flatten())    
    
    //slices2_ch.collect().flatten().view { "value: $it" }    
    mat_ch = Channel.fromPath(params.outdir)
    overlay_ch = OVERLAY2D(slices2_ch.collect().flatten(),mat_ch)

    slices3_ch = SLICES3D(pdbs_ch.flatten())
    overlay_ch = OVERLAY3D(slices3_ch.collect().flatten(),mat_ch)
    //images3_ch = IMAGES3D(pdbs_ch.flatten())        
    //slices3_ch.collect().flatten().view { "value: $it" }
    
}