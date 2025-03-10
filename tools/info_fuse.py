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
    csv_file = pd.read_csv(r'../result_file/12321321.csv', header=0)
    for i in range(len(csv_file)):
        if patient_id == csv_file.iloc[i, 0].zfill(10):
            operation_data = csv_file.iloc[i, 1]
            diagnosis = csv_file.iloc[i, 2]
            name = csv_file.iloc[i, 3]
            sex = csv_file.iloc[i, 4]
            age = csv_file.iloc[i, 5]
            # print('operation_data:', operation_data)
            # print('diagnosis:', diagnosis)
            # print('sex', sex)
            # print('age', age)
            return [operation_data, diagnosis, name, sex, age]


def get_info(excelfile, result_file):
    excel_file = pd.read_excel(excelfile)
    # 删除第0列和第一列，并将第1列改为nii_file
    excel_file.drop(excel_file.columns[0], axis=1, inplace=True)
    excel_file.drop(excel_file.columns[0], axis=1, inplace=True)
    excel_file.insert(0, 'nii_file', np.nan)
    excel_file.insert(1, 'Age', np.nan)
    excel_file.insert(1, 'Sex', np.nan)
    excel_file.insert(1, 'Name', np.nan)
    excel_file.insert(1, 'Diagnosis', np.nan)
    excel_file.insert(1, 'Operation_data', np.nan)
    nii_dir = r'/media/spgou/ZYJ/Dataset/Nii_Dataset'
    print("Stage 1: Add hyperlink...")
    for i in tqdm(range(len(excel_file))):
        patient_id = excel_file.iloc[i, 8]
        check_date = str(int(excel_file.iloc[i, 16])) if not pd.isnull(excel_file.iloc[i, 16]) else '0'
        modality = excel_file.iloc[i, 41]
        # patient_dir = os.path.join(nii_dir, patient_id + '_' + check_date)
        # for modality_file in os.listdir(patient_dir):
        for patient in os.listdir(nii_dir):
            if patient_id == patient.split('_')[0] and check_date == patient.split('_')[1]:
                patient_dir = os.path.join(nii_dir, patient)
                for modality_file in os.listdir(patient_dir):
                    if modality_file.split('_')[1] == modality:
                        nii_file = os.path.join(patient_dir, modality_file)
                        # 把路径的前缀替换
                        nii_file = nii_file.replace(r'/media/spgou/ZYJ', r'G:')
                        # 添加nii文件的超链接
                        excel_file.iloc[i, 0] = '=HYPERLINK("{}", "{}")'.format(nii_file, nii_file)

    print('Stage 2: Fuse hospital operation info...')
    for i in tqdm(range(len(excel_file))):
        patient_id = excel_file.iloc[i, 8]
        info = load_csv(patient_id)
        print(info)
        if info:
            excel_file.iloc[i, 1] = info[0]
            excel_file.iloc[i, 2] = info[1]
            excel_file.iloc[i, 3] = info[2]
            excel_file.iloc[i, 4] = info[3]
            excel_file.iloc[i, 5] = info[4]
            # excel_file.to_excel(r'../result_file/temp.xlsx', index=False)
        print(excel_file.iloc[i, 0:6])
    # data.to_excel(r'../result_file/fused_patient_result.xlsx', index=False)
    excel_file.to_excel(result_file, index=False)


# def fuse_csv(input_excel, output_excel):
#     data = pd.read_excel(input_excel)
#     data.insert(1, 'Age', np.nan)
#     data.insert(1, 'Sex', np.nan)
#     data.insert(1, 'Name', np.nan)
#     data.insert(1, 'Diagnosis', np.nan)
#     data.insert(1, 'Operation_data', np.nan)
#
#     print('Stage 2: Fuse hospital operation info...')
#     for i in tqdm(range(len(data))):
#         patient_id = data.iloc[i, 8]
#         info = load_csv(patient_id)
#         print(info)
#         if info:
#             data.iloc[i, 1] = info[0]
#             data.iloc[i, 2] = info[1]
#             data.iloc[i, 3] = info[2]
#             data.iloc[i, 4] = info[3]
#             data.iloc[i, 5] = info[4]
#         print(data.iloc[i, 1:6])
#     data.to_excel(output_excel, index=False)


if __name__ == "__main__":
    get_info(r'../result_file/selected_result_v1.xlsx', result_file=r'../result_file/fused_result.xlsx')
    # fuse_csv(r'../result_file/fused_result.xlsx', r'../result_file/fused_patient_result.xlsx')
