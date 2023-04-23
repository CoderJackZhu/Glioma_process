import os
import shutil
import pandas as pd
from tqdm import tqdm
import numpy as np


def select4mod(input_dir, output_dir):
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        modalities = os.listdir(patient_dir)
        modalities = list(set([modality.split('.')[0].split('_')[1] for modality in modalities]))
        if len(modalities) == 4:
            if not os.path.exists(os.path.join(output_dir, patient)):
                os.mkdir(os.path.join(output_dir, patient))
            for modality in os.listdir(patient_dir):
                modality_file = os.path.join(patient_dir, modality)
                shutil.copy(modality_file, os.path.join(output_dir, patient, modality))



if __name__ == '__main__':
    input_dir = r"/media/spgou/ZYJ/Nii_Dataset_RAI_Registered"
    output_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_4mod"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    select4mod(input_dir, output_dir)
