
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
# ======================================================================
# DEFINE NODE: INFOSOURCE
# ======================================================================
# define list with subject ids:
#sub_list = list(range(136))
sub_list = list(range(1))
sub_list = ['I' + str(i) for i in sub_list]
# define the infosource node that collects the data:
infosource = Node(IdentityInterface(
    fields=['subject_id']), name='infosource')
# let the node iterate (paralellize) over all subjects:
infosource.iterables = [('subject_id', sub_list)]
# ======================================================================
# DEFINE SELECTFILES NODE
# ======================================================================
path_root = os.path.dirname(os.getcwd())

templates = dict(dicom=opj(path_root, 'data', '{subject_id}'))
# define the selectfiles node:
selectfiles = Node(SelectFiles(templates), name='selectfiles')
# ======================================================================
# DICOM 2 NIFTI CONVERSION
# ======================================================================
# function: put dcm2niix into a node:
dcm2niix = Node(Dcm2niix(), name='dcm2niix')
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
clf_pipeline.connect(selectfiles, 'dicom', dcm2niix, 'source_names')
clf_pipeline.connect(dcm2niix, 'converted_files', datasink, 'dcm2niix.@converted_files')
clf_pipeline.connect(dcm2niix, 'bids', datasink, 'dcm2niix.@bids')
# ======================================================================
# WRITE GRAPH AND EXECUTE THE WORKFLOW
# ======================================================================
# write the graph:
clf_pipeline.write_graph(graph2use='colored', simple_form=True)
# will execute the workflow using all available cpus:
clf_pipeline.run(plugin='MultiProc')
