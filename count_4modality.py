# -*- coding:utf-8 -*-
# @PROJECT_NAME :Dcm_process
# @FileName     :count_4modality.py
# @Time         :2023/4/5 20:44
# @Author       :Jack Zhu
import os
import pandas as pd

def count(file_path):
    files = os.listdir(file_path)
    num_count = 0
    for file in files:
        file_path = os.path.join(file_path, file)
        nii_files = os.listdir(file_path)
        nii_list  = []
        for nii_file in nii_files:
            nii_file_path = os.path.join(file_path, nii_file)
            modality = nii_file.split('_')[1]
            if modality not in nii_list:
                nii_list.append(modality)
        if len(nii_list) == 4:
            num_count += 1
            print(f'------------------{file}------------------')
            with open('result_file/4modality.txt', 'w') as f:
                f.write(file + '\n')



if __name__ == "__main__":
    file_path = 'G:/Nii_Dataset'
    count(file_path)
