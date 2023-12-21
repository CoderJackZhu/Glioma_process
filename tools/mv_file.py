import os
import random
import shutil
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def mv_file(source_dir, img_dir, seg_dir):
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    if not os.path.exists(seg_dir):
        os.makedirs(seg_dir)
    # 获取文件夹中的文件列表
    patients = os.listdir(source_dir)

    # 遍历文件列表
    for patient in tqdm(patients, desc="Processing Images"):
        # 获取文件名
        patient_dir = os.path.join(source_dir, patient)
        # 获取文件名
        out_patient_dir = os.path.join(img_dir, patient)
        if not os.path.exists(out_patient_dir):
            os.makedirs(out_patient_dir)
        modality_files = os.listdir(patient_dir)
        patient_id = "_".join(patient.split('_')[:-1])
        for modality_file in modality_files:
            modality = modality_file.split('.')[0].split(patient_id)[-1].split('_')[1:]
            # print(modality)
            if modality[0] == 'T1' and len(modality) == 1:
                shutil.copy(os.path.join(patient_dir, modality_file), os.path.join(out_patient_dir, modality_file))
            elif modality[0] == 'T2' and len(modality) == 1:
                shutil.copy(os.path.join(patient_dir, modality_file), os.path.join(out_patient_dir, modality_file))
            elif modality[0] == 'T1c' and len(modality) == 1:
                shutil.copy(os.path.join(patient_dir, modality_file), os.path.join(out_patient_dir, modality_file))
            elif modality[0] == 'FLAIR' and len(modality) == 1:
                shutil.copy(os.path.join(patient_dir, modality_file), os.path.join(out_patient_dir, modality_file))
            elif modality[0] == 'tumor' and modality[1] == 'segmentation':
                shutil.copy(os.path.join(patient_dir, modality_file), os.path.join(seg_dir, modality_file))


if __name__ == '__main__':
    mv_file('/media/spgou/DATA/ZYJ/Dataset/5.UCSF-PDGM/UCSF-PDGM-v3-20230111',
            '/media/spgou/DATA/ZYJ/Dataset/5.UCSF-PDGM/UCSF-PDGM-v3-20230111_img',
            '/media/spgou/DATA/ZYJ/Dataset/5.UCSF-PDGM/UCSF-PDGM-v3-20230111_seg')
