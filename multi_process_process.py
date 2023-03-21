# -*- coding:utf-8 -*-
# @PROJECT_NAME :Dcm_process
# @FileName     :multi_process_process.py
# @Time         :2023/3/18 21:38
# @Author       :Jack Zhu

import pydicom
import os
import pandas as pd
from multiprocessing import Pool
from DcmData import DcmData


def get_data_paths():
    dataset_path = r'G:\DCM_Dataset'
    images_paths = []
    for paths, dirnames, filenames in os.walk(dataset_path):
        for dir in dirnames:
            dir_path = os.path.join(paths, dir)
            files = os.listdir(dir_path)
            try:
                img_path = os.path.join(dir_path, files[0])
            except:
                continue
            if os.path.isdir(img_path):
                continue
            print(img_path)
            images_paths.append(img_path)
    images_paths.sort()
    # 将路径保存为txt文件
    with open('image_path.txt', 'wb') as f:
        for path in images_paths:
            f.write(path.encode('utf-8'))
            f.write('\n'.encode('utf-8'))
    return images_paths


def try_get_data(img_path):
    try:
        print(img_path)
        dcm_data = DcmData(img_path)
        data = dcm_data.Infos
        # dcm_data.show_all_attributes()
        info_data = pd.DataFrame.from_dict(data, orient='index').T
        # info_data = pd.DataFrame.from_dict(dcm_data, orient='index').T
        return info_data

    except:
        print(f'----------failed to read file:{img_path}-----------------')
        f = "failed.txt"
        with open(f, "a") as file:
            file.write(img_path.encode('utf-8') + '\n'.encode('utf-8'))


def multi_process_save():
    # 如果已经存在路径文件，则直接读取
    if os.path.exists('image_path.txt'):
        with open('image_path.txt', 'rb') as f:
            images_paths = f.readlines()
            images_paths = [path.decode('utf-8').strip() for path in images_paths]
    else:
        images_paths = get_data_paths()
    for path in images_paths:
        print(path)
    # 多进程读取数据
    with Pool(4) as p:
        all_data = p.map(try_get_data, images_paths)
    all_data = pd.concat(all_data, axis=0)
    all_data.to_excel('dataset_result.xlsx')


if __name__ == "__main__":
    multi_process_save()
