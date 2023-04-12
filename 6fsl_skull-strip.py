import os
import shutil
import pandas as pd
from tqdm import tqdm
import numpy as np
import SimpleITK as sitk
import xlrd
def select_after_operation():
    operation_info = xlrd.open_workbook(r"./reference/12321321.xls")
    print(operation_info[0])


def skull_strip(registrated_dir, skull_stripped_dir):
    pass






if __name__ == "__main__":
    registrated_dir = r"./Registrated"
    skull_stripped_dir = r"./skull_stripped"
    if not os.path.exists(skull_stripped_dir):
        os.mkdir(skull_stripped_dir)
    select_after_operation()
    skull_strip(registrated_dir, skull_stripped_dir)
