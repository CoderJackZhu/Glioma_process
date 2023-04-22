# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :info_fuse.py
# @Time         :2023/4/21 18:24
# @Author       :Jack Zhu

import os
import shutil
import numpy as np
import pandas as pd
from tqdm import tqdm


def get_info(excelfile, result_file):
    excel_file = pd.read_excel(excelfile)
    # csv_file = pd.read_csv(r'../result_file/12321321.csv')
    excel_file.insert(2, 'nii_file', np.nan)

    nii_dir = r'/media/spgou/ZYJ/Nii_Dataset'
    for i in tqdm(range(len(excel_file))):
        patient_id = excel_file.iloc[i, 5]
        check_date = str(int(excel_file.iloc[i, 13])) if not np.isnan(excel_file.iloc[i, 13]) else 'nan'
        modality = excel_file.iloc[i, 38]
        # patient_dir = os.path.join(nii_dir, patient_id + '_' + check_date)
        # for modality_file in os.listdir(patient_dir):
        for patient in os.listdir(nii_dir):
            if patient_id == patient.split('_')[0]:
                patient_dir = os.path.join(nii_dir, patient)
                for modality_file in os.listdir(patient_dir):
                    if modality_file.split('_')[1] == modality:
                        nii_file = os.path.join(patient_dir, modality_file)
                        # 给excel表格添加nii文件路径的超链接
                        excel_file.iloc[i, 2] = '=HYPERLINK("{}", "{}")'.format(nii_file, nii_file.split(os.sep)[-1])

    excel_file.to_excel(result_file, index=False)


if __name__ == "__main__":
    get_info(r'../result_file/selected_result.xlsx', result_file=r'../result_file/fused_result.xlsx')
