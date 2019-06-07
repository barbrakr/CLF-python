# CLF-python
Cortical Lesion Finder in Python (work in progress, not a medical tool)

Overview of DCT_compile.m script: steps in the pipeline
1. load dicoms, and convert dicoms to nifti
2. set origin along ac-pc in T1w
3. segmentation (incl. conversion to MNI) with cat12-equivalent
4. coregistration, deformation
5. calculate TIV
6. calculate junction area ("blurring", voxels with intensity between WM and GM) and cortical extension area (thresholded above 0.5 - gives GM voxels) images
7. remove subcortical GM
8. remove cerebellum (using AAL template)
9. smooth junction file
10. ttestJCT, ttestEXT (between patient and their age/sex matched control)
11. create dicoms: (T1 proc., JL,EL, JS, ES)
    a. cleaned-up T1w (normalized, standard space)
    b. junction file binary, overlaid on T1w (P>C)
    c. extension file binary (P>C)
    d. junction (P<C)
    e. extension (P<C)
    f. summary (JL,EL)
    g. summary (JL, ES) - HS gliosis
    h. summary total (JL,JS,EL,ES all overlaid on T1w)
    
    **NOTE: diagnosis notes: in one case, FCD detected when blurring (junction) is larger, and extension (cortical extension) is greater. in alternative diagnosis (hippocampal scarring), the GM gets smaller, but blurring region increases

12. for each finding, remove duplicate (summary) file in case summary and non-summary are the same
13. move newly-created dicom files to subject's results directory (tell clinician results are ready, and where to find them)
