# -*- coding:utf-8 -*-
# @PROJECT_NAME :Dcm_process
# @FileName     :dcm2nii.py
# @Time         :2023/3/25 22:00
# @Author       :Jack Zhu
import os
import pydicom
import pandas as pd
from multiprocessing import Pool
import SimpleITK as sitk
# import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# 用python写一个函数把dcm格式的文件转成nii.gz格式的文件
# 1. 读取dcm文件
# 2. 保存为nii.gz文件


def dcm2nii_itk(dcms_path, nii_path):
    # 1.构建dicom序列文件阅读器，并执行（即将dicom序列文件“打包整合”）
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dcms_path)
    reader.SetFileNames(dicom_names)
    image2 = reader.Execute()
    # 2.将整合后的数据转为array，并获取dicom文件基本信息
    image_array = sitk.GetArrayFromImage(image2)  # z, y, x
    origin = image2.GetOrigin()  # x, y, z
    spacing = image2.GetSpacing()  # x, y, z
    direction = image2.GetDirection()  # x, y, z
    # 3.将array转为img，并保存为.nii.gz
    image3 = sitk.GetImageFromArray(image_array)
    image3.SetSpacing(spacing)
    image3.SetDirection(direction)
    image3.SetOrigin(origin)
    sitk.WriteImage(image3, nii_path)

def dcm2nii_nib(dcm_file_path, nii_file_path):
    ds = pydicom.dcmread(dcm_file_path)
    img = ds.pixel_array.astype(np.float32)
    img /= np.max(img)
    img *= 255
    img = img.astype(np.uint8)
    affine = np.diag([1, 1, 1, 1])
    nii = nib.Nifti1Image(img, affine)
    nib.save(nii, nii_file_path + '.nii.gz')

def main():
    info = pd.read_excel('selected_result.xlsx')
    count_list = []
    for i in tqdm(range(len(info))):
        file1_path = info.loc[i, 'ImagePath']
        dir_path = os.path.dirname(file1_path)
        file_count = len(os.listdir(dir_path))
        count_list.append(file_count)
    # 画出数量的立方图
    plt.hist(count_list)
    plt.show()


if __name__ == "__main__":
    main()
    # file = 'G:/DCM_Dataset/2021-12-17胶质瘤-约760例/DICOM10/PA0/ST0/SE2/IM0'
    # gz_file_path = './test'
    # dir_path = os.path.dirname(file)
    # print(dir_path)
    # dcm2niigz(dir_path, gz_file_path)
