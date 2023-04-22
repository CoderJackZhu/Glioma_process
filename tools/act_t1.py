"""
本代码用于对nii.gz格式的医学影像进行处理，对T1、T2、T1+C、T2FLAIR四种影像进行处理，把T1的掩膜用于其他三个模态
"""

import os
import shutil
import pandas as pd
from tqdm import tqdm
import numpy as np
import nibabel as nib




