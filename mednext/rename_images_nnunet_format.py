import os
import shutil
import re

def rename_nii_files(source_dir, dest_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # List all files in the source directory
    files = os.listdir(source_dir)

    # Regular expression to match filenames like Case1021_image.nii.gz
    pattern = re.compile(r'Case(\d{4})_image.nii.gz')

    for filename in files:
        match = pattern.match(filename)
        if match:
            case_number = match.group(1)
            new_filename = f'Case_{case_number}_0000.nii.gz'
            source_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(dest_dir, new_filename)
            shutil.copyfile(source_path, dest_path)
            print(f'Renamed and copied: {filename} -> {new_filename}')

    print('All files renamed and copied.')

# Example usage:
source_directory = '../input/'
destination_directory = '../intermediate/image_nnunet_format/'
rename_nii_files(source_directory, destination_directory)
