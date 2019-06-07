import dicom2nifti

def main():

    # Read directory of dicom files into a single 3D nifti file.
    dicom_directory = None
    dicom_list = dicom2nifti.common.read_dicom_directory(dicom_directory)
    # TODO: add to dicom_array_to_nifti kwargs to save output and read instead of converting if present.
    nifti_dict = dicom2nifti.convert.dicom_array_to_nifti(dicom_list=dicom_list, output_file=None, reorient_nifti=True)
    nifti_image = nifti_dict['NIFTI']
    nifti_file_path = nifti_dict['NII_FILE']

    