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

def registration_visualization(input_dir, registrated_dir, output_dir):
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)


