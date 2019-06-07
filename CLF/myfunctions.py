def prompt_demographics():
   age = input("Please enter age in whole years: ")
   sex = input("Please enter sex (m/f): ")
   return age, sex

def my_dcm2niix(folder):
    # convert dcm series to nii.gz and .json using nipype and dcm2niix
    from nipype.interfaces.dcm2nii import Dcm2niix
    converter = Dcm2niix()
    converter.inputs.source_dir = folder
    converter.inputs.compression = 5
    converter.inputs.output_dir = folder
    converter.inputs.out_filename = '%i_%4s_%d'
    converter.cmdline
    converted_files = converter.run()
    return converted_files

