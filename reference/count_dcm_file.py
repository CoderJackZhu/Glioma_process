# -*- coding:utf-8 -*-
# @PROJECT_NAME :Dcm_process
# @FileName     :count_dcm_file.py
# @Time         :2023/3/20 21:47
# @Author       :Jack Zhu
import os
import pandas as pd
from multiprocessing import Pool
from DcmData import DcmData

if __name__ == "__main__":
    with open('failed.txt', 'rb') as f:
        images_paths = f.readlines()
        images_paths = [path.decode('gbk').strip() for path in images_paths]
        for path in images_paths:
            print(path)
            try:
                dcm_data = DcmData(path)
                data = dcm_data.Infos
                print(data)
            except:
                print(f'----------failed to read file:{path}-----------------')

