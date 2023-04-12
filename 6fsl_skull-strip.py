import os
import shutil
import pandas as pd
from tqdm import tqdm
import numpy as np
import SimpleITK as sitk

def sef


def skull_strip(registrated_dir, skull_stripped_dir):







if __name__ == "__main__":
    registrated_dir = r".\Registrated"
    skull_stripped_dir = r".\skull_stripped"
    if not os.path.exists(skull_stripped_dir):
        os.mkdir(skull_stripped_dir)
    skull_strip(registrated_dir, skull_stripped_dir)