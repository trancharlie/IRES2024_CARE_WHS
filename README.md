# IRES2024_CARE_WHS

We provide the testing scripts and trained models used for the CARE2024 challenge which won 1st place performance on CT and MRI whole heart segmentation.

## Training code (possibly future to do)

A precise training code is not provided at the moment but can be relatively easily reproduced by familiarity with nnUNet's coding (setting environmental variables, data naming format, etc.). MedNeXt uses the nnUNet-v1 style convention. 

1. [MedNext](https://github.com/MIC-DKFZ/MedNeXt) 
2. [nnUNet-v1](https://github.com/MIC-DKFZ/nnUNet/tree/nnunetv1)
3. [DOMINO++](https://github.com/lab-smile/DOMINOPlusPlus)

# Training Code (Future Plans)

Precise training code is not provided at the moment but can be relatively easily reproduced with familiarity with nnUNet's coding principles (e.g., setting environment variables, following data naming conventions, etc.).


## Submitted Model Components
Our submitted model included an ensemble of the following:

1. A standard **MedNeXt-M-k3** model.
2. A **MedNeXt-M-k3** model with **DA5 augmentation**.
   - You can find the source code of the DA5 from the nnUNet github ([DA5](https://github.com/MIC-DKFZ/nnUNet/tree/nnunetv1/nnunet/training/network_training/nnUNet_variants/data_augmentation)).
3. A **MedNeXt-M-k3** model with **DOMINO++ loss** ([DOMINO++ GitHub](https://github.com/lab-smile/DOMINOPlusPlus)):  
   - This can be re-implemented by incorporating the DOMINO++ loss into the MedNeXt/nnUNet trainer.  
   - To achieve this, train a standard **MedNeXt-M-k3** model, obtain its output confusion matrix, and "invert" it to utilize DOMINO++ effectively.

## Tested models directory

Download the models from this microsoft onedrive link [(DOWNLOAD LINK)](https://uflorida-my.sharepoint.com/:f:/g/personal/charlietran_ufl_edu/Epzq9x5BWXBBqXo-8nSgB2UBLCKcVO-brofrIiApuBushQ?e=Lu8b1F). There is one for each model.

## Testing Script 

The entire prediction scripture should contain the following lines. 
1. The rename_images_nnunet_format takes input from the directory '../input/' and expects the data to be named "Case####_image.nii.gz" and converts this into an nnUNet-style name into the '../intermediate/image_nnunet_format/" directory with name Case_1021_0000.nii.gz where 0000 is the modality index (in the care challenge, as subjects do not have both CT and MRI, both are considered a single modality for z-score normalization).
2. The mednext_v1_predict lines are run with the --save_npz flag to save the probabiliies, and are ensembled (if this repo is uploaded as intended, it should work on its own in this repo. I think the original nnUNet / mednext requires a small modification to the prediction script because it expects the prediction to be on the same machine as it was trained).
3. The ensembling code averages and outputs as so (a small modificaion to the original MedNext to allow pairs and triple ensembles).
4. The script ``final_format'' changes the segmentation labels from [0,1,2, ....] into the CARE2024 specified format of pixel values [LV = 500, RV = 600, LA = 420, ....] and changes the output names from nnUNet-style into a specified format `CASE####_pred.nii.gz". 

```
python rename_images_nnunet_format.py

mednextv1_predict -i ../intermediate/image_nnunet_format/ -o ../intermediate/test_pred/3d_M/ -tr nnUNetTrainerV2_MedNeXt_M_kernel3 -m 3d_M -p nnUNetPlansv2.1_trgSp_1x1x1 -t 800 --save_npz

mednextv1_predict -i ../intermediate/image_nnunet_format/ -o ../intermediate/test_pred/3d_M_DA5/ -tr nnUNetTrainerV2_MedNeXt_M_kernel3 -m 3d_M_DA5 -p nnUNetPlansv2.1_trgSp_1x1x1 -t 800 --save_npz

mednextv1_predict -i ../intermediate/image_nnunet_format/ -o ../intermediate/test_pred/3d_M_DOMINO/ -tr nnUNetTrainerV2_MedNeXt_M_kernel3 -m 3d_M_DOMINO -p nnUNetPlansv2.1_trgSp_1x1x1 -t 800 --save_npz

mednextv1_ensemble -f "../intermediate/test_pred/3d_M/" "../intermediate/test_pred/3d_M_DA5/" "../intermediate/test_pred/3d_M_DOMINO/" -o "..//intermediate/test_pred/ENSEMBLE/" -pp "./nnUNet_trained_models/nnUNet/ensembles/Task800_MedNXT/ensemble_3d_M__nnUNetTrainerV2_MedNeXt_kernel3__nnUNetPlansv2.1_trgSp_1x1x1--3d_M_DA5__nnUNetTrainerV2_MedNeXt_kernel3__nnUNetPlansv2.1_trgSp_1x1x1--3d_M_DOMINO__nnUNetTrainerV2_MedNeXt_kernel3__nnUNetPlansv2.1_trgSp_1x1x1/postprocessing.json" --npz

python final_format.py
```

## Additional information for reproduction

Remember in nnUNet you need to set the environment variables inside your .bashrc file (I forget if this is technically required for testing, but it is definitely required for training). 
```
export nnUNet_raw_data_base="PATH_TO_YOUR_MEDNEXT/nnUNet_raw_data_base"
export nnUNet_preprocessed="PATH_TO_YOUR_MEDNEXT/nnUNet_preprocessed"
export RESULTS_FOLDER="PATH_TO_YOUR_MEDNEXT/nnUNet_trained_models"
```

Update it by 
```
source /home/username/.bashrc
```
You can verify if what you did was right by typing in terminal
```
echo $nnUNet_raw_data_base
```

### Other packages I may have used in the progression
May possibly be others that you need to install on the fly. The most imporant packages were installed above and usually other packages don't conflict so these should install easily.
```
pip install nibabel
pip install seaborn
pip install jupyter 
pip install scikit-learn
pip install cupy-cuda12x
pip install monai==1.1.0
```

## Contact Information

You may contact me at charlietran@ufl.edu for any questions or information.


