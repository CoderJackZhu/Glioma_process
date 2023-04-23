# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :3dcm2nii.py
# @Time         :2023/3/25 22:00
# @Author       :Jack Zhu
import os
import pydicom
import pandas as pd
from multiprocessing import Pool
# import SimpleITK as sitk
# import nibabel as nib
# import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
# import gc
# import ants
import dicom2nifti


# 用python写一个函数把dcm格式的文件转成nii.gz格式的文件
# 1. 读取dcm文件
# 2. 保存为nii.gz文件


# def dcm2nii_itk(dcms_path, nii_path):
#     if os.path.exists(nii_path):
#         return
#     # try:
#         # 1.构建dicom序列文件阅读器，并执行（即将dicom序列文件“打包整合”）
#     reader = sitk.ImageSeriesReader()
#     dicom_names = reader.GetGDCMSeriesFileNames(dcms_path)
#     reader.SetFileNames(dicom_names)
#     image2 = reader.Execute()
#     # 2.将整合后的数据转为array，并获取dicom文件基本信息
#     image_array = sitk.GetArrayFromImage(image2)
#     image_array = image_array.astype(np.float32)
#     image_array /= np.max(image_array)
#     image_array *= 255
#     image_array = image_array.astype(np.uint8)
#     # 3.将array转为nii.gz文件
#     image = sitk.GetImageFromArray(image_array)
#     sitk.WriteImage(image, nii_path)
#     # except:
#     #     print(f'----------failed to read file:{dcms_path}-----------------')
#     #     f = "failed_save_nii.txt"
#     #     with open(f, "a") as file:
#     #         file.write(dcms_path.encode('utf-8') + '\n'.encode('utf-8'))
#
#
#     # reader = sitk.ImageSeriesReader()
#     # seriesIDs = reader.GetGDCMSeriesIDs(dcms_path)
#     # N = len(seriesIDs)
#     # lens = np.zeros([N])
#     # for i in range(N):
#     #     dicom_names = reader.GetGDCMSeriesFileNames(dcms_path, seriesIDs[i])
#     #     lens[i] = len(dicom_names)
#     # N_MAX = np.argmax(lens)
#     # dicom_names = reader.GetGDCMSeriesFileNames(dcms_path, seriesIDs[N_MAX])
#     # reader.SetFileNames(dicom_names)
#     # image = reader.Execute()
#     # sitk.WriteImage(image, nii_path)


# def dcm2nii_nib(dcm_folder_path, nii_file_path):
#     if os.path.exists(nii_file_path):
#         return
#     print(dcm_folder_path)
#     # 获取DICOM文件列表
#     dcm_files = [os.path.join(dcm_folder_path, f) for f in os.listdir(dcm_folder_path)]
#
#     # 读取DICOM序列的第一个文件，获取图像尺寸和像素间距
#     first_dcm = pydicom.read_file(dcm_files[0])
#     x, y = first_dcm.Rows, first_dcm.Columns
#     slice_thickness = first_dcm.SliceThickness
#     pixel_spacing = first_dcm.PixelSpacing
#
#     # 创建一个3D Numpy数组存储所有的DICOM像素数据
#     img_array = np.zeros((x, y, len(dcm_files)), dtype=np.int16)
#
#     # 逐个读取DICOM文件，将像素数据存储到Numpy数组中
#     for i, f in enumerate(dcm_files):
#         dcm = pydicom.read_file(f)
#         img_array[:, :, i] = dcm.pixel_array
#
#     # 创建一个Nifti1Image对象并将像素数据填充到其中
#     nii_image = nib.Nifti1Image(img_array, np.eye(4))
#
#     # 设置Nifti1Image对象的像素尺寸和像素间距属性
#     nii_image.header.set_zooms((pixel_spacing[0], pixel_spacing[1], slice_thickness))
#
#     # 将Nifti1Image对象保存为NIfTI文件
#     nib.save(nii_image, nii_file_path)

def dcm2nii(dcm_image_folder, save_nii_image_path, patient_id, nii_modality):
    if os.path.exists(save_nii_image_path):
        return
    print("patient_id={}, modality={}, dcm_image_folder={}, save_nii_image_path={}".format(patient_id, nii_modality,
                                                                                           dcm_image_folder,
                                                                                           save_nii_image_path))
    # 1.conversion of the DICOM files to the NIFTI file format;
    dicom2nifti.settings.enable_validate_slice_increment()
    dicom2nifti.settings.enable_validate_orthogonal()
    try:
        dicom2nifti.dicom_series_to_nifti(dcm_image_folder, save_nii_image_path,
                                          reorient_nifti=True)  # LAS oriented

    except Exception as error:
        print("Caution!!! patient_id={}, modality={}, error: {}.".format(patient_id, nii_modality, error))
        file = r'./result_file/dcm_to_nii_error_list.txt'
        with open(file, 'a+') as f:
            f.write("patient_id={}, modality={}, error: {}. \n".format(patient_id, nii_modality, error))

        dicom2nifti.settings.disable_validate_slice_increment()
        dicom2nifti.settings.disable_validate_orthogonal()
        dicom2nifti.dicom_series_to_nifti(dcm_image_folder, save_nii_image_path,
                                          reorient_nifti=True)  # LAS oriented


def get_use_data():
    info = pd.read_excel('./result_file/selected_result_v1.xlsx')
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
        # basic_info['StudyTime'] = info.loc[i, 'StudyTime']
    # 保存数量的列表
    np.save('./result_file/use_dir_list.npy', dir_list)
    return dir_list
    #     count_list.append(file_count)
    # # 保存数量的列表
    # count_list = np.load('./result_file/count_list.npy')
    # # 画出数量的立方图
    # plt.hist(count_list, bins=100, range=(0, 60))
    # plt.show()


def if_use_data():
    if os.path.exists('./result_file/use_dir_list.npy'):
        dir_list = np.load('./result_file/use_dir_list.npy', allow_pickle=True)
        return dir_list
    else:
        dir_list = get_use_data()
        return dir_list


def multi_process(dir_list, dest_dir):
    # 并行处理
    pool = Pool(12)
    for i in tqdm(range(len(dir_list))):
        # print(dir_list[i])
        # 筛掉不用的模态
        modality = dir_list[i]['modility']
        if modality not in ['T1', 'T1+C', 'T2', 'T2 FLAIR']:
            continue
        dir_path = dir_list[i]['dir_path']
        dir_path = dir_path = os.path.normpath(dir_path)
        # print(dir_path)
        patient_id = str(dir_list[i]['patient_id'])
        patient_study_date = str(int(dir_list[i]['StudyDate']))
        patient_dir = os.path.join(dest_dir, patient_id + '_' + patient_study_date)
        if not os.path.exists(patient_dir):
            os.mkdir(patient_dir)

        # print(dir_path)
        nii_path = os.path.join(dest_dir, patient_dir,
                                patient_id + '_' + str(modality) + '_' + patient_study_date + '.nii.gz')
        pool.apply_async(dcm2nii, (dir_path, nii_path, patient_id, modality))
    pool.close()
    pool.join()

    # for i in tqdm(range(len(dir_list))):
    #     print(dir_list[i])
    #     dir_path = dir_list[i]['dir_path']
    #     patient_id = dir_list[i]['patient_id']
    #     patient_dir = os.path.join(dest_dir, str(patient_id))
    #     if not os.path.exists(patient_dir):
    #         os.mkdir(patient_dir)
    #     modality = dir_list[i]['modility']
    #     # print(dir_path)
    #     nii_path = os.path.join(dest_dir, patient_dir, str(patient_id) + '_' + str(modality) + '.nii.gz')


'''
Visualize the nii results.
'''


# def show_nii_images(nii_images_dict, save_visualize_basic_path):
#     load_nii_images = {}
#     for image_name, image_path in nii_images_dict.items():
#         load_nii_images[image_name] = nib.load(image_path).get_fdata()
#
#     # show the images
#     number_of_slices = list(load_nii_images.values())[0].shape[2]
#     for index in range(0, number_of_slices):
#
#         num_figures = len(load_nii_images)
#         plt.figure(figsize=(5 * num_figures, 5))
#         j = 0
#         for image_name, nii_image in load_nii_images.items():
#             j = j + 1
#             sub_fig = plt.subplot(1, num_figures, j)
#             sub_fig.set_title(image_name, fontsize=20)
#             plt.axis('off')
#             plt.imshow(nii_image[:, :, index].T)
#
#         plt.subplots_adjust(left=0.03, bottom=0.03, right=0.97, top=0.9, wspace=0.03, hspace=0)
#
#         basename = os.path.basename(image_path)
#         save_path = save_visualize_basic_path + '/' + basename[:-5] + '_' + str(index) + '.png'
#         plt.savefig(save_path)
#
#         plt.show()
#
#         # Clear the current axes.
#         plt.cla()
#         # Clear the current figure.
#         plt.clf()
#         # Closes all the figure windows.
#         plt.close('all')
#         gc.collect()

def main():
    dir_list = if_use_data()
    dest_dir = 'G:/Nii_Dataset'
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    # 并行处理
    multi_process(dir_list, dest_dir)


if __name__ == "__main__":
    main()
    # show_nii_images({'1':'./test.nii.gz'}, '.')
    # file = 'G:\\DCM_Dataset\\2021-12-17胶质瘤-约760例\\DICOM20\\PA0\\ST0\\SE0\\IM0'
    # gz_file_path = './test.nii.gz'
    # dir_path = os.path.dirname(file)
    # dir_path = 'G:\\DCM_Dataset\\新2022-05-18胶质母细胞瘤-约1500\\DICONDIT1\\PA7\\ST0\\SE3'
    # p = Pool(8)
    # p.apply_async(dcm2nii_itk, (dir_path, gz_file_path))
    # p.close()
    # p.join()
    # dcm2nii_itk(dir_path, gz_file_path)
    # dcm2nii(dir_path, gz_file_path, '1', '1')
