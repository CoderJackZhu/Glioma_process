# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :one_mod_skull.py
# @Time         :2023/8/1 21:04
# @Author       :Jack Zhu
"""
本代码用于给童诺老师的单模态T1序列的数据进行去头骨处理，这里采用了两种方法，分别是CaPTK和FSL
"""

import os
import shutil
from multiprocessing import Pool

import pandas as pd
from tqdm import tqdm
import numpy as np
import SimpleITK as sitk
import subprocess
import nibabel as nib


def t1_skull_stripping(nii_dir, dest_dir):
    """
    对MRI影像的t1序列进行skull stripping
    """
    print('Step: CaPTK preprocess')
    cmd_list = []
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    tools = 'C:/CaPTk_Full/1.9.0/bin/DeepMedic.exe'
    tools = os.path.normpath(tools)
    patient_dirs = os.listdir(nii_dir)
    for patient_dir in tqdm(patient_dirs):
        out_patient_dir = os.path.join(dest_dir, patient_dir)
        if not os.path.exists(out_patient_dir):
            os.mkdir(out_patient_dir)
        cmd = (f"{tools} -i {os.path.join(nii_dir, patient_dir)} -md C:/CaPTk_Full/1.9.0/data/deepMedic/saved_models/skullStripping_modalityAgnostic -o {out_patient_dir}")
        cmd_list.append(cmd)
    # 多进程处理
    pool = Pool(processes=8)
    pool.map(os.system, cmd_list)
    pool.close()
    pool.join()


# fsl 安装
# 使用本地安装包
# 解压缩到要安装的文件夹。推荐和我一样解压缩到/usr/local目录下
# 有可能会出现权限不足的问题无法解压缩，可以在usr目录中打开终端，输入
# sudo chmod -R 777 local
# 输入密码后，打开权限
# 配置环境变量.bashrc
# export FSLDIR=/usr/local/fsl
# export PATH=$PATH:$FSLDIR/bin
# source $FSLDIR/etc/fslconf/fsl.sh


def fsl_skull_strip(nii_dir, dest_dir):
    """
    对MRI影像的t1序列进行skull stripping
    """
    print('Step: FSL preprocess')
    cmd_list = []
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    patient_dirs = os.listdir(nii_dir)
    for patient_dir in tqdm(patient_dirs):
        out_patient_dir = os.path.join(dest_dir, patient_dir)
        if not os.path.exists(out_patient_dir):
            os.mkdir(out_patient_dir)
        cmd = (f"/usr/local/fsl/bin/bet2 {os.path.join(nii_dir, patient_dir)} {out_patient_dir} -o -m -f 0.3")
        os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ'  # 设置环境变量
        cmd_list.append(cmd)
    # 多进程处理
    pool = Pool(processes=8)
    pool.map(os.system, cmd_list)
    pool.close()
    pool.join()


if __name__ == "__main__":
    nii_dir = r'strip_dir'
    dest_dir = r'F:\\Code\\Medical\\Glioma_process\\out_strip_dir'
    t1_skull_stripping(nii_dir, dest_dir)
