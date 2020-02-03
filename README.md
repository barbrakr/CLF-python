# Cortical Lesion Finder

<img src="https://github.com/barbrakr/CLF-python/blob/master/Hackathon_21012020_UoL_bkreilkamp_figure.jpg" width=330 align="right" />

Cortical Lesion Finder is a free and open source voxel-based-morphometry method to identify epileptogenic lesions. This tool works on structural MRI (T1-weighted MPRAGE or FSPGR) and is designed to identify malformations of cortical development such as focal cortical dysplasias, hippocampal sclerosis, amygdala enlargment, encephaloceles and gliosis. 

# Disclaimer
This is work in progress and not meant to be used as a medical tool.

# Citation
- Kreilkamp, B.A.K., Das, K., Wieshmann, U.C., Tyler, K., Kiel, S., Gould, S., Marson, A.G., Keller, S.S. (2017) Voxel-based MRI Analysis Can Assist Clinical Diagnostics in Patients with MRI-negative Epilepsy. Organization of Human Brain Mapping, Vancouver, Canada, June 2017. http://tiny.cc/VBM_epilepsy

# License
Copyright © 2019, [Barbara A.K. Kreilkamp](https://orcid.org/0000-0001-6881-5191). This project is licensed under [BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause).

# Core dependencies
[Python 3.7](https://www.python.org/downloads/release/python-376/) (other versions of python (>=3.0) should be fine too)

 | Package                                            | Tested version |
 |----------------------------------------------------|----------------|
 | [NumPy](https://numpy.org)                         | 1.16.1         |
 | [NiBabel](https://nipy.org/nibabel/)               | 2.4.1          |
 | [NiPype](https://nipype.readthedocs.io/en/latest/) | 1.4.0          |
 | [niflow-nipype1-workflows](https://pypi.org/project/niflow-nipype1-workflows/) | 0.0.4 |


# Installation

- Download the latest [release](https://github.com/barbrakr/CLF-python/) and unzip it.
From command line change directory to the package:
```
cd /path/to/CLF-python/
```

- Pip-Users: Install the requirements by running the following command:    
```
pip install -r requirements.txt
```

- Conda-Users: Install the requirements by running the following command:
```
conda install --file requirements.txt
```

- You can then simply run the code:
```
python CLF/example_workflow.py
```

- Depending on your installations of the python version, you may have to specify the versions explicitly, e.g.:
```
python3.7 CLF/example_workflow.py
```

# Workflow
*OVERVIEW* of `DCT_compile.m` script (steps in the pipeline)
1. Load dicoms, and convert dicoms to nifti.
2. Set origin along ac-pc in T1w (probably not necessary to do this explicitly/manually in FSL).
3. Coregistration, deformation (including registration to MNI-template).
4. Segmentation with cat12-equivalent.
5. Calculate TIV.
6. Remove subcortical GM (using AAL template).
7. Remove cerebellum (using AAL template).
8. Calculate junction area ("blurring", voxels with intensity between WM and GM) and cortical extension area (thresholded above 0.5 - gives GM voxels) images.
9. Smooth junction and extension file.
10. ttestJCT, ttestEXT (between patient and controls, confounds: age, sex, TIV)
11. Create dicoms: (T1 proc., JL, EL, JS, ES)
    a. Cleaned-up T1w (normalized, standard space)
    b. Junction file binary, overlaid on T1w (P>C)
    c. Extension file binary (P>C)
    d. Junction (P<C)
    e. Extension (P<C)
    f. Summary (JL, EL)
    g. Summary (JL, ES) - HS gliosis
    h. Summary total (JL, JS, EL, ES all overlaid on T1w)
    
    **NOTE: diagnosis notes: in one case, FCD detected when blurring (junction) is larger, and extension (cortical extension) is greater. in alternative diagnosis (hippocampal scarring), the GM gets smaller, but blurring region increases

12. For each finding, remove duplicate (summary) file in case summary and non-summary are the same.
13. Move newly-created dicom files to subject's results directory (tell clinician results are ready, and where to find them).

# Support
Please use [GitHub issues](https://github.com/barbrakr/CLF-python/issues) for questions, bug reports or feature requests.

# Collaborators
- Samuel Berry: @el-suri
- Tom Chambers
- Devin Crowley: @devincrowley
- Johnny King Lau: @jonkingseestheworld
- Roopa Pai: @roopa-pai
- Carsten Schmidt-Samoa: @carsten.schmidt-samoa
- Lennart Wittkuhn: @lnnrtwttkhn

# Reference
This method is extended and modified from this publication on the Morphometric Analysis Pipeline (MAP) developed by Huppertz et al. 2005:

- Huppertz, H.-J., Grimm, C., Fauser, S., Kassubek, J., Mader, I., Hochmuth, A., Schulze-Bonhage, A. (2005). Enhanced visualization of blurred gray-white matter junctions in focal cortical dysplasia by voxel-based 3D MRI analysis. Epilepsy Research, 67(1-2), 35-50. <https://doi.org/10.1016/j.eplepsyres.2005.07.009> 

