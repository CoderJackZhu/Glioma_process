import os
import shutil
import pandas as pd
from tqdm import tqdm
import nibabel as nib

def rename2net(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        modalities = os.listdir(patient_dir)
        for modality in tqdm(modalities):
            modality_file = os.path.join(patient_dir, modality)
            med_image = nib.load(modality_file)
            try:
                med_image = med_image.get_fdata()
                if med_image.shape != (240, 240, 155):
                    print('Warning: modality shape error! modality shape is: {}'.format(med_image.shape))
                    continue
            except Exception as e:
                print('Warning: modality info error! modality info is: {}'.format(e))

            if len(modality.split('.')[0].split('_')) == 3:
                patient_id = modality.split('.')[0].split('_')[0]
                patient_date = modality.split('.')[0].split('_')[2]
                modality_type = modality.split('.')[0].split('_')[1]
                if modality_type == 'T1':
                    modality_id = '0000'
                elif modality_type == 'T1+C':
                    modality_id = '0001'
                elif modality_type == 'T2':
                    modality_id = '0002'
                elif modality_type == 'T2FLAIR':
                    modality_id = '0003'
                else:
                    # 警告
                    print('Warning: modality type error! modality type is: {}'.format(modality_type))
                    continue
                new_modality_name = patient_id + '_' + patient_date + '_' + modality_id + '.nii.gz'
                new_modality_file = os.path.join(output_dir, new_modality_name)
                shutil.copy(modality_file, new_modality_file)
            else:
                continue


if __name__ == '__main__':
    input_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_Skulled_4mod_Normal"
    output_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_Skulled_4mod_Normal_rename"
    rename2net(input_dir, output_dir)
