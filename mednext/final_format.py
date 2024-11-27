import os
import shutil
import re
import os
import nibabel as nib
import numpy as np


## PURPOSE OF THIS CODE IS TO UNDO THE FILE NAMING AND TO REMAP THE SEGMENTATION LABELS INTO [0,1,2,3,4,5,...]

# Function to rename and move files
def rename_and_move_files(source_folder, destination_folder):
    # Ensure destination folder exists, create if it doesn't
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through files in the source folder
    for filename in os.listdir(source_folder):
        # Check if file is a nii.gz file
        if filename.endswith('.nii.gz'):
            # Extract ID from filename using regex
            match = re.search(r'Case_(\d+)\.nii\.gz', filename)
            if match:
                id_number = match.group(1)
                new_filename = f'Case{id_number}_pred.nii.gz'
                
                # Construct full paths
                source_path = os.path.join(source_folder, filename)
                destination_path = os.path.join(destination_folder, new_filename)
                
                # Rename and move the file
                shutil.copy(source_path, destination_path)
                print(f'Moved {filename} to {destination_path}')

                
def segmentation_format(input_dir, output_dir):

    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ### SEGMENTATION PART OF CODE
    # Define the label mapping
    label_mapping = {
        0: 0,   # Background (unchanged)
        1: 500, # LV
        2: 600, # RV
        3: 420, # LA
        4: 550, # RA
        5: 205, # Myo
        6: 820, # AO
        7: 850  # PA
    }
    # Iterate through each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.nii.gz'):
            # Load the NIfTI file
            filepath = os.path.join(input_dir, filename)
            nii_img = nib.load(filepath)
            data = nii_img.get_fdata()

            # Remap labels according to label_mapping
            remapped_data = np.zeros_like(data, dtype=np.int16)  # Use appropriate dtype
            for orig_label, new_label in label_mapping.items():
                remapped_data[data == orig_label] = new_label

            # Ensure remapped data is integer type
            remapped_data = remapped_data.astype(np.int16)  # Adjust dtype as needed

            # Create a new NIfTI image with remapped data
            remapped_nii = nib.Nifti1Image(remapped_data, nii_img.affine, nii_img.header, dtype = np.int16)

            # Save the remapped NIfTI file
            #output_filename = filename.replace('_pred.nii.gz', '_remapped.nii.gz')  # Adjust output filename if needed
            output_filename = filename 
            output_filepath = os.path.join(output_dir, output_filename)
            nib.save(remapped_nii, output_filepath)

            print(f'Remapped file saved: {output_filename}')
            
            
            
            
# Replace with your actual source and destination folder paths
source_folder = '../intermediate/test_pred/ENSEMBLE/'
destination_folder = '../intermediate/test_pred_reverse_name/'

# Call the function to rename and move files
rename_and_move_files(source_folder, destination_folder)

### Input and output directories for segmentation
input_dir = '../intermediate/test_pred_reverse_name/'
output_dir = '../output/'

segmentation_format(input_dir, output_dir)


