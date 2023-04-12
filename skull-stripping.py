# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :skull-stripping.py
# @Time         :2023/4/5 21:51
# @Author       :Jack Zhu
import os
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure, morphology, filters
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import cv2
import time
import sys
import shutil
import glob
import pandas as pd
import pydicom
import scipy.ndimage
import scipy.misc
import scipy.ndimage
import scipy.misc
import nibabel as nib

def thresh_based(img):
    import numpy as np
    import nibabel as nib
    from skimage import filters

    # 加载nii文件
    img = nib.load(img).get_fdata()

    # 计算阈值
    thresh = filters.threshold_otsu(img)

    # 应用阈值
    mask = img > thresh

    # 保存输出
    nib.save(nib.Nifti1Image(mask.astype(np.uint8), affine=None), 'output.nii.gz')

def edge_based(img):
    # 加载nii文件
    img = nib.load(img).get_fdata()

    # 计算边缘
    edges = filters.sobel(img)

    # 应用阈值
    thresh = filters.threshold_otsu(edges)
    mask = edges > thresh

    # 保存输出
    nib.save(nib.Nifti1Image(mask.astype(np.uint8), affine=None), 'output.nii.gz')

if __name__ == "__main__":
    edge_based('test.nii.gz')
