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
                return 'nan'
            operation_data = operation_info.iloc[i, 1].replace('-', '')
            if check_date < operation_data:
                return 'pre'
            else:
                return 'post'


def skull_strip(registrated_dir, skull_stripped_dir):
    pass


if __name__ == "__main__":
    registrated_dir = r"./Registrated"
    skull_stripped_dir = r"./skull_stripped"
    if not os.path.exists(skull_stripped_dir):
        os.mkdir(skull_stripped_dir)
    check_if_operation()
    skull_strip(registrated_dir, skull_stripped_dir)
