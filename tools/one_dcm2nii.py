import os
import pydicom
from multiprocessing import Pool
import dicom2nifti
import pandas as pd

def dcm2nii(dcm_image_folder, save_nii_image_path, patient_id, nii_modality):
    if os.path.exists(save_nii_image_path):
        return
    print("patient_id={}, modality={}, dcm_image_folder={}, save_nii_image_path={}".format(patient_id, nii_modality,
                                                                                           dcm_image_folder,
                                                                                           save_nii_image_path))
    # 1.conversion of the DICOM files to the NIFTI file format;
    dicom2nifti.settings.enable_validate_slice_increment()
    dicom2nifti.settings.enable_validate_orthogonal()
    try:
        dicom2nifti.dicom_series_to_nifti(dcm_image_folder, save_nii_image_path,
                                          reorient_nifti=True)  # LAS oriented

    except Exception as error:
        print("Caution!!! patient_id={}, modality={}, error: {}.".format(patient_id, nii_modality, error))
        file = r'./result_file/dcm_to_nii_error_list.txt'
        with open(file, 'a+') as f:
            f.write("patient_id={}, modality={}, error: {}. \n".format(patient_id, nii_modality, error))

        dicom2nifti.settings.disable_validate_slice_increment()
        dicom2nifti.settings.disable_validate_orthogonal()
        dicom2nifti.dicom_series_to_nifti(dcm_image_folder, save_nii_image_path,
                                          reorient_nifti=True)  # LAS oriented


def load_error_info(error_file):
    error_info = []
    with open(error_file, 'r') as f:
        for line in f.readlines():
            error_info.append(line)
    return error_info


def load_patient_info(patient_info_file):
    patient_info = pd.read_excel(patient_info_file)
    return patient_info


def try_transfer():
    error_file = r'../result_file/dcm_to_nii_error_list.txt'
    error_info = load_error_info(error_file)
    patient_info_file = r'../result_file/selected_result_v1.xlsx'
    patient_info = load_patient_info(patient_info_file)
    save_nii_dir = '/media/spgou/DATA/ZYJ/Dataset/New_Nii_file'
    if not os.path.exists(save_nii_dir):
        os.mkdir(save_nii_dir)
    for error in error_info:
        try:
            patient_id = error.split(',')[0].split('=')[1]
            print(patient_id)
            modality = error.split(',')[1].split('=')[1]
            error_reason = error.split(',')[2].split(':')[1]
            out_patient_dir = os.path.join(save_nii_dir, patient_id)
            if not os.path.exists(out_patient_dir):
                os.mkdir(out_patient_dir)
            patient_info_row = patient_info[patient_info['PatientID'] == patient_id]
            for index in range(len(patient_info_row)):
                dcm_image_file = patient_info_row.iloc[index, 2]
                # print(dcm_image_file)
                dir_path = os.path.dirname(dcm_image_file)
                dir_path = os.path.normpath(dir_path)
                print(dir_path)
        except Exception as e:
            print(e)
            continue





if __name__ == '__main__':
    try_transfer()