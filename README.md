# Cortical Lesion Finder
Cortical Lesion Finder is a free and open source voxel-based-morphometry method to identify epileptogenic lesions. This tool works on structural MRI (T1-weighted MPRAGE or FSPGR) and is designed to identify malformations of cortical development such as focal cortical dysplasias, hippocampal sclerosis, amygdala enlargment, encephaloceles and gliosis. 

# Disclaimer
This is work in progress and not meant to be used as a medical tool.

# Citation
Kreilkamp, B.A.K., Das, K., Wieshmann, U.C., Tyler, K., Kiel, S., Gould, S., Marson, A.G., Keller, S.S. (2017) Voxel-based MRI Analysis Can Assist Clinical Diagnostics in Patients with MRI-negative Epilepsy. Organization of Human Brain Mapping, Vancouver, Canada, June 2017. http://tiny.cc/VBM_epilepsy

# License
Copyright © 2019, [Barbara A.K. Kreilkamp](https://orcid.org/0000-0001-6881-5191). This project is licensed under [BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause).

# Core dependencies
[Python 3.7](https://www.python.org/downloads/release/python-376/) (other versions of python (>=3.0) should be fine too)

| Package   | Tested version   |
|------------|-------------------------------|
| [NumPy](https://numpy.org)        | 1.16.1 |
| [NiBabel](https://nipy.org/nibabel/)        | 2.4.1 |
| [NiPype](https://nipype.readthedocs.io/en/latest/)        | 1.4.0 |

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

# Support

Please use [GitHub issues](https://github.com/barbrakr/CLF-python/issues) for questions, bug reports or feature requests.


# Collaborators

Samuel Berry: @el-suri

Tom Chambers

Devin Crowley: @devincrowley

Johnny King Lau: @jonkingseestheworld

Roopa Pai: @roopa-pai

Carsten Schmidt-Samoa: @carsten.schmidt-samoa

Lennart Wittkuhn: @lnnrtwttkhn


 
# REQUIREMENTS

pip install nipype==1.4.0

pip install niflow-nipype1-workflows

pip install numpy==1.16.1

[to be confirmed if complete]


# Workflow

*OVERVIEW* of DCT_compile.m script (steps in the pipeline)
1. load dicoms, and convert dicoms to nifti
2. set origin along ac-pc in T1w (probably not necessary to do this explicitly/manually in FSL)
3. coregistration, deformation (incl. registration to MNI-template) 
4. segmentation with cat12-equivalent
5. calculate TIV
6. remove subcortical GM (using AAL template)
7. remove cerebellum (using AAL template)
8. calculate junction area ("blurring", voxels with intensity between WM and GM) and cortical extension area (thresholded above 0.5 - gives GM voxels) images
9. smooth junction and extension file
10. ttestJCT, ttestEXT (between patient and controls, confounds: age, sex, TIV)
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



