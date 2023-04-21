# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :info_fuse.py
# @Time         :2023/4/21 18:24
# @Author       :Jack Zhu

import os
import shutil
import numpy as np
import pandas as pd


def get_info(excelfile):
    excel_file = pd.read_excel(excelfile)
    # csv_file = pd.read_csv(r'../result_file/12321321.csv')

if __name__ == "__main__":
    get_info(r'../result_file/selected_result.xlsx')
