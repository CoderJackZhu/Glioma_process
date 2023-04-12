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
import gc
import os
import nibabel as nib
from deepbrain import Extractor



def extract_brain_mask(image_path, save_brain_mask_path, save_visualize_basic_path=None, show_results=False):
    '''
    Run brain Extraction by deepbrain package.
    See https://github.com/iitzco/deepbrain/blob/master/bin/deepbrain-extractor.
    '''

    print('\nBegin to extract the brain of {}.'.format(image_path))

    # read data
    image = nib.load(image_path)
    affine = image.affine
    image = image.get_fdata()

    # extract brain
    ext = Extractor()
    prob = ext.run(
        image)  # `prob` will be a 3d numpy image containing probability of being brain tissue for each of the voxels in `img`
    mask = prob > 0.5

    # Save mask as nifti
    brain_mask = (1 * mask).astype(np.uint8)
    brain_mask = nib.Nifti1Image(brain_mask, affine)
    nib.save(brain_mask, save_brain_mask_path)
    print('\n Finsh saving the mask to {}.'.format(save_brain_mask_path))

if __name__ == "__main__":
    extract_brain_mask('/media/spgou/ZYJ/Nii_Dataset/0000004868_20110712/0000004868_T2_20110712.nii.gz', 'masked.nii.gz')
