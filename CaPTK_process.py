# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :CaPTK_process.py
# @Time         :2023/5/9 22:47
# @Author       :Jack Zhu


import os
# import sys
import numpy as np
# import nibabel as nib
# import matplotlib.pyplot as plt
# import SimpleITK as sitk
import shutil
from tqdm import tqdm
import pandas as pd
from multiprocessing import Pool
from tools.utils import select4mod, rename2net, check_info, check_if_operation


def dcm2nii_captk(dcm_dir='./test_data/SE11', output_path='./test_data', tools_path='C:\\CaPTk_Full\\1.9.0\\bin'):
    """
    使用CaPTK的dcm2nii将dcm文件转换为nii.gz文件
    """
    if not os.path.exists(output_path):
        os.mkdir(output_path)
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
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    if os.path.exists('./result_file/use_dir_list.npy'):
        dir_list = np.load('./result_file/use_dir_list.npy', allow_pickle=True)
    else:
        info = pd.read_excel('./result_file/fused_result_v2.xlsx')
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
        if modality not in ['T1', 'T1+C', 'T2', 'T2FLAIR']:
            continue
        dir_path = dir_list[i]['dir_path']
        dir_path = os.path.normpath(dir_path)
        # print(dir_path)
        patient_id = str(dir_list[i]['patient_id'])
        patient_study_date = str(int(dir_list[i]['StudyDate']))
        patient_dir = os.path.join(dest_dir, patient_id + '_' + patient_study_date)
        if not os.path.exists(patient_dir):
            os.mkdir(patient_dir)
        modality_dir = os.path.join(patient_dir, modality)
        if not os.path.exists(modality_dir):
            os.mkdir(modality_dir)
        pool.apply_async(dcm2nii_captk, args=(dir_path, modality_dir, tools_path))
    pool.close()
    pool.join()


def rename2normal(source_dir, dest_dir):
    """
    将CaPTK转换后的文件名改为普通格式即每个病人日期文件夹下包含id+模态T1、T1+C、T2、T2FLAIR+日期四个文件
    """
    print('Step2: rename')
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    patient_dirs = os.listdir(source_dir)
    for patient_dir in tqdm(patient_dirs):
        patient_id = patient_dir.split('_')[0]
        patient_data = patient_dir.split('_')[1]
        patient_dir_path = os.path.join(source_dir, patient_dir)
        patient_dest_dir = os.path.join(dest_dir, patient_id + '_' + patient_data)
        if not os.path.exists(patient_dest_dir):
            os.mkdir(patient_dest_dir)
        modality_dirs = os.listdir(patient_dir_path)
        for modality_dir in modality_dirs:
            modality_dir_path = os.path.join(patient_dir_path, modality_dir)
            files = os.listdir(modality_dir_path)
            files = [file for file in files if file.endswith('.nii')]
            if len(files) == 1:
                modality_file = files[0]
                modality_file_path = os.path.join(modality_dir_path, modality_file)
            elif len(files) == 0:
                continue
            else:
                axi_files = [file for file in files if 'ax' in file or 'Ax' in file]
                if len(axi_files) == 0:
                    modality_file = files[0]
                else:
                    modality_file = axi_files[0]
                modality_file_path = os.path.join(modality_dir_path, modality_file)
            shutil.copy(modality_file_path,
                        os.path.join(patient_dest_dir, patient_id + '_' + patient_data + '_' + modality_dir + '.nii.gz'))


def split_if_operation(source_dir, dest_dir):
    """
    将手术前后的数据分开
    """
    print('Step4: Split if operation')
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    before_operation_dir = os.path.join(dest_dir, 'before_operation')
    after_operation_dir = os.path.join(dest_dir, 'after_operation')
    if not os.path.exists(before_operation_dir):
        os.mkdir(before_operation_dir)
    if not os.path.exists(after_operation_dir):
        os.mkdir(after_operation_dir)
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
        shutil.copytree(patient_dir_path, patient_dest_dir)


def anonymize_patient(source_dir, dest_dir):
    """
    从匿名表格中获取对应信息并更改为匿名化后的编号
    """
    print('Step5: Anonymize patient')
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    anonymize_info = pd.read_excel('reference/Preprocess/anonymous_table.xlsx')
    for i in tqdm(range(len(anonymize_info))):
        patient_id = anonymize_info.loc[i, 'PatientID']
        patient_anonymize_id = anonymize_info.loc[i, 'PatientID_anonymized']
        patient_dirs = os.listdir(source_dir)
        for patient_dir in patient_dirs:
            if patient_dir.split('_')[0] == patient_id:
                patient_dir_path = os.path.join(source_dir, patient_dir)
                patient_anonymize_dir = patient_anonymize_id + '_' + patient_dir.split('_')[1]
                # Gliomas_00001_id_data
                patient_anonymize_dir_path = os.path.join(dest_dir, patient_anonymize_dir)
                shutil.copytree(patient_dir_path, patient_anonymize_dir_path)
                # 重命名文件夹中的文件
                patient_anonymize_files = os.listdir(patient_anonymize_dir_path)
                for patient_anonymize_file in patient_anonymize_files:
                    patient_anonymize_file_path = os.path.join(patient_anonymize_dir_path, patient_anonymize_file)
                    patient_anonymize_file_new_name = patient_anonymize_file.replace(patient_id, patient_anonymize_id)
                    patient_anonymize_file_new_name_path = os.path.join(patient_anonymize_dir_path, patient_anonymize_file_new_name)
                    os.rename(patient_anonymize_file_path, patient_anonymize_file_new_name_path)



def brats_preprocess_captk(nii_dir, dest_dir):
    """
    使用CaPTK的预处框架进行预处理
    """
    print('Step6: CaPTK preprocess')
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    tools = 'C:/CaPTk_Full/1.9.0/bin/BraTSPipeline.exe'
    tools = os.path.normpath(tools)
    cmd_list = []
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
                t1c_file = os.path.join(patient_dir_path, modality_file)
            elif modality == 'T2':
                t2_file = os.path.join(patient_dir_path, modality_file)
            elif modality == 'T2FLAIR':
                flair_file = os.path.join(patient_dir_path, modality_file)
            else:
                print('Wrong modality{} in {}'.format(modality, patient_dir))
            # 确认四个模态文件都存在
        if os.path.exists(t1_file) and os.path.exists(t1c_file) and os.path.exists(t2_file) and os.path.exists(
                flair_file):
            cmd = tools + ' -t1 ' + t1_file + ' -t1c ' + t1c_file + ' -t2 ' + t2_file + ' -fl ' + \
                  flair_file + ' -o ' + patient_dest_dir + ' -b 0'
            print(cmd)
            cmd_list.append(cmd)
        #     try:
        #         os.system(cmd)
        #     except Exception as e:
        #         print('Error in {}'.format(patient_dir))
        # else:
        #     print('Missing modality file in {}'.format(patient_dir))
    # 多进程运行
    pool = Pool(processes=4)
    pool.map(os.system, cmd_list)
    pool.close()
    pool.join()
    # 命令后可以加参数-b 0 设置不进行分割


def extract_4mod_segment(patient_dir, patient_normal_dir, patient_seg_dir):
    """
    从captk结果中提取四个模态的数据和分割结果
    """
    if not os.path.exists(patient_normal_dir):
        os.mkdir(patient_normal_dir)
    if not os.path.exists(patient_seg_dir):
        os.mkdir(patient_seg_dir)
    patients = os.path.basename(patient_dir)
    patient_id = patients.split('_')[0]
    patient_date = patients.split('_')[1]
    t1_file = os.path.join(patient_dir, 'T1_to_SRI_brain.nii.gz')
    t1c_file = os.path.join(patient_dir, 'T1CE_to_SRI_brain.nii.gz')
    t2_file = os.path.join(patient_dir, 'T2_to_SRI_brain.nii.gz')
    fl_file = os.path.join(patient_dir, 'FL_to_SRI_brain.nii.gz')
    seg_file = os.path.join(patient_dir, 'brainTumorMask_SRI.nii.gz')
    try:
        shutil.copy(t1_file, os.path.join(patient_normal_dir, patient_id + '_' + patient_date + '_T1' + '.nii.gz'))
        shutil.copy(t1c_file,
                    os.path.join(patient_normal_dir, patient_id + '_' + patient_date + '_T1+C' + '.nii.gz'))
        shutil.copy(t2_file, os.path.join(patient_normal_dir, patient_id + '_' + patient_date + '_T2' + '.nii.gz'))
        shutil.copy(fl_file,
                    os.path.join(patient_normal_dir, patient_id + '_' + patient_date + '_T2FLAIR' + '.nii.gz'))
        shutil.copy(seg_file, os.path.join(patient_seg_dir, patient_id + '_' + patient_date + '.nii.gz'))
    except Exception as e:
        print('Error in {}'.format(patient_dir))


def batch_extract_4mod_segment(source_dir, dest_dir, seg_dir):
    """
    批量提取captk结果中的四个模态数据和分割结果
    """
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    if not os.path.exists(seg_dir):
        os.mkdir(seg_dir)
    patient_dirs = os.listdir(source_dir)
    for patient_dir in patient_dirs:
        patient_normal_dir = os.path.join(dest_dir, patient_dir)
        extract_4mod_segment(os.path.join(source_dir, patient_dir), patient_normal_dir, seg_dir)


if __name__ == "__main__":
    # batch_dcm2nii_captk(dest_dir='D:/ZYJ/Dataset/captk_nii', pool_num=12, tools_path='C:/CaPTk_Full/1.9.0/bin')
    # rename2normal(source_dir='D:/ZYJ/Dataset/captk_nii', dest_dir='D:/ZYJ/Dataset/captk_nii_rename')
    # select4mod('D:/ZYJ/Dataset/captk_nii_rename', 'D:/ZYJ/Dataset/captk_nii_4mod')
    # split_if_operation('D:/ZYJ/Dataset/captk_nii_4mod', 'D:/ZYJ/Dataset/captk_nii_4mod_operation')
    # anonymize_patient('D:/ZYJ/Dataset/captk_nii_4mod_operation/before_operation',
    #                   'D:/ZYJ/Dataset/captk_nii_4mod_before_operation_anonymize')
    brats_preprocess_captk('D:/ZYJ/Dataset/captk_nii_4mod_before_operation_anonymize',
                           'D:/ZYJ/Dataset/captk_nii_4mod_before_operation_anonymize_processed')
    # brats_preprocess_captk('G:\\Dataset\\Nii_Dataset', 'G:\\Dataset\\Nii_Dataset_processed')
    batch_extract_4mod_segment('D:/ZYJ/Dataset/captk_nii_4mod_before_operation_anonymize_processed',
                               'D:/ZYJ/Dataset/captk_nii_4mod_before_operation_anonymize_processed_4mod',
                               'D:/ZYJ/Dataset/captk_nii_4mod_before_operation_anonymize_processed_seg')
