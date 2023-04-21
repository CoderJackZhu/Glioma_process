import os
import shutil
import pandas as pd
from tqdm import tqdm
import numpy as np
import SimpleITK as sitk
import subprocess


def check_if_operation(patient_id, check_date):
    operation_info = pd.read_csv('result_file/12321321.csv')
    for i in tqdm(range(len(operation_info))):
        id = operation_info.iloc[i, 0].zfill(10)
        operation_data = operation_info.iloc[i, 1]
        if id == patient_id:
            if type(operation_data) == float:
                return False
            operation_data = str(operation_data).replace('-', '').split(' ')[0]
            print(check_date, operation_data)
            if int(check_date) < int(operation_data):
                return True
            else:
                return False
    return False


def skull_strip(registrated_dir, skull_stripped_dir):
    # first = "exec bash;"
    # aa = "#!/bin/bash; "
    # a = "source /home/spgou/.bashrc; source /etc/bash.bashrc;"
    # b = "export PATH=$PATH:$FSLDIR/bin;"
    # c = "source ${FSLDIR}/etc/fslconf/fsl.csh;"
    for patient in tqdm(os.listdir(registrated_dir)):
        patient_id = patient.split('_')[0]
        patient_date = patient.split('_')[1]
        # print(patient_id)
        if_operation = check_if_operation(patient_id, patient_date)
        if not if_operation:
            continue
        print(patient)
        patient_dir = os.path.join(registrated_dir, patient)
        if not os.path.exists(os.path.join(skull_stripped_dir, patient)):
            os.mkdir(os.path.join(skull_stripped_dir, patient))
        # # 先处理T1，再用T1的模板处理其他几个模态
        # for modality in os.listdir(patient_dir):
        #     modality_file = os.path.join(patient_dir, modality)
        #     skull_stripped_file = os.path.join(skull_stripped_dir, patient, modality)
        #     if modality.split('.')[0].split('_')[1] == 'T1':
        #         cmd = f"bet2 {modality_file} {skull_stripped_file} -o -m"
        #         os.system(cmd)
        #         break
        for modality in os.listdir(patient_dir):
            modality = modality.replace(' ', '')
            modality_file = os.path.join(patient_dir, modality)
            skull_stripped_file = os.path.join(skull_stripped_dir, patient, modality)
            if os.path.exists(skull_stripped_file):
                continue
            cmd =  f"/home/spgou/fsl/bin/bet2 {modality_file} {skull_stripped_file} -o -m"
            print(cmd)
            os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ'  # 设置环境变量
            subprocess.call(cmd, shell=True)
            # os.system(cmd)
            # subprocess.call(cmd, shell=True)
            # env = os.environ.copy()
            # env['PATH'] = env['PATH'] + ':/home/spgou/fsl/bin'
            # p = subprocess.Popen(cmd, shell=True, env=env)
            # p.wait()


def select_before_operation():
    nii_path = "/media/Z"
    pass


if __name__ == "__main__":
    # registrated_dir = r"/media/spgou/DATA/ZYJ/Dcm_process/Registration_Dataset"
    # skull_stripped_dir = r"/media/spgou/DATA/ZYJ/Dcm_process/skull_stripped_out"
    registrated_dir = r"/media/spgou/ZYJ//Nii_Dataset_RAI_Registered"
    skull_stripped_dir = r"/media/spgou/ZYJ//Nii_Dataset_RAI_Registered_Skull_Stripped"
    if not os.path.exists(skull_stripped_dir):
        os.mkdir(skull_stripped_dir)
    skull_strip(registrated_dir, skull_stripped_dir)
