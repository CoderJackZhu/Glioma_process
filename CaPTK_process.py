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
from tools.utils import select4mod, rename2net, check_info, check_if_operation


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


def split_if_operation(source_dir, dest_dir):
    """
    将手术前后的数据分开
    """
    print('Step2: Split if operation')
    before_operation_dir = os.path.join(dest_dir, 'before_operation')
    after_operation_dir = os.path.join(dest_dir, 'after_operation')
    patient_dirs = os.listdir(source_dir)
    for patient_dir in tqdm(patient_dirs):
        patient_id = patient_dir.split('_')[0]
        patient_data = patient_dir.split('_')[1]
        not_operation = check_if_operation(patient_id, patient_data)
        patient_dir_path = os.path.join(source_dir, patient_dir)
        if not_operation:
            patient_dest_dir = os.path.join(before_operation_dir, patient_dir)
        else:
            patient_dest_dir = os.path.join(after_operation_dir, patient_dir)
        if not os.path.exists(patient_dest_dir):
            os.mkdir(patient_dest_dir)
        shutil.copy(patient_dir_path, patient_dest_dir)


def anonymize_patient(source_dir, dest_dir):
    """
    从匿名表格中获取对应信息并更改为匿名化后的编号
    """
    anonymize_info = pd.read_excel('reference/Preprocess/anonymous_table.xlsx')
    print('Step3: Anonymize patient')
    for i in tqdm(len(anonymize_info)):
        patient_id = anonymize_info.loc[i, 'PatientID']
        patient_anonymize_id = anonymize_info.loc[i, 'PatientID_anonymized']
        patient_dirs = os.listdir(source_dir)
        for patient_dir in patient_dirs:
            if patient_dir.split('_')[0] == patient_id:
                patient_dir_path = os.path.join(source_dir, patient_dir)
                patient_anonymize_dir = patient_anonymize_id + '_' + patient_dir.split('_')[1]
                # Gliomas_00001_id_data
                patient_anonymize_dir_path = os.path.join(dest_dir, patient_anonymize_dir)
                if not os.path.exists(patient_anonymize_dir_path):
                    os.mkdir(patient_anonymize_dir_path)
                shutil.copy(patient_dir_path, patient_anonymize_dir_path)


def brats_preprocess_captk(nii_dir, dest_dir, tools_path='C:\\CaPTk_Full\\1.9.0\\bin'):
    """
    使用CaPTK的预处框架进行预处理
    """
    print('Step4: CaPTK preprocess')
    tools = os.path.join(tools_path, 'BraTSPipeline.exe')
    patient_dirs = os.listdir(nii_dir)
    for patient_dir in tqdm(patient_dirs):
        patient_dir_path = os.path.join(nii_dir, patient_dir)
        patient_dest_dir = os.path.join(dest_dir, patient_dir)
        if not os.path.exists(patient_dest_dir):
            os.mkdir(patient_dest_dir)
        modality_files = os.listdir(patient_dir_path)
        for modality_file in modality_files:
            modality = modality_file.split('.')[0].split('_')[-1]
            if modality == 'T1':
                t1_file = os.path.join(patient_dir_path, modality_file)
            elif modality == 'T1+C':
                t1C_file = os.path.join(patient_dir_path, modality_file)
            elif modality == 'T2':
                t2_file = os.path.join(patient_dir_path, modality_file)
            elif modality == 'FLAIR':
                flair_file = os.path.join(patient_dir_path, modality_file)
            else:
                print('Wrong modality{} in {}'.format(modality, patient_dir))
            # 确认四个模态文件都存在
            if os.path.exists(t1_file) and os.path.exists(t1C_file) and os.path.exists(t2_file) and os.path.exists(
                    flair_file):
                cmd = tools + '-t1 ' + t1_file + ' -t1c ' + t1C_file + ' -t2 ' + t2_file + ' -fl ' + \
                      flair_file + ' -o ' + patient_dest_dir
                try:
                    os.system(cmd)
                except Exception as e:
                    print('Error in {}'.format(patient_dir))
            else:
                print('Missing modality file in {}'.format(patient_dir))

        # 命令后可以加参数-b 0 设置不进行分割
        # 参数解释Optional parameters:
        # 
        # [  -u, --usage]        Prints basic usage message
        # 
        # [  -h, --help]         Prints verbose usage information
        # 
        # [  -v, --version]      Prints information about software version
        # 
        # [ -rt, --runtest]      Runs the tests
        # 
        # [-cwl, --cwl]          Generates a .cwl file for the software
        # 
        # [  -s, --skullStrip]   Flag whether to skull strip or not
        #                        Defaults to 1
        #                        This uses DeepMedic: https://cbica.github.io/CaPTk/seg_DL.html
        # 
        # [  -b, --brainTumor]   Flag whether to segment brain tumors or not
        #                        Defaults to 1
        #                        This uses DeepMedic: https://cbica.github.io/CaPTk/seg_DL.html
        # 
        # [  -d, --debug]        Print debugging information
        #                        Defaults to 1
        # 
        # [  -i, --interFiles]   Save intermediate files
        #                        Defaults to 1
        # 
        # [  -p, --patientID]    Patient ID to pre-pend to final output file names
        #                        If empty, final output is of the form ${modality}_to_SRI.nii.gz


if __name__ == "__main__":
    batch_dcm2nii_captk(dest_dir='./result_file/captk_nii', pool_num=8, tools_path='C:\\CaPTk_Full\\1.9.0\\bin')
    select4mod('./result_file/captk_nii', './result_file/captk_nii_4mod')
    split_if_operation('./result_file/captk_nii_4mod', './result_file/captk_nii_4mod_operation')
    anonymize_patient('./result_file/captk_nii_4mod_operation/before_operation',
                      './result_file/captk_nii_4mod_before_operation_anonymize')
    brats_preprocess_captk('./result_file/captk_nii_4mod_operation/before_operation_anonymize',
                           './result_file/captk_nii_4mod_before_operation_anonymize_processed',
                           tools_path='C:\\CaPTk_Full\\1.9.0\\bin')
