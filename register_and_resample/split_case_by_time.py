import os
from tqdm import tqdm
import shutil

if __name__ == '__main__':
    data_dir = r".\RAI_xiangya_Dataset"
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
