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


