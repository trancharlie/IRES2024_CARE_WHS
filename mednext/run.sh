#!/bin/bash
#SBATCH --job-name=ALL    # Job name
#SBATCH --mail-type=ALL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=charlietran@ufl.edu    # Where to send mail
#SBATCH --nodes=1
#SBATCH --ntasks=1       
#SBATCH --cpus-per-task=10
#SBATCH --mem-per-cpu=10gb
#SBATCH --time=12:00:00               # Time limit hrs:min:sec
#SBATCH --output=RUN_%j.log   # Standard output and error log
#SBATCH --account=joel.harley
#SBATCH --qos=joel.harley
#SBATCH --partition=gpu
#SBATCH --gpus=a100:1

# OPTION 2: SELF CREATED ENV
module load conda
conda activate /home/charlietran/conda/envs/dockerwhs/
export PATH=/home/charlietran/conda/envs/dockerwhs/bin:$PATH
cd /blue/joel.harley/charlietran/docker_care/mednext/

python rename_images_nnunet_format.py

mednextv1_predict -i ../intermediate/image_nnunet_format/ -o ../intermediate/test_pred/3d_M/ -tr nnUNetTrainerV2_MedNeXt_M_kernel3 -m 3d_M -p nnUNetPlansv2.1_trgSp_1x1x1 -t 800 --save_npz

mednextv1_predict -i ../intermediate/image_nnunet_format/ -o ../intermediate/test_pred/3d_M_DA5/ -tr nnUNetTrainerV2_MedNeXt_M_kernel3 -m 3d_M_DA5 -p nnUNetPlansv2.1_trgSp_1x1x1 -t 800 --save_npz

mednextv1_predict -i ../intermediate/image_nnunet_format/ -o ../intermediate/test_pred/3d_M_DOMINO/ -tr nnUNetTrainerV2_MedNeXt_M_kernel3 -m 3d_M_DOMINO -p nnUNetPlansv2.1_trgSp_1x1x1 -t 800 --save_npz

mednextv1_ensemble -f "../intermediate/test_pred/3d_M/" "../intermediate/test_pred/3d_M_DA5/" "../intermediate/test_pred/3d_M_DOMINO/" -o "..//intermediate/test_pred/ENSEMBLE/" -pp "./nnUNet_trained_models/nnUNet/ensembles/Task800_MedNXT/ensemble_3d_M__nnUNetTrainerV2_MedNeXt_kernel3__nnUNetPlansv2.1_trgSp_1x1x1--3d_M_DA5__nnUNetTrainerV2_MedNeXt_kernel3__nnUNetPlansv2.1_trgSp_1x1x1--3d_M_DOMINO__nnUNetTrainerV2_MedNeXt_kernel3__nnUNetPlansv2.1_trgSp_1x1x1/postprocessing.json" --npz

python final_format.py

date
