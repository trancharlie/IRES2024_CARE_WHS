# IRES2024_CARE_WHS

We provide the testing scripts and trained models used for the CARE2024 challenge which won 1st place performance on CT and MRI whole heart segmentation.

## Training code (possibly future to do)

A precise training code is not provided at the moment but can be relatively easily reproduced by familiarity with nnUNet's coding (setting environmental variables, data naming format, etc.). 

[1, MedNext] https://github.com/MIC-DKFZ/MedNeXt
[2, nnUNet-v1] https://github.com/MIC-DKFZ/nnUNet/tree/nnunetv1
[3, DOMINO++] https://github.com/lab-smile/DOMINOPlusPlus 

Our submitted model contained an ensemble of 
[1] A standard MedNext-M-k3 model
[2] A MedNeXt-M-k3 model with DA5 augmentation
[3] A MedNeXt-M-k3 model with DOMINO++ loss (https://github.com/lab-smile/DOMINOPlusPlus). This can re-implemented by adding the DOMINO++ loss into the MedNeXt/nnUNEt Trainer. By necessity, you need to train a standard MedNeXt-M-k3 model, and obtain its ouput confusion matrix and ``invert it'' to utilize DOMINO++. 

## Tested models directory

Download the models from this link

## Testing Script 

The order of prediction goes as follows

`` python rename_images_nnunet_format.py

mednextv1_predict -i ../intermediate/image_nnunet_format/ -o ../intermediate/test_pred/3d_M/ -tr nnUNetTrainerV2_MedNeXt_M_kernel3 -m 3d_M -p nnUNetPlansv2.1_trgSp_1x1x1 -t 800 --save_npz

mednextv1_predict -i ../intermediate/image_nnunet_format/ -o ../intermediate/test_pred/3d_M_DA5/ -tr nnUNetTrainerV2_MedNeXt_M_kernel3 -m 3d_M_DA5 -p nnUNetPlansv2.1_trgSp_1x1x1 -t 800 --save_npz

mednextv1_predict -i ../intermediate/image_nnunet_format/ -o ../intermediate/test_pred/3d_M_DOMINO/ -tr nnUNetTrainerV2_MedNeXt_M_kernel3 -m 3d_M_DOMINO -p nnUNetPlansv2.1_trgSp_1x1x1 -t 800 --save_npz

mednextv1_ensemble -f "../intermediate/test_pred/3d_M/" "../intermediate/test_pred/3d_M_DA5/" "../intermediate/test_pred/3d_M_DOMINO/" -o "..//intermediate/test_pred/ENSEMBLE/" -pp "./nnUNet_trained_models/nnUNet/ensembles/Task800_MedNXT/ensemble_3d_M__nnUNetTrainerV2_MedNeXt_kernel3__nnUNetPlansv2.1_trgSp_1x1x1--3d_M_DA5__nnUNetTrainerV2_MedNeXt_kernel3__nnUNetPlansv2.1_trgSp_1x1x1--3d_M_DOMINO__nnUNetTrainerV2_MedNeXt_kernel3__nnUNetPlansv2.1_trgSp_1x1x1/postprocessing.json" --npz

python final_format.py ''

