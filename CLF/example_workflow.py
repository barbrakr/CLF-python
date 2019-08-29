
# import basic libraries:
import os

from pathlib import Path

import sys
import glob
import warnings
from os.path import join as opj
# import nipype libraries:
from nipype.interfaces.utility import Function, IdentityInterface
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.pipeline.engine import Workflow, Node, MapNode
from nipype.interfaces.dcm2nii import Dcm2niix
from nipype.workflows.smri.freesurfer.autorecon1 import create_AutoRecon1
from nipype.interfaces import fsl
from nipype.interfaces.fsl.maths import MultiImageMaths


# ======================================================================
# DEFINE INPUT: User
# ======================================================================

# Read directory of dicom files into a single 3D nifti file.
dicom_directory = input("Please enter folder.")

#bk#from myfunctions import prompt_demographics, my_dcm2niix
from myfunctions import prompt_demographics

age, sex = prompt_demographics()

# ======================================================================
# DEFINE NODE: INFOSOURCE
# ======================================================================
# define list with subject ids:
sub_list = [''] #bk# ['sub-01']
# define the infosource node that collects the data:
infosource = Node(IdentityInterface(
    fields=['subject_id']), name='infosource')
# let the node iterate (paralellize) over all subjects:
infosource.iterables = [('subject_id', sub_list)]
# ======================================================================
# DEFINE SELECTFILES NODE
# ======================================================================
path_root = dicom_directory #os.path.dirname(os.getcwd())
path_app = os.path.dirname(os.getcwd())

templates = dict(dicom=opj(path_root, '', '{subject_id}'))
test = opj(path_app,'CLF-python')
# define the selectfiles node:
selectfiles = Node(SelectFiles(templates), name='selectfiles')
# ======================================================================
# DICOM 2 NIFTI CONVERSION
# ======================================================================
# function: put dcm2niix into a node:
dcm2niix = Node(Dcm2niix(), name='dcm2niix')
dcm2niix.inputs.out_filename = '%i_%4s_%d'
print(dcm2niix.inputs.out_filename)

# ======================================================================
# DEFINE FREESURFER NODE
# ======================================================================
# function: autorecon1
# 1. Motion Correction and Conform
# 2. NU (Non-Uniform intensity normalization)
# 3. Talairach transform computation
# 4. Intensity Normalization 1
# 5. Skull Strip
#distance = 50
#fs_recon1 = Node(create_AutoRecon1(), name='fs_recon1')
#fs_recon1.inputs.inputspec.subject_id = 'subj1'
#fs_recon1.inputs.inputspec.subjects_dir = '.'
#fs_recon1.inputs.inputspec.T1_files = dcm2niix.inputs.out_filename #'T1.nii.gz'
#fs_recon1.run()

# =====================================================================
# DEFINE FSL FAST NODE
# =====================================================================
fastr = Node(interface = fsl.FAST(), name = 'fastr')
fastr.inputs.in_files = '/Users/NEURO-222/Desktop/DCT_anon_dREF059p_27f_lPL2/derivatives/dcm2niix/NOID_0005_Ax_FSPGR_BRAVO_PURE.nii.gz' #"%s" % (dcm2niix.inputs.out_filename) #'aal_realinterest.nii' #Should eventually be 'NOID_0005_Ax_FSPGR_BRAVO_PURE.nii.gz'
fastr.inputs.out_basename = 'fast_'
fastr.inputs.verbose = True
fastr.inputs.probability_maps = True
fastr.inputs.output_biascorrected = True
out_basename = fastr.run()

# ======================================================================
# DEFINE FSLMATHS NODE
# ======================================================================
fslmaths = Node(interface = fsl.MultiImageMaths(),
                          name = 'fslmaths', iterfield = ['in_file', 'op_string'])
fslmaths.inputs.in_file = opj(test,'aal_realinterest.nii')
fslmaths.inputs.op_string = "-bin -add %s" #should eventually be "-bin -mul %s"
fslmaths.inputs.operand_files = opj(test,'aal_realinterest.nii') #should eventually be: freesurfer.inputs.out_filename #FreeSurfer derived intensity-normalized image
fslmaths.inputs.out_file = "nobg_nocerebellum.nii.gz"

# ======================================================================
# CREATE DATASINK NODE (OUTPUT STREAM):
# ======================================================================
# create a node of the function:
datasink = Node(DataSink(), name='datasink')
# assign the path to the base directory:
datasink.inputs.base_directory = os.path.join(path_root, 'derivatives')
# create a list of substitutions to adjust the file paths of datasink:
substitutions = [('_subject_id_', '')]
# assign the substitutions to the datasink command:
datasink.inputs.substitutions = substitutions
# determine whether to store output in parameterized form:
datasink.inputs.parameterization = True
# ======================================================================
# DEFINE THE WORKFLOW:
# ======================================================================
# initiation of the 1st-level analysis workflow:
clf_pipeline = Workflow(name='clf_pipeline')
# stop execution of the workflow if an error is encountered:
clf_pipeline.config = {'execution': {'stop_on_first_crash': True,
                                   'hash_method': 'timestamp'}}
# define the base directory of the workflow:
clf_pipeline.base_dir = os.path.join(path_root, 'work')
# connect the 1st-level analysis components
clf_pipeline.connect(infosource, 'subject_id', selectfiles, 'subject_id')
clf_pipeline.connect(selectfiles, 'dicom', dcm2niix, 'source_dir')
clf_pipeline.connect(dcm2niix, 'converted_files', datasink, 'dcm2niix.@converted_files')
clf_pipeline.connect(dcm2niix, 'bids', datasink, 'dcm2niix.@bids')
clf_pipeline.connect(fastr, 'out_folder', datasink, 'fastr.@output_folder')
clf_pipeline.connect(fslmaths, 'out_file', datasink, 'fslmaths.@out_files')
#bk#clf_pipeline.connect(dcm2niix, 'converted_files', fs_recon1, 'inputspec.T1_files')
#bk#clf_pipeline.connect(fs_recon1, 'out_file', datasink, 'fs_recon1.@out_file')
# ======================================================================
# WRITE GRAPH AND EXECUTE THE WORKFLOW
# ======================================================================
# write the graph:
#clf_pipeline.write_graph(graph2use='colored', simple_form=True)
# will execute the workflow using all available cpus:
clf_pipeline.run(plugin='MultiProc')
