# -*- coding:utf-8 -*-
# @PROJECT_NAME :Dcm_process
# @FileName     :count_4modality.py
# @Time         :2023/4/5 20:44
# @Author       :Jack Zhu
import os
from tqdm import tqdm
import pandas as pd

# 按日期和病人ID划分，得到7433个文件夹
对其中每天每个病人的文件夹查找，找到4种模态全的文件夹，记录下来，共有2993个文件夹
def count(dir_path):
    files = os.listdir(dir_path)
    num_count = 0
    for file in tqdm(files):
        file_path = os.path.join(dir_path, file)
        nii_files = os.listdir(file_path)
        nii_list = []
        for nii_file in nii_files:
            nii_file_path = os.path.join(file_path, nii_file)
            modality = nii_file.split('_')[1]
            if modality not in nii_list:
                nii_list.append(modality)
        if len(nii_list) == 4:
            num_count += 1
            with open('result_file/4modality.txt', 'a') as f:
                f.write(file + '\n')


if __name__ == "__main__":
    dir_path = 'G:/Nii_Dataset'
    count(dir_path)
