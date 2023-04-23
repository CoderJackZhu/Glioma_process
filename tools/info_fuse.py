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

def load_csv(patient_id):
    csv_file = pd.read_csv(r'../result_file/12321321.csv')
    for i in range(len(csv_file)):
        if patient_id == csv_file.iloc[i, 0]:
            operation_data = csv_file.iloc[i, 1]
            diagnosis = csv_file.iloc[i, 2]
            sex = csv_file.iloc[i, 3]
            age = csv_file.iloc[i, 4]
            print('operation_data:', operation_data)
            print('diagnosis:', diagnosis)
            print('sex', sex)
            print('age', age)
            return [operation_data, diagnosis, sex, age]


def get_info(excelfile, result_file):
    excel_file = pd.read_excel(excelfile)
    # 删除第0列和第一列，并将第1列改为nii_file
    excel_file.drop(excel_file.columns[0], axis=1, inplace=True)
    excel_file.drop(excel_file.columns[0], axis=1, inplace=True)
    excel_file.insert(0, 'nii_file', np.nan)

    nii_dir = r'/media/spgou/ZYJ/Nii_Dataset'
    print("Stage 1: Add hyperlink...")
    for i in tqdm(range(len(excel_file))):
        patient_id = excel_file.iloc[i, 3]
        check_date = str(int(excel_file.iloc[i, 11])) if not np.isnan(excel_file.iloc[i, 11]) else 'nan'
        modality = excel_file.iloc[i, 36]
        # patient_dir = os.path.join(nii_dir, patient_id + '_' + check_date)
        # for modality_file in os.listdir(patient_dir):
        for patient in os.listdir(nii_dir):
            if patient_id == patient.split('_')[0] and check_date == patient.split('_')[1]:
                patient_dir = os.path.join(nii_dir, patient)
                for modality_file in os.listdir(patient_dir):
                    if modality_file.split('_')[1] == modality:
                        nii_file = os.path.join(patient_dir, modality_file)
                        # 给excel表格添加nii文件路径的超链接
                        excel_file.iloc[i, 0] = '=HYPERLINK("{}", "{}")'.format(nii_file, nii_file.split(os.sep)[-1])

    excel_file.to_excel(result_file, index=False)

def fuse_csv(input_excel, output_excel):
    data = pd.read_excel(input_excel)
    data.insert(1, 'Operation_data', np.nan)
    data.insert(2, 'Diagnosis', np.nan)
    data.insert(3, 'Sex', np.nan)
    data.insert(4, 'Age', np.nan)
    print('Stage 2: Fuse hospital operation info...')
    for i in tqdm(range(len(data))):
        patient_id = data.iloc[i, 7]
        data.iloc[i, 1:5] = load_csv(patient_id)
    data.to_excel(output_excel, index=False)




if __name__ == "__main__":
    get_info(r'../result_file/selected_result_v1.xlsx', result_file=r'../result_file/fused_result.xlsx')
    fuse_csv(r'../result_file/fused_result.xlsx', r'../result_file/fused_patient_result.xlsx')
