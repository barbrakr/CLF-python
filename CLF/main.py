import dicom2nifti

def main():

    # Read directory of dicom files into a single 3D nifti file.
    
    dicom_directory = input("Please enter folder.")

    from myfunctions import prompt_demographics, my_dcm2niix
    age, sex = prompt_demographics()
    my_dcm2niix(dicom_directory)

main()    
