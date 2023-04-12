# -*- coding:utf-8 -*-
# @PROJECT_NAME :Glioma_process
# @FileName     :rm_space.py
# @Time         :2023/4/12 20:06
# @Author       :Jack Zhu
import os
import shutil


if __name__ == "__main__":
    origin_path = r'./some_Nii_Dataset_origin'
    target_path = r'./some_Nii_Dataset'
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    for case in os.listdir(origin_path):
        case_path = os.path.join(origin_path, case)
        target_case_path = os.path.join(target_path, case)
        if not os.path.exists(target_case_path):
            os.mkdir(target_case_path)
        for nifty in os.listdir(case_path):
            nifty_path = os.path.join(case_path, nifty)
            nifty_replace = nifty.replace(' ', '')
            target_nifty_path = os.path.join(target_case_path, nifty_replace)
            shutil.copy(nifty_path, target_nifty_path)
