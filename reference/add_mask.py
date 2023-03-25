# -*- coding:utf-8 -*-
# @PROJECT_NAME :Dcm_process
# @FileName     :add_mask.py
# @Time         :2023/3/23 18:53
# @Author       :Jack Zhu


if __name__ == "__main__":
    import SimpleITK as sitk
    import numpy as np
    import matplotlib.pyplot as plt

    """
    这里有两种情况，第一种为原图和label都是由SimpleITK所读取
    """
    img_path = "E:\Dataset\MedicalDataset\BRaTS_2021_Task1_Dataset\BraTS2021_00621\BraTS2021_00621_t1.nii.gz"
    ground_truth_path = "E:\Dataset\MedicalDataset\BRaTS_2021_Task1_Dataset\BraTS2021_00621\BraTS2021_00621_seg.nii.gz"
    img = sitk.ReadImage(img_path)
    # SimpleITK需要将图像转为uint8
    ImgUint8 = sitk.Cast(sitk.RescaleIntensity(img, ), sitk.sitkUInt8)
    overlay = sitk.LabelOverlay(ImgUint8, seg)
    nda = sitk.GetArrayViewFromImage(overlay)
    plt.imshow(nda[n, :, :])  # n为要读取的切片

