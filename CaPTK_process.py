# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :CaPTK_process.py
# @Time         :2023/5/9 22:47
# @Author       :Jack Zhu


import os
import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import SimpleITK as sitk
import shutil
from tqdm import tqdm
import pandas as pd
from multiprocessing import Pool
from tools.utils import select4mod, rename2net, check_info, get_patient_path

def get_patient_path(root_path):
    pass


def dcm2nii_captk(dcm_dir='./test_data/SE11', output_path='./test_data', tools_path='C:\\CaPTk_Full\\1.9.0\\bin'):
    """
    使用CaPTK的dcm2nii将dcm文件转换为nii.gz文件
    """
    tools = os.path.join(tools_path, f'dcm2niix.exe')
    tools = os.path.normpath(tools)
    tools = tools.encode('gbk').decode('utf-8')
    cmd = f'{tools} -f %i_%p -o {output_path} {dcm_dir}'
    # dcm2niix.exe -o F:\Code\Medical\Glioma_process\test_data F:\Code\Medical\Glioma_process\test_data\SE10
    print(cmd)
    try:
        os.system(cmd)
    except Exception as e:
        print(e)

def batch_dcm2nii_captk(dest_dir, pool_num=8, tools_path='C:\\CaPTk_Full\\1.9.0\\bin'):
    """
    批量并行将dcm文件转换为nii.gz文件
    """
    print("Step1: dcm2nii")
    if os.path.exists('./result_file/use_dir_list.npy'):
        dir_list = np.load('./result_file/use_dir_list.npy', allow_pickle=True)
    else:
        info = pd.read_excel('./result_file/fused_result_v1.xlsx')
        dir_list = []
        for i in tqdm(range(len(info))):
            basic_info = {}
            file1_path = info.loc[i, 'ImagePath']
            dir_path = os.path.dirname(file1_path)
            file_count = len(os.listdir(dir_path))
            if file_count > 15:
                basic_info['dir_path'] = dir_path
                dir_list.append(basic_info)
            else:
                continue
            basic_info['patient_id'] = info.loc[i, 'PatientID']
            basic_info['modility'] = info.loc[i, 'MRISequence']
            basic_info['StudyDate'] = info.loc[i, 'StudyDate']
        np.save('./result_file/use_dir_list.npy', dir_list)
    pool = Pool(pool_num)
    for i in tqdm(range(len(dir_list))):
        # 筛掉不用的模态
        modality = dir_list[i]['modility']
        if modality not in ['T1', 'T1+C', 'T2', 'T2 FLAIR']:
            continue
        dir_path = dir_list[i]['dir_path']
        dir_path = os.path.normpath(dir_path)
        # print(dir_path)
        patient_id = str(dir_list[i]['patient_id'])
        patient_study_date = str(int(dir_list[i]['StudyDate']))
        patient_dir = os.path.join(dest_dir, patient_id + '_' + patient_study_date)
        if not os.path.exists(patient_dir):
            os.mkdir(patient_dir)
        pool.apply_async(dcm2nii_captk, args=(dir_path, patient_dir, tools_path))
    pool.close()
    pool.join()


def anonymize_patient(source_dir):
    """
    从匿名表格中获取对应信息并更改为匿名化后的编号
    """
    anonymize_info = pd.read_excel('reference/Preprocess/anonymous_table.xlsx')
    print('Step2: Anonymize patient')
    for i in tqdm(len(anonymize_info)):
        patient_id = anonymize_info.loc[i, 'PatientID']
        # TODO





if __name__ == "__main__":
    batch_dcm2nii_captk(dest_dir='./result_file/captk_nii', pool_num=8, tools_path='C:\\CaPTk_Full\\1.9.0\\bin')
    select4mod('./result_file/captk_nii', './result_file/captk_nii_4mod')