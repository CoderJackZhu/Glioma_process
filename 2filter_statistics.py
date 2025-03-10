# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :2filter_statistics.py
# @Time         :2023/3/21 11:02
# @Author       :Jack Zhu
import os
import pandas as pd
from DcmData import DcmData
from tqdm import tqdm

def analyze_MRISequence(SeriesDescription):
    if 't1' in SeriesDescription:
        # if 'flair' in SeriesDescription:
        #     if '+c' in SeriesDescription:
        #         return 'T1 FLAIR+C'
        #     else:
        #         return 'T1 FLAIR'
        if '+c' in SeriesDescription:
            return 'T1+C'
        else:
            return 'T1'
    elif 't2' in SeriesDescription:
        if 'flair' in SeriesDescription or 'darkfluid' in SeriesDescription or 'dark fluid' in SeriesDescription or 'dark-fluid' in SeriesDescription or 'dark_fluid' in SeriesDescription:
            if '+c' in SeriesDescription:
                return 'T2FLAIR+C'
            else:
                return 'T2FLAIR'
        elif '+c' in SeriesDescription:
            return 'T2+C'
        else:
            return 'T2'
    elif 'bravo' in SeriesDescription or 'mpeage' in SeriesDescription:
        return 'T1'


def analyze_ImagePlane(SeriesDescription):
    if 'ax' in SeriesDescription or 'oax' in SeriesDescription or 'tra' in SeriesDescription:
        return 'Axial'
    elif 'cor' in SeriesDescription:
        return 'Coronal'
    elif 'sag' in SeriesDescription:
        return 'Sagittal'
    else:
        return 'Others'


def select_sequence_from_excel():
    # 读取excel文件
    data = pd.read_excel('./result_file/basic_dataset_v1.xlsx')
    for i in range(len(data)):
        if type(data.loc[i, 'SeriesDescription']) != str:
            continue
        data.loc[i, 'SeriesDescription'] = data.loc[i, 'SeriesDescription'].lower()
        data.loc[i, 'MRISequence'] = analyze_MRISequence(data.loc[i, 'SeriesDescription'])
        data.loc[i, 'ImagePlane'] = analyze_ImagePlane(data.loc[i, 'SeriesDescription'])
    # 保存为新的excel文件
    data.to_excel('selected_result_v1.xlsx', index=False)


def find_patient_amount():
    data = pd.read_excel('./result_file/selected_result_v1.xlsx')
    patient_amount = data['PatientID'].value_counts()
    # print(patient_amount)
    # Name: PatientID, Length: 3485, dtype: int64
    patient_sequence_dict = {}
    patient_plane_dict = {}
    for idx in patient_amount.index:
        patient_sequence_dict[idx] = []
        patient_plane_dict[idx] = []
    for i in range(len(data)):
        if type(data.loc[i, 'MRISequence']) != str:
            data.loc[i, 'MRISequence'] = str(data.loc[i, 'MRISequence'])
            if 'nan' in data.loc[i, 'MRISequence']:
                continue
        # if type(data.loc[i, 'ImagePlane']) != str:
        #     continue
        patient_sequence_dict[data.loc[i, 'PatientID']].append(data.loc[i, 'MRISequence'])
        patient_plane_dict[data.loc[i, 'PatientID']].append(data.loc[i, 'ImagePlane'])
    # print(patient_sequence_dict)
    # print(patient_plane_dict)
    T1_C_count, T1_count, T2_FLAIR_C_count, T2_FLAIR_count, T2_C_count, T2_count = 0, 0, 0, 0, 0, 0
    t1c_t1_t2flairc_t2flair_t2_count = 0
    t1c_t1_t2flair_t2_count = 0
    t1_t2flair_t2_count = 0
    t1c_t2flair_t2_count = 0
    t1c_t1_t2flair_t2_patients = []
    for idx in patient_amount.index:
        patient_sequence_dict[idx] = list(set(patient_sequence_dict[idx]))
        patient_plane_dict[idx] = list(set(patient_plane_dict[idx]))
        # for sequence in patient_sequence_dict[idx]:
        #     if 'T1 FLAIR+C' == sequence:
        #         T1_FLAIR_C_count += 1
        #     elif 'T1 FLAIR' == sequence:
        #         T1_FLAIR_count += 1
        #     elif 'T1+C' == sequence:
        #         T1_C_count += 1
        #     elif 'T1' == sequence:
        #         T1_count += 1
        #     elif 'T2FLAIR+C' == sequence:
        #         T2_FLAIR_C_count += 1
        #     elif 'T2FLAIR' == sequence:
        #         T2_FLAIR_count += 1
        #     elif 'T2+C' == sequence:
        #         T2_C_count += 1
        #     elif 'T2' == sequence:
        #         T2_count += 1

        # if 'T1 FLAIR+C' in patient_sequence_dict[idx]:
        #     T1_FLAIR_C_count += 1
        # if 'T1 FLAIR' in patient_sequence_dict[idx]:
        #     T1_FLAIR_count += 1
        if 'T1+C' in patient_sequence_dict[idx]:
            T1_C_count += 1
        if 'T1' in patient_sequence_dict[idx]:
            T1_count += 1
        if 'T2FLAIR+C' in patient_sequence_dict[idx]:
            T2_FLAIR_C_count += 1
        if 'T2FLAIR' in patient_sequence_dict[idx]:
            T2_FLAIR_count += 1
        if 'T2+C' in patient_sequence_dict[idx]:
            T2_C_count += 1
        if 'T2' in patient_sequence_dict[idx]:
            T2_count += 1

        if 'T1+C' in patient_sequence_dict[idx] and 'T1' in patient_sequence_dict[idx] and 'T2FLAIR+C' in \
                patient_sequence_dict[idx] and 'T2FLAIR' in patient_sequence_dict[idx] and 'T2' in \
                patient_sequence_dict[idx]:
            t1c_t1_t2flairc_t2flair_t2_count += 1
        if 'T1' in patient_sequence_dict[idx] and 'T1+C' in patient_sequence_dict[idx] and \
                'T2FLAIR' in patient_sequence_dict[idx] and 'T2' in patient_sequence_dict[idx]:
            t1c_t1_t2flair_t2_count += 1
            t1c_t1_t2flair_t2_patients.append(idx)
        if 'T1' in patient_sequence_dict[idx] and 'T2FLAIR' in patient_sequence_dict[idx] and \
                'T2' in patient_sequence_dict[idx]:
            t1_t2flair_t2_count += 1
        if 'T1+C' in patient_sequence_dict[idx] and 'T2FLAIR' in patient_sequence_dict[idx] and \
                'T2' in patient_sequence_dict[idx]:
            t1c_t2flair_t2_count += 1

            # attribute_combination = tuple(sorted(patient_sequence_dict[idx]))
            # print(attribute_combination)
            # attribute_combination_count[attribute_combination] = attribute_combination_count.get(attribute_combination, 0) + 1
    # for key, value in attribute_combination_count.items():
    #     print(key, value)
    # print('attribute_combination_count: ', attribute_combination_count)

    # print('T1 FLAIR+C: ', T1_FLAIR_C_count)
    # print('T1 FLAIR: ', T1_FLAIR_count)
    print('T1+C: ', T1_C_count)
    print('T1: ', T1_count)
    print('T2FLAIR+C: ', T2_FLAIR_C_count)
    print('T2FLAIR: ', T2_FLAIR_count)
    print('T2+C: ', T2_C_count)
    print('T2: ', T2_count)
    print('t1c_t1_t2flairc_t2flair_t2_count: ', t1c_t1_t2flairc_t2flair_t2_count)
    print('t1_t2flair_t2_count: ', t1_t2flair_t2_count)
    print('t1c_t2flair_t2_count: ', t1c_t2flair_t2_count)
    print('t1c_t1_t2flair_t2_count: ', t1c_t1_t2flair_t2_count)

    with open('result_file/patient_count_information.txt', 'w') as f:
        f.write(('Patient amount: ' + str(len(patient_amount))) + '\n')
        # f.write('T1 FLAIR+C: ' + str(T1_FLAIR_C_count) + '\n')
        # f.write('T1 FLAIR: ' + str(T1_FLAIR_count) + '\n')
        f.write('T1+C: ' + str(T1_C_count) + '\n')
        f.write('T1: ' + str(T1_count) + '\n')
        f.write('T2FLAIR+C: ' + str(T2_FLAIR_C_count) + '\n')
        f.write('T2FLAIR: ' + str(T2_FLAIR_count) + '\n')
        f.write('T2+C: ' + str(T2_C_count) + '\n')
        f.write('T2: ' + str(T2_count) + '\n')
        f.write('T1, T1+C, T2FLAIR+C, T2FLAIR, T2 all_count: ' + str(t1c_t1_t2flairc_t2flair_t2_count) + '\n')
        f.write('T1, T1+C, T2FLAIR, T2 all_count: ' + str(t1c_t1_t2flair_t2_count) + '\n')
        f.write('T1, T2FLAIR, T2 all_count: ' + str(t1_t2flair_t2_count) + '\n')
        f.write('T1+C, T2FLAIR, T2 all_count: ' + str(t1c_t2flair_t2_count) + '\n')
        # for key, value in attribute_combination_count.items():
        #     f.write(str(key) + ': ' + str(value) + '\n')

    # 去除重复病人
    t1c_t1_t2flair_t2_patients = list(set(t1c_t1_t2flair_t2_patients))
    with open('result_file/t1c_t1_t2flair_t2_PATIENT_ID.txt', 'w') as f:
        for patient in t1c_t1_t2flair_t2_patients:
            f.write(patient + '\n')
    # print(patient_sequence_dict)

# 按日期和病人ID划分，得到7433个文件夹，对其中每天每个病人的文件夹查找，找到4种模态全的文件夹，记录下来，共有2993个文件夹
def count4modality(dir_path):
    files = os.listdir(dir_path)
    num_count = 0
    for file in tqdm(files):
        file_path = os.path.join(dir_path, file)
        nii_files = os.listdir(file_path)
        nii_list = []
        for nii_file in nii_files:
            nii_file_path = os.path.join(file_path, nii_file)
            modality = nii_file.split('_')[1]
            if modality not in nii_list:
                nii_list.append(modality)
        if len(nii_list) == 4:
            num_count += 1
            with open('result_file/4modality.txt', 'a') as f:
                f.write(file + '\n')

if __name__ == "__main__":
    # select_sequence_from_excel()
    find_patient_amount()
    # dir_path = 'G:/Nii_Dataset'
    # count4modality(dir_path)
