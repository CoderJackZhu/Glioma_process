import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import shutil
import matplotlib.pyplot as plt
import nibabel as nib

'''
本代码用于把nii.gz格式的医学影像中不正常的数据，比如全黑的数据剔除掉
'''


def filter_normal(input_dir, output_dir):
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


if __name__ == '__main__':
    input_dir = r"/media/spgou/ZYJ/Nii_Dataset_RAI_Registered_Skulled_4mod"
    output_dir = r"/media/spgou/ZYJ/Nii_Dataset_RAI_Registered_Skulled_4mod_Normal"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    filter_normal(input_dir, output_dir)
