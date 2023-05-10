# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :utils.py
# @Time         :2023/5/10 17:12
# @Author       :Jack Zhu

import os
import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os
import shutil
import pandas as pd
from tqdm import tqdm


def check_info(patient_path):
    """
    确认nii.gz文件中含有病人的多少信息
    """
    # info = []
    for file in os.listdir(patient_path):
        if file.endswith(".nii"):
            file_path = os.path.join(patient_path, file)
            img = nib.load(file_path)
            meta_data = img.header
            for key in meta_data:
                print(key, meta_data[key])


def select4mod(input_dir, output_dir):
    print('select 4 modality full data')
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        modalities = [modality for modality in os.listdir(patient_dir) if modality.endswith('.nii')]
        modalities = list(set([modality.split('.')[0].split('_')[-1] for modality in modalities]))
        if len(modalities) == 4:
            if not os.path.exists(os.path.join(output_dir, patient)):
                os.mkdir(os.path.join(output_dir, patient))
            for modality in os.listdir(patient_dir):
                modality_file = os.path.join(patient_dir, modality)
                shutil.copy(modality_file, os.path.join(output_dir, patient, modality))

# if __name__ == '__main__':
#     input_dir = r"/media/spgou/ZYJ/Nii_Dataset_RAI_Registered"
#     output_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_4mod"
#     if not os.path.exists(output_dir):
#         os.mkdir(output_dir)
#     select4mod(input_dir, output_dir)


def rename2net(input_dir, output_dir):
    """
    将nii.gz文件重命名为nnUNet需要的格式
    """
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        modalities = os.listdir(patient_dir)
        for modality in tqdm(modalities):
            modality_file = os.path.join(patient_dir, modality)
            # med_image = nib.load(modality_file)
            # try:
            #     med_image = med_image.get_fdata()
            #     if med_image.shape != (240, 240, 155):
            #         print('Warning: modality shape error! modality shape is: {}'.format(med_image.shape))
            #         continue
            # except Exception as e:
            #     print('Warning: modality info error! modality info is: {}'.format(e))

            if len(modality.split('.')[0].split('_')) == 3 or modality.split('.')[0].split('_')[-1] == 't1mask':
                patient_id = modality.split('.')[0].split('_')[0]
                patient_date = modality.split('.')[0].split('_')[2]
                modality_type = modality.split('.')[0].split('_')[1]
                if modality_type == 'T1':
                    modality_id = '0000'
                elif modality_type == 'T1+C':
                    modality_id = '0001'
                elif modality_type == 'T2':
                    modality_id = '0002'
                elif modality_type == 'T2FLAIR':
                    modality_id = '0003'
                else:
                    # 警告
                    print('Warning: modality type error! modality type is: {}'.format(modality_type))
                    continue
                new_modality_name = patient_id + '_' + patient_date + '_' + modality_id + '.nii.gz'
                new_modality_file = os.path.join(output_dir, new_modality_name)
                if os.path.exists(new_modality_file):
                    continue
                shutil.copy(modality_file, new_modality_file)
            else:
                continue

# if __name__ == '__main__':
#     input_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_4mod_skulled"
#     output_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_4mod_skulled_rename"
#     rename2net(input_dir, output_dir)


def filter_normal(input_dir, output_dir):
    """
    本代码用于把nii.gz格式的医学影像中不正常的数据，比如全黑的数据剔除掉
    """
    average = []
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        if not os.path.exists(os.path.join(output_dir, patient)):
            os.mkdir(os.path.join(output_dir, patient))
        for modality in os.listdir(patient_dir):
            modality_file = os.path.join(patient_dir, modality)
            # 读取nii.gz文件
            data = nib.load(modality_file)
            # 获取nii.gz文件的数据
            try:
                data = data.get_fdata()
            except:
                continue
            # 计算每个像素的平均值
            mean = np.mean(data)
            average.append(mean)
    average = np.array(average)
    # 计算平均值的标准差
    std = np.std(average)
    # 计算平均值的均值
    mean = np.mean(average)
    # 计算平均值的上下界
    upper = mean + 3 * std
    lower = mean - 3 * std
    print('mean:', mean)
    print('std:', std)
    print('upper:', upper)
    print('lower:', lower)

    # 把不正常的数据剔除掉
    # 绘制直方图
    plt.hist(average, bins=100)
    plt.show()
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        if not os.path.exists(os.path.join(output_dir, patient)):
            os.mkdir(os.path.join(output_dir, patient))
        for modality in os.listdir(patient_dir):
            modality_file = os.path.join(patient_dir, modality)
            data = nib.load(modality_file)
            try:
                data = data.get_fdata()
                if data.shape != (240, 240, 155):
                    continue
            except Exception as e:
                continue
            mean = np.mean(data)
            if lower < mean < upper:
                shutil.copy(modality_file, os.path.join(output_dir, patient, modality))


def split_case_by_time(data_dir=r".\RAI_xiangya_Dataset"):
    case_dir_list = [os.path.join(data_dir, case) for case in os.listdir(data_dir)]

    for case_dir in tqdm(case_dir_list):

        nifty_path_list = [os.path.join(case_dir, nifty) for nifty in os.listdir(case_dir)]
        nifty_split_by_time = {}
        for nifty_path in nifty_path_list:
            time = nifty_path.split("_")[-1].replace(".nii.gz", '')
            if time not in nifty_split_by_time.keys():
                nifty_split_by_time[time] = []
            nifty_split_by_time[time].append(nifty_path)

        target_case_dir_list = [case_dir + "_" + time for time in nifty_split_by_time]
        for target_case_dir in target_case_dir_list:
            os.mkdir(target_case_dir)

        for time, nifty_path_list in nifty_split_by_time.items():
            target_case_dir = case_dir + "_" + time
            for nifty_path in nifty_path_list:
                target_nifty_path = os.path.join(target_case_dir, nifty_path.split(os.sep)[-1])
                shutil.copy(nifty_path, target_nifty_path)

        shutil.rmtree(case_dir)


def check_if_operation(patient_id, check_date):
    operation_info = pd.read_csv('result_file/12321321.csv')
    for i in range(len(operation_info)):
        id = operation_info.iloc[i, 0].zfill(10)
        operation_data = operation_info.iloc[i, 1]
        if id == patient_id:
            if type(operation_data) == float:
                return False
            operation_data = str(operation_data).replace('-', '').split(' ')[0]
            if int(check_date) < int(operation_data):
                return True
            else:
                return False
    return False


if __name__ == "__main__":
    run_code = 0
