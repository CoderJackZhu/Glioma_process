# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :utils.py
# @Time         :2023/5/10 17:12
# @Author       :Jack Zhu
import multiprocessing
import os
import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os
import shutil
import pandas as pd
from tqdm import tqdm
import random
from sklearn.model_selection import train_test_split
import SimpleITK as sitk

join = os.path.join


def check_info(patient_path):
    """
    确认nii.gz文件中含有病人的多少信息
    """
    # info = []
    for file in os.listdir(patient_path):
        if file.endswith(".nii"):
            file_path = os.path.join(patient_path, file)
            img = nib.load(file_path)
            meta_data = img.header
            for key in meta_data:
                print(key, meta_data[key])


def select4mod(input_dir, output_dir):
    print('Step3: select 4 modality full data')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        modalities = [modality for modality in os.listdir(patient_dir) if modality.endswith('.nii.gz')]
        modalities = list(set([modality.split('.')[0].split('_')[-1] for modality in modalities]))
        if len(modalities) == 4:
            if not os.path.exists(os.path.join(output_dir, patient)):
                os.mkdir(os.path.join(output_dir, patient))
            for modality in os.listdir(patient_dir):
                modality_file = os.path.join(patient_dir, modality)
                shutil.copy(modality_file, os.path.join(output_dir, patient, modality))


# if __name__ == '__main__':
#     input_dir = r"/media/spgou/ZYJ/Nii_Dataset_RAI_Registered"
#     output_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_4mod"
#     if not os.path.exists(output_dir):
#         os.mkdir(output_dir)
#     select4mod(input_dir, output_dir)


def rename2net(input_dir, output_dir):
    """
    将nii.gz文件重命名为nnUNet需要的格式
    """
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        modalities = os.listdir(patient_dir)
        for modality in tqdm(modalities):
            modality_file = os.path.join(patient_dir, modality)
            # med_image = nib.load(modality_file)
            # try:
            #     med_image = med_image.get_fdata()
            #     if med_image.shape != (240, 240, 155):
            #         print('Warning: modality shape error! modality shape is: {}'.format(med_image.shape))
            #         continue
            # except Exception as e:
            #     print('Warning: modality info error! modality info is: {}'.format(e))

            if len(modality.split('.')[0].split('_')) == 3 or modality.split('.')[0].split('_')[-1] == 't1mask':
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
                if os.path.exists(new_modality_file):
                    continue
                shutil.copy(modality_file, new_modality_file)
            else:
                continue


# if __name__ == '__main__':
#     input_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_4mod_skulled"
#     output_dir = r"/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered_4mod_skulled_rename"
#     rename2net(input_dir, output_dir)


def mkdirs(path):
    """
    创建文件夹,如果是列表则创建多个文件夹，
     如果是多级文件夹则创建多级文件夹，考虑父文件夹不存在的情况
    :param path: 文件夹路径
    :return:
    """
    if isinstance(path, list):
        for sub_path in path:
            mkdirs(sub_path)
    else:
        if not os.path.exists(path):
            os.makedirs(path)


def filter_normal(input_dir, output_dir):
    """
    本代码用于把nii.gz格式的医学影像中不正常的数据，比如全黑的数据剔除掉
    """
    average = []
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        if not os.path.exists(os.path.join(output_dir, patient)):
            os.mkdir(os.path.join(output_dir, patient))
        for modality in os.listdir(patient_dir):
            modality_file = os.path.join(patient_dir, modality)
            # 读取nii.gz文件
            data = nib.load(modality_file)
            # 获取nii.gz文件的数据
            try:
                data = data.get_fdata()
            except:
                continue
            # 计算每个像素的平均值
            mean = np.mean(data)
            average.append(mean)
    average = np.array(average)
    # 计算平均值的标准差
    std = np.std(average)
    # 计算平均值的均值
    mean = np.mean(average)
    # 计算平均值的上下界
    upper = mean + 3 * std
    lower = mean - 3 * std
    print('mean:', mean)
    print('std:', std)
    print('upper:', upper)
    print('lower:', lower)

    # 把不正常的数据剔除掉
    # 绘制直方图
    plt.hist(average, bins=100)
    plt.show()
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        if not os.path.exists(os.path.join(output_dir, patient)):
            os.mkdir(os.path.join(output_dir, patient))
        for modality in os.listdir(patient_dir):
            modality_file = os.path.join(patient_dir, modality)
            data = nib.load(modality_file)
            try:
                data = data.get_fdata()
                if data.shape != (240, 240, 155):
                    continue
            except Exception as e:
                continue
            mean = np.mean(data)
            if lower < mean < upper:
                shutil.copy(modality_file, os.path.join(output_dir, patient, modality))


def split_case_by_time(data_dir=r".\RAI_xiangya_Dataset"):
    case_dir_list = [os.path.join(data_dir, case) for case in os.listdir(data_dir)]

    for case_dir in tqdm(case_dir_list):

        nifty_path_list = [os.path.join(case_dir, nifty) for nifty in os.listdir(case_dir)]
        nifty_split_by_time = {}
        for nifty_path in nifty_path_list:
            time = nifty_path.split("_")[-1].replace(".nii.gz", '')
            if time not in nifty_split_by_time.keys():
                nifty_split_by_time[time] = []
            nifty_split_by_time[time].append(nifty_path)

        target_case_dir_list = [case_dir + "_" + time for time in nifty_split_by_time]
        for target_case_dir in target_case_dir_list:
            os.mkdir(target_case_dir)

        for time, nifty_path_list in nifty_split_by_time.items():
            target_case_dir = case_dir + "_" + time
            for nifty_path in nifty_path_list:
                target_nifty_path = os.path.join(target_case_dir, nifty_path.split(os.sep)[-1])
                shutil.copy(nifty_path, target_nifty_path)

        shutil.rmtree(case_dir)


def check_if_operation(patient_id, check_date):
    operation_info = pd.read_csv('result_file/12321321.csv')
    for i in range(len(operation_info)):
        id = operation_info.iloc[i, 0].zfill(10)
        operation_data = operation_info.iloc[i, 1]
        if id == patient_id:
            if type(operation_data) == float:
                return False
            operation_data = str(operation_data).replace('-', '').split(' ')[0]
            if int(check_date) < int(operation_data):
                return True
            else:
                return False
    return False


def check_empty_dir(mod_dir):
    """
    检查空文件夹并删除
    Args:
        mod_dir:

    Returns:

    """
    for file in os.listdir(mod_dir):
        file_path = os.path.join(mod_dir, file)
        files = os.listdir(file_path)
        if len(files) == 0:
            print(file_path)
            shutil.rmtree(file_path)


def visualize_result(patient_dir, pic_dir):
    """
    对于每个病人的每个模态的影像随机取三张切片并进行可视化
    Args:
        patient_dir:
        pic_dir:
    Returns:

    """
    if not os.path.exists(pic_dir):
        os.mkdir(pic_dir)
    patients = os.listdir(patient_dir)
    for patient in tqdm(patients):
        patient_path = os.path.join(patient_dir, patient)
        for modality in os.listdir(patient_path):
            modality_path = os.path.join(patient_path, modality)
            modality_data = nib.load(modality_path).get_fdata()
            for i in range(4):
                slice = random.randint(0, modality_data.shape[2] - 1)
                slice_data = modality_data[:, :, slice]
                plt.imshow(slice_data, cmap='gray')
                plt.savefig(os.path.join(pic_dir, patient + '_' + modality + '_' + str(slice) + '.png'))
                plt.close()


def transfer_net_format(input_dir, output_dir):
    """
    把病人的数据的文件名转换成nnUNet网络可以分割的格式
    Args:
        input_dir:
        output_dir:

    Returns:

    """
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        for modality in os.listdir(patient_dir):
            modality_file = os.path.join(patient_dir, modality)
            mode = modality.split('.')[0].split('_')[-1]
            if mode == 'T1':
                file = '0000.nii.gz'
            elif mode == 'T1+C':
                file = '0001.nii.gz'
            elif mode == 'T2':
                file = '0002.nii.gz'
            elif mode == 'T2FLAIR':
                file = '0003.nii.gz'
            else:
                continue
            file_name = '_'.join(modality.split('.')[0].split('_')[:-1]) + '_' + file
            shutil.copy(modality_file, os.path.join(output_dir, file_name))


def modality_rename(input_dir, output_dir):
    """
    把病人的数据的文件名模态的名称进行修改
    Args:
        input_dir:
        output_dir:

    Returns:

    """
    mkdirs(output_dir)
    for patient in tqdm(os.listdir(input_dir)):
        patient_dir = os.path.join(input_dir, patient)
        out_patient_dir = os.path.join(output_dir, patient)
        mkdirs(out_patient_dir)
        for modality in os.listdir(patient_dir):
            modality_file = os.path.join(patient_dir, modality)
            mode = modality.split('.')[0].split('_')[-1]
            if mode == 'T1':
                file = 't1.nii.gz'
            elif mode == 'T1+C':
                file = 't1Gd.nii.gz'
            elif mode == 'T2':
                file = 't2.nii.gz'
            elif mode == 'T2FLAIR':
                file = 'flair.nii.gz'
            else:
                continue
            file_name = '_'.join(modality.split('.')[0].split('_')[:-1]) + '_' + file
            shutil.copy(modality_file, os.path.join(out_patient_dir, file_name))


def split_train_test(input_dir, output_dir):
    """
    把数据集分成训练集和验证集
    Args:
        input_dir:/media/spgou/DATA/ZYJ/Dataset/captk_before_data_rename
        output_dir:/media/spgou/DATA/ZYJ/Dataset/RadiogenomicsProjects/GliomasSubtypes/originalData/XiangyaHospital
    """
    mkdirs(output_dir)
    train_dir = os.path.join(output_dir, 'XiangyaHospital_train')
    test_dir = os.path.join(output_dir, 'XiangyaHospital_test')
    train_dir_image = os.path.join(train_dir, 'Images')
    train_dir_seg = os.path.join(train_dir, 'segmentation')
    test_dir_image = os.path.join(test_dir, 'Images')
    test_dir_seg = os.path.join(test_dir, 'segmentation')
    mkdirs([train_dir, test_dir, train_dir_image, train_dir_seg, test_dir_image, test_dir_seg])

    patients = os.listdir(input_dir)
    train_patients, test_patients = train_test_split(patients, test_size=0.2, random_state=42)
    for patient in tqdm(train_patients):
        patient_dir = os.path.join(input_dir, patient)
        shutil.copytree(patient_dir, os.path.join(train_dir_image, patient))
    for patient in tqdm(test_patients):
        patient_dir = os.path.join(input_dir, patient)
        shutil.copytree(patient_dir, os.path.join(test_dir_image, patient))


def get_anonymized_id(patient_id):
    """
    给出病人的id，通过表格获取匿名化的id
    Args:
        patient_id:
    """
    df = pd.read_excel('../reference/Preprocess/anonymous_table.xlsx')
    for i in range(df.shape[0]):
        if df.iloc[i, 0] == patient_id:
            return df.iloc[i, 1]
    return None


def fuse_infov3():
    results = pd.read_excel('../result_file/fused_result_v2.xlsx')
    # 加匿名化的id到第一列
    results.insert(0, 'anonymous_id', None)
    for i in range(results.shape[0]):
        results.iloc[i, 0] = get_anonymized_id(results.iloc[i, 9])
    results.to_excel('../result_file/fused_result_v3.xlsx', index=False)


def fuse_infov4():
    results = pd.read_excel('../result_file/fused_result_v3.xlsx')
    # 把病人信息加到v3的结果中
    add_info = pd.read_excel('../reference/已补充-缺少病理数据的病人ID.xlsx')
    for i in range(add_info.shape[0]):
        for j in range(results.shape[0]):
            patient_id = str(add_info.iloc[i, 0]).zfill(10)
            if patient_id == results.iloc[j, 9]:
                results.iloc[j, 3] = add_info.iloc[i, 2]
                results.iloc[j, 4] = add_info.iloc[i, 1]
                continue
    results.to_excel('../result_file/fused_result_v4.xlsx', index=False)


def check_empty_data(input_dir):
    """
    检查数据集中是否有空的数据
    Args:
        input_dir:

    Returns:

    """
    patients = os.listdir(input_dir)
    for patient in tqdm(patients):
        patient_dir = os.path.join(input_dir, patient)
        for modality in os.listdir(patient_dir):
            modality_path = os.path.join(patient_dir, modality)
            modality_data = nib.load(modality_path).get_fdata()
            if np.sum(modality_data) == 0:
                print(patient, modality)


def mv_seg_file(
        img_dir='/media/spgou/DATA/ZYJ/Dataset/RadiogenomicsProjects/GliomasSubtypes/originalData/XiangyaHospital/XiangyaHospital_test/Images',
        seg_dir='/media/spgou/DATA/ZYJ/Dataset/captk_before_data_net_seg',
        out_dir='/media/spgou/DATA/ZYJ/Dataset/RadiogenomicsProjects/GliomasSubtypes/originalData/XiangyaHospital/XiangyaHospital_test/segmentation'):
    """
    把图片文件夹对应的seg文件夹中的文件移动到新的文件夹中
    Args:
        img_dir:
        seg_dir:
        out_dir:

    Returns:

    """
    mkdirs(out_dir)
    patients = os.listdir(img_dir)
    for patient in tqdm(patients):
        seg_file = os.path.join(seg_dir, patient + '.nii.gz')
        out_file = os.path.join(out_dir, patient + '.nii.gz')
        shutil.copy(seg_file, out_file)


def subfiles(folder: str, join: bool = True, prefix: str = None, suffix: str = None, sort: bool = True):
    if join:
        l = os.path.join
    else:
        l = lambda x, y: y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isfile(os.path.join(folder, i))
           and (prefix is None or i.startswith(prefix))
           and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res


def check_labels(seg_file="/media/spgou/DATA/ZYJ/Dataset/captk_before_data_net_seg/Gliomas_00005_20181117.nii.gz"):
    """
    检查标签文件是否有问题
    Args:
        seg_file:

    Returns:

    """
    seg_data = nib.load(seg_file).get_fdata()
    print(np.unique(seg_data))


def convert_labels_back_to_BraTS(seg: np.ndarray):
    new_seg = np.zeros_like(seg)
    new_seg[seg == 1] = 2
    new_seg[seg == 3] = 4
    new_seg[seg == 2] = 1
    return new_seg


def load_convert_labels_back_to_BraTS(filename, input_folder, output_folder):
    a = sitk.ReadImage(join(input_folder, filename))
    b = sitk.GetArrayFromImage(a)
    c = convert_labels_back_to_BraTS(b)
    d = sitk.GetImageFromArray(c)
    d.CopyInformation(a)
    sitk.WriteImage(d, join(output_folder, filename))


def convert_folder_with_preds_back_to_BraTS_labeling_convention(input_folder: str, output_folder: str,
                                                                num_processes: int = 12):
    """
    reads all prediction files (nifti) in the input folder, converts the labels back to BraTS convention and saves the
    """
    mkdirs(output_folder)
    nii = subfiles(input_folder, suffix='.nii.gz', join=False)
    with multiprocessing.get_context("spawn").Pool(num_processes) as p:
        p.starmap(load_convert_labels_back_to_BraTS, zip(nii, [input_folder] * len(nii), [output_folder] * len(nii)))


def merge_diagnose_info():
    """
    合并两次的诊断信息表格，并把附加其他病人的诊断信息附加到主诊断信息表格后面
    """
    main_diagnose = pd.read_csv('../result_file/12321321.csv', header=0)
    added_diagnose = pd.read_excel('../reference/已补充-缺少病理数据的病人ID.xlsx', header=0)
    length = len(main_diagnose)
    for i in range(len(added_diagnose)):
        # 合并两次的诊断信息表格，并把附加其他病人的诊断信息附加到主诊断信息表格后面
        main_diagnose.loc[length + i] = [added_diagnose.iloc[i, 0], None, added_diagnose.iloc[i, 2],
                                         added_diagnose.iloc[i, 1], None, None]
        # main_diagnose.iloc[length + i, 0] = added_diagnose.iloc[i, 0]
        # main_diagnose.iloc[length + i, 2] = added_diagnose.iloc[i, 2]
        # main_diagnose.iloc[length + i, 3] = added_diagnose.iloc[i, 1]
    main_diagnose.to_excel('../result_file/diagnose_info.xlsx', index=False)


def get_and_merge_patient_who_grade(excel_path='../result_file/features_XiangyaHospital_train.xlsx', save_path='../result_file/features_XiangyaHospital_train_who.xlsx'):
    """
    给训练和测试的特征列表加一列who等级，等级的数据从诊断信息的表格中提取，然后匿名化并对应到特征列表中
    """
    features = pd.read_excel(excel_path, header=0)
    diagnose_info = pd.read_excel('../result_file/PathologicalData_DropNull_manualCorrected_analyzed.xlsx', header=0)
    # 给特征列表加一列who等级
    features['WHO_grade'] = None
    df = pd.read_excel('../reference/Preprocess/anonymous_table.xlsx')

    for i in tqdm(range(len(features))):
        anonymized_id = features.iloc[i, 0]
        for j in range(len(diagnose_info)):
            patient_id = diagnose_info.loc[j, 'PatientID']
            for k in range(df.shape[0]):
                if df.iloc[k, 0] == patient_id.zfill(10):
                    anony_id = df.iloc[k, 1]
                    break
            if anony_id == '_'.join(anonymized_id.split('_')[:2]):
                print(anonymized_id, patient_id, diagnose_info.loc[j, 'WHO_grade'])
                features.iloc[i, -1] = diagnose_info.loc[j, 'WHO_grade']
                break
    features.to_excel(save_path, index=False)

def merge_pathological_data_anonymized():
    """给提取到的病理信息加一列匿名化的病人ID
    """
    pathological_data = pd.read_excel('../result_file/PathologicalData_DropNull_manualCorrected.xlsx', header=0)
    df = pd.read_excel('../reference/Preprocess/anonymous_table.xlsx')
    # 匿名化后的ID插入到第一列
    pathological_data.insert(0, 'PatientID_anonymized', None)
    for i in tqdm(range(len(pathological_data))):
        patient_id = pathological_data.loc[i, 'PatientID']
        for j in range(df.shape[0]):
            if df.iloc[j, 0] == patient_id.zfill(10):
                pathological_data.iloc[i, 0] = df.iloc[j, 1]
                break
    pathological_data.to_excel('../result_file/PathologicalData_DropNull_manualCorrected_anonymized.xlsx', index=False)

if __name__ == "__main__":
    # check_empty('D:\\ZYJ\\Dataset\\Nii_Dataset_RAI_Registered_4mod_skulled_resolve_before')
    # visualize_result('D:\\ZYJ\\Dataset\\Nii_Dataset_RAI_Registered_4mod_skulled_resolve_before',
    #                  'D:\\ZYJ\\Dataset\\Nii_Dataset_RAI_Registered_4mod_skulled_resolve_before_pic')
    # transfer_net_format('/media/spgou/DATA/ZYJ/Dataset/captk_nii_4mod_after_operation_anonymize_processed_4mod', '/media/spgou/DATA/ZYJ/Dataset/captk_after_data_net_format')
    # modality_rename('/media/spgou/DATA/ZYJ/Dataset/captk_before_data', '/media/spgou/DATA/ZYJ/Dataset/captk_before_data_rename')
    # split_train_test('/media/spgou/DATA/ZYJ/Dataset/captk_before_data_rename', '/media/spgou/DATA/ZYJ/Dataset/RadiogenomicsProjects/GliomasSubtypes/originalData/XiangyaHospital')
    # check_empty('/media/spgou/DATA/ZYJ/Dataset/RadiogenomicsProjects/GliomasSubtypes/originalData/XiangyaHospital/XiangyaHospital_test/Images')
    # mv_seg_file()
    # check_labels()
    # convert_folder_with_preds_back_to_BraTS_labeling_convention(
    #     '/media/spgou/DATA/ZYJ/Dataset/RadiogenomicsProjects/GliomasSubtypes/originalData/XiangyaHospital/XiangyaHospital_test/segmentation',
    #     '/media/spgou/DATA/ZYJ/Dataset/RadiogenomicsProjects/GliomasSubtypes/originalData/XiangyaHospital/XiangyaHospital_test/seg')
    # fuse_infov4()
    # merge_diagnose_info()
    get_and_merge_patient_who_grade()
