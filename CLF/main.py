import dicom2nifti

def main():

    # Read directory of dicom files into a single 3D nifti file.
    
    dicom_directory = input("Please enter folder.")
    from nipype.interfaces.dcm2nii import Dcm2niix
    converter = Dcm2niix()
    converter.inputs.source_dir = dicom_directory
    converter.inputs.compression = 5
    converter.inputs.output_dir = dicom_directory
    converter.cmdline
    converter.run() 

    from myfunctions import prompt_demographics
    age, sex = prompt_demographics()

    #class dicom2nifti.convert_dicom.Vendor
    #GE = input("Please state vendor - '2' for GE")
    #dicom_list = dicom2nifti.common.read_dicom_directory(dicom_directory)
    # TODO: add to dicom_array_to_nifti kwargs to save output and read instead of converting if present.
    #nifti_dict = dicom2nifti.convert_dicom.are_imaging_dicoms(dicom_list)
    #dicom2nifti.convert_dicom.dicom_series_to_nifti(original_dicom_directory, output_file='.', reorient_nifti=True)    
    #nifti_image = nifti_dict['NIFTI']
    #nifti_file_path = nifti_dict['NII_FILE']


main()    
