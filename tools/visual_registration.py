"""
本代码用于对可视化对nii.gz格式的医学影像配准前后的效果进行可视化
"""
import os
import shutil
import pandas as pd
from tqdm import tqdm
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from skimage import measure
import SimpleITK as sitk
import gc


def show_registered_images(fixed_image_path, moving_image_path, registered_image_path, save_visualize_basic_path):
    """
    Visualize the registration results.
    """
    fixed_image = nib.load(fixed_image_path).get_fdata()
    moving_image = nib.load(moving_image_path).get_fdata()
    registered_image = nib.load(registered_image_path).get_fdata()

    # read images
    fixedImage = sitk.ReadImage(fixed_image_path)
    movingImage = sitk.ReadImage(moving_image_path)
    registeredImage = sitk.ReadImage(registered_image_path)

    # convert the pixel value to uint8
    fixedNDA = sitk.GetArrayViewFromImage(fixedImage)
    movingNDA = sitk.GetArrayViewFromImage(movingImage)
    registeredNDA = sitk.GetArrayViewFromImage(registeredImage)

    fixedImageUint8 = sitk.Cast(
        sitk.IntensityWindowing(fixedImage, windowMinimum=float(fixedNDA.min()), windowMaximum=float(fixedNDA.max()),
                                outputMinimum=0.0, outputMaximum=255.0), sitk.sitkUInt8)
    movingImageUint8 = sitk.Cast(
        sitk.IntensityWindowing(movingImage, windowMinimum=float(movingNDA.min()), windowMaximum=float(movingNDA.max()),
                                outputMinimum=0.0, outputMaximum=255.0), sitk.sitkUInt8)
    registeredImageUint8 = sitk.Cast(sitk.IntensityWindowing(registeredImage, windowMinimum=float(registeredNDA.min()),
                                                             windowMaximum=float(registeredNDA.max()),
                                                             outputMinimum=0.0, outputMaximum=255.0), sitk.sitkUInt8)

    # show the images
    number_of_slices = min(fixed_image.shape[2], moving_image.shape[2])
    for index in range(0, number_of_slices):
        rgbImage_afterReg = sitk.Cast(sitk.Compose(fixedImageUint8[:, :, index],
                                                   fixedImageUint8[:, :, index] * 0.5 + registeredImageUint8[:, :,
                                                                                        index] * 0.5,
                                                   registeredImageUint8[:, :, index]), sitk.sitkVectorUInt8)

        plt.figure(figsize=(20, 5))
        sub_fig = plt.subplot(1, 4, 1)
        sub_fig.set_title("Fixed Image", fontsize=20)
        plt.axis('off')
        plt.imshow(fixed_image[:, :, index].T)

        sub_fig = plt.subplot(1, 4, 2)
        sub_fig.set_title("Moving Image", fontsize=20)
        plt.axis('off')
        plt.imshow(moving_image[:, :, index].T)

        sub_fig = plt.subplot(1, 4, 3)
        sub_fig.set_title("Registered Image", fontsize=20)
        plt.axis('off')
        plt.imshow(registered_image[:, :, index].T)

        sub_fig = plt.subplot(1, 4, 4)
        sub_fig.set_title("Overlap after registration", fontsize=20)
        plt.axis('off')
        plt.imshow(sitk.GetArrayViewFromImage(rgbImage_afterReg))

        plt.subplots_adjust(left=0.03, bottom=0.03, right=0.97, top=0.9, wspace=0.03, hspace=0)

        basename = os.path.basename(moving_image_path)
        save_path = os.path.join(save_visualize_basic_path, basename.split('.')[0] + '_' + str(index) + '.png')

        plt.savefig(save_path)

        # plt.show()

        # Clear the current axes.
        plt.cla()
        # Clear the current figure.
        plt.clf()
        # Closes all the figure windows.
        plt.close('all')
        gc.collect()


def visual_registration(fixed_image_path, moving_patient_dir, registered_patient_dir, save_dir):
    """
    Visualize the registration results.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    modalities_list = os.listdir(moving_patient_dir)
    for modality in modalities_list:
        modality_file = os.path.join(moving_patient_dir, modality)
        modality_registered_file = os.path.join(registered_patient_dir, modality)
        modality_save_pic_dir = os.path.join(save_dir, modality.split('.')[0])
        if not os.path.exists(modality_save_pic_dir):
            os.makedirs(modality_save_pic_dir)
        # if os.path.exists(modality_file) and os.path.exists(modality_registered_file):
        show_registered_images(fixed_image_path, modality_file, modality_registered_file, modality_save_pic_dir)


def batch_visual_registration(moving_patient_dir, registered_patient_dir, save_pic_dir):
    """
    Visualize the registration results.
    :param fixed_image_path:
    :param moving_patient_dir:
    :param registered_patient_dir:
    :param save_pic_dir:
    :return:
    """

    atlas_template = "../reference/sri24_rai/atlastImage.nii.gz"
    erly_template = "../reference/sri24_rai/erly_unstrip.nii"
    late_template = "../reference/sri24_rai/late_unstrip.nii"
    spgr_template = "../reference/sri24_rai/spgr_unstrip.nii"

    if not os.path.exists(save_pic_dir):
        os.makedirs(save_pic_dir)
    patient_list = os.listdir(moving_patient_dir)
    for patient in tqdm(patient_list):
        patient_dir = os.path.join(moving_patient_dir, patient)
        patient_registered_dir = os.path.join(registered_patient_dir, patient)
        patient_save_dir = os.path.join(save_pic_dir, patient)
        if not os.path.exists(patient_save_dir):
            os.makedirs(patient_save_dir)

        modalities_list = os.listdir(patient_dir)
        for modality in modalities_list:
            modality_file = os.path.join(patient_dir, modality)
            for modality_registered in os.listdir(patient_registered_dir):
                if modality.split('.')[0].split('_')[1] == modality_registered.split('.')[0].split('_')[1]:
                    modality_registered_file = os.path.join(patient_registered_dir, modality_registered)
                    modality_save_pic_dir = os.path.join(patient_save_dir, modality_registered.split('.')[0])
                    if not os.path.exists(modality_save_pic_dir):
                        os.makedirs(modality_save_pic_dir)
                    # if os.path.exists(modality_file) and os.path.exists(modality_registered_file):
                    if modality_registered.split('.')[0].split('_')[-1] == 'atlas':
                        fixed_image_path = atlas_template
                    elif modality_registered.split('.')[0].split('_')[-1] == 'erly':
                        fixed_image_path = erly_template
                    elif modality_registered.split('.')[0].split('_')[-1] == 'late':
                        fixed_image_path = late_template
                    elif modality_registered.split('.')[0].split('_')[-1] == 'spgr':
                        fixed_image_path = spgr_template
                    else:
                        raise ValueError("The template is not exist!")
                    # print('fixed_image_path: ', fixed_image_path)
                    # print('moving_file: ', modality_file)
                    # print('registered_file: ', modality_registered_file)
                    show_registered_images(fixed_image_path, modality_file, modality_registered_file,
                                           modality_save_pic_dir)

    # for patient in tqdm(patient_list):
    #     patient_dir = os.path.join(moving_patient_dir, patient)
    #     patient_registered_dir = os.path.join(registrated_patient_dir, patient)
    #     patient_save_dir = os.path.join(save_dir, patient)
    #     if not os.path.exists(patient_save_dir):
    #         os.makedirs(patient_save_dir)
    #
    #     modalities_list = os.listdir(patient_dir)
    #     for modality in modalities_list:
    #         modality_file = os.path.join(patient_dir, modality)
    #         modality_registered_file = os.path.join(patient_registered_dir, modality)
    #         print(modality_file)
    #         print(modality_registered_file)
    #         modality_save_pic_dir = os.path.join(patient_save_dir, modality.split('.')[0])
    #         if not os.path.exists(modality_save_pic_dir):
    #             os.makedirs(modality_save_pic_dir)
    #         if os.path.exists(modality_file) and os.path.exists(modality_registered_file):
    #             show_registered_images(fixed_image_path, modality_file, modality_registered_file, modality_save_pic_dir)
    #         else:
    #             print('some file does not exist')
    #             print('{} or {}'.format(modality_file, modality_registered_file))
    #             with open('../result_file/visualize_registration_error.txt', 'a') as f:
    #                 f.write('{} or {}'.format(modality_file, modality_registered_file))
    #                 f.write('\n')


if __name__ == '__main__':
    # # moving_patient_dir = '/media/spgou/ZYJ/Nii_Dataset_RAI/0002139521_20190212'
    # # registered_patient_dir = '/media/spgou/ZYJ/Nii_Dataset_RAI_Registered/0002139521_20190212'
    # # save_dir = '/media/spgou/DATA/ZYJ/Dataset/register_visual'
    # # 原模板
    # # fixed_image_path = '../reference/sri24_rai/atlastImage.nii.gz'
    # fixed_image_path = '../reference/sri24_rai/spgr_unstrip.nii'
    # # fixed_image_path = '../reference/sri24_rai/late_unstrip.nii'
    # # fixed_image_path = '../reference/sri24_rai/spgr_unstrip.nii'
    # moving_image_path = '../test_data/0000798625_20220409/0000798625_T2FLAIR_20220409.nii.gz'
    # # registered_image_path = '../test_data/0000000695_T1_20200105.nii.gz'
    # registered_image_path = '../test_data/0000798625_20220409_registered/0000798625_T2FLAIR_20220409_spgr.nii.gz'
    # save_visualize_basic_path = '../test_data/' + registered_image_path.split(os.sep)[-1].split('.')[0] + '_visual'
    # if not os.path.exists(save_visualize_basic_path):
    #     os.makedirs(save_visualize_basic_path)
    #
    # # visual_registration(fixed_image_path, moving_patient_dir, registered_patient_dir, save_dir)
    # show_registered_images(fixed_image_path, moving_image_path, registered_image_path, save_visualize_basic_path)
    moving_patient_dir = '/media/spgou/ZYJ/Dataset/Nii_Dataset_RAI'
    registered_patient_dir = '/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered'
    batch_visual_registration(moving_patient_dir, registered_patient_dir, save_pic_dir='/media/spgou/DATA/ZYJ/Dataset/visualize_registration')
