import os
import shutil
import pandas as pd
from tqdm import tqdm
import numpy as np
import SimpleITK as sitk


def check_if_operation(patient_id, check_date):
    operation_info = pd.read_csv('./reference/12321321.csv')
    for i in tqdm(range(len(operation_info))):
        id = operation_info.iloc[i, 0]
        if id == patient_id:
            if operation_info.iloc[i, 1] == 'nan':
                return False
            operation_data = operation_info.iloc[i, 1].replace('-', '')
            if check_date < operation_data:
                return True
            else:
                return False


def skull_strip(registrated_dir, skull_stripped_dir):
    for patient in tqdm(os.listdir(registrated_dir)):
        patient_id = patient.split('_')[0]
        patient_date = patient.split('_')[1]
        if_operation = check_if_operation(patient_id, patient_date)
        if not if_operation:
            continue
        patient_dir = os.path.join(registrated_dir, patient)
        if not os.path.exists(os.path.join(skull_stripped_dir, patient)):
            os.mkdir(os.path.join(skull_stripped_dir, patient))
        for modality in os.listdir(patient_dir):
            modality_file = os.path.join(patient_dir, modality)



if __name__ == "__main__":
    registrated_dir = r"./Registrated"
    skull_stripped_dir = r"./skull_stripped"
    if not os.path.exists(skull_stripped_dir):
        os.mkdir(skull_stripped_dir)
    check_if_operation()
    skull_strip(registrated_dir, skull_stripped_dir)
