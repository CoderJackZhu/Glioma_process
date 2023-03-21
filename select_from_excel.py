# -*- coding:utf-8 -*-
# @PROJECT_NAME :Dcm_process
# @FileName     :select_from_excel.py
# @Time         :2023/3/21 11:02
# @Author       :Jack Zhu
import os
import pandas as pd
from DcmData import DcmData
from multi_process_process import get_data_paths, try_get_data, multi_process_save


def analyze_MRISequence(SeriesDescription):
    if 't1' in SeriesDescription:
        if 'flair' in SeriesDescription:
            if '+c' in SeriesDescription:
                return 'T1 FLAIR+C'
            else:
                return 'T1 FLAIR'
        elif '+c' in SeriesDescription:
            return 'T1+C'
        else:
            return 'T1'
    elif 't2' in SeriesDescription:
        if 'flair' in SeriesDescription:
            if '+c' in SeriesDescription:
                return 'T2 FLAIR+C'
            else:
                return 'T2 FLAIR'
        elif '+c' in SeriesDescription:
            return 'T2+C'
        else:
            return 'T2'

def analyze_ImagePlane(SeriesDescription):
    if 'ax' in SeriesDescription:
        return 'Axial'
    elif 'cor' in SeriesDescription:
        return 'Coronal'
    elif 'sag' in SeriesDescription:
        return 'Sagittal'
    else:
        return 'Others'


def select_from_excel():
    # 读取excel文件
    data = pd.read_excel('all_dataset_result.xlsx')
    for i in range(len(data)):
        if type(data.loc[i, 'SeriesDescription']) != str:
            continue
        data.loc[i, 'SeriesDescription'] = data.loc[i, 'SeriesDescription'].lower()
        data.loc[i, 'MRISequence'] = analyze_MRISequence(data.loc[i, 'SeriesDescription'])
        data.loc[i, 'ImagePlane'] = analyze_ImagePlane(data.loc[i, 'SeriesDescription'])
    # 保存为新的excel文件
    data.to_excel('selected_result.xlsx', index=False)


if __name__ == "__main__":
    select_from_excel()
