import os
import shutil
import pandas as pd
from tqdm import tqdm
import numpy as np
import SimpleITK as sitk
import subprocess
import nibabel as nib


def check_if_operation(patient_id, check_date):
    operation_info = pd.read_csv('result_file/12321321.csv')
    for i in range(len(operation_info)):
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


def t1_skull_strip(registrated_dir, skull_stripped_dir):
    print('Stage 1: T1 skull strip...(now for all modalities)')
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
        patient_dir = os.path.join(registrated_dir, patient)
        if not os.path.exists(os.path.join(skull_stripped_dir, patient)):
            os.mkdir(os.path.join(skull_stripped_dir, patient))
        # 先处理T1，再用T1的模板处理其他几个模态
        for modality in os.listdir(patient_dir):
            modality_file = os.path.join(patient_dir, modality)
            skull_stripped_file = os.path.join(skull_stripped_dir, patient, modality)
            if os.path.exists(skull_stripped_file):
                continue
            # if modality.split('.')[0].split('_')[1] == 'T1':
            cmd = f"/home/spgou/fsl/bin/bet2 {modality_file} {skull_stripped_file} -o -m"
            os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ'  # 设置环境变量
            os.system(cmd)
            break

        # for modality in os.listdir(patient_dir):
        #     modality = modality.replace(' ', '')
        #     modality_file = os.path.join(patient_dir, modality)
        #     skull_stripped_file = os.path.join(skull_stripped_dir, patient, modality)
        #     if os.path.exists(skull_stripped_file):
        #         continue
        #     cmd = f"/home/spgou/fsl/bin/bet2 {modality_file} {skull_stripped_file} -o -m"
        #     print(cmd)
        #     subprocess.call(cmd, shell=True)


def act_t1_mask(input_dir, output_dir):
    print('Stage 2: Act T1 mask to other modalities...')
    for patient in tqdm(os.listdir(output_dir)):
        patient_dir = os.path.join(output_dir, patient)
        for modality in os.listdir(patient_dir):
            modality_file = os.path.join(patient_dir, modality)
            # # 把T1的所有文件复制到结果文件夹中
            # if modality.split('.')[0].split('_')[1] == 'T1':
            #     shutil.copy(modality_file, os.path.join(out_patient_dir, modality))
            # 把T1的掩膜用于其他三个模态
            if modality.split('.')[0].split('_')[1] == 'T1' and modality.split('.')[0].split('_')[-1] == 'mask':
                # 获取T1的掩膜
                t1_mask = nib.load(modality_file)
                t1_mask = t1_mask.get_fdata()
                t1_mask = np.array(t1_mask, dtype=np.uint8)

        if t1_mask is None:
            # 警告：没有找到T1的掩膜
            print('Warning: No T1 mask found in patient {}'.format(patient))
            continue
        input_patient_dir = os.path.join(input_dir, patient)
        # 获取其他三个模态的文件名
        more_modalities = [modality for modality in os.listdir(input_patient_dir) \
                           if modality.split('.')[0].split('_')[1] != 'T1']
        for modality in more_modalities:
            more_modality_file = os.path.join(input_patient_dir, modality)
            data = nib.load(more_modality_file)
            data = data.get_fdata()
            # 把T1的掩膜用于其他三个模态
            data = data * t1_mask
            # 保存
            data = nib.Nifti1Image(data, affine=np.eye(4))
            nib.save(data, os.path.join(patient_dir, modality.split('.')[0] + '_t1mask.nii.gz'))


if __name__ == "__main__":
    # registrated_dir = r"/media/spgou/DATA/ZYJ/Dcm_process/Registration_Dataset"
    # skull_stripped_dir = r"/media/spgou/DATA/ZYJ/Dcm_process/skull_stripped_out"
    registrated_dir = r"/media/spgou/ZYJ//Nii_Dataset_RAI_Registered"
    skull_stripped_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_Skulled"
    if not os.path.exists(skull_stripped_dir):
        os.mkdir(skull_stripped_dir)
    t1_skull_strip(registrated_dir, skull_stripped_dir)
    act_t1_mask(registrated_dir, skull_stripped_dir)
