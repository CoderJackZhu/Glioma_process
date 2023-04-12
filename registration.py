import ants
import os
from tqdm import tqdm

'''
Register images and save the results.
'''


def register_images(fixed_image_path, moving_image_path, save_registered_path):
    fixed_img = ants.image_read(fixed_image_path)
    moving_img = ants.image_read(moving_image_path)

    registered_results = ants.registration(fixed=fixed_img, moving=moving_img, type_of_transform='Rigid')
    registered_moving_image = registered_results['warpedmovout']
    transform_from_move_to_fix = registered_results['fwdtransforms']
    transform_from_fix_to_move = registered_results['invtransforms']

    ants.image_write(registered_moving_image, save_registered_path)


if __name__ == '__main__':
    data_dir = "./RAI_xiangya_Dataset"
    target_data_dir = "Registration_Dataset"

    if not os.path.exists(target_data_dir):
        os.mkdir(target_data_dir)

    case_dir_list = [os.path.join(data_dir, case) for case in os.listdir(data_dir)]

    for case_dir in tqdm(case_dir_list):
        nifty_path_list = [os.path.join(case_dir, nifty) for nifty in os.listdir(case_dir)]
        splited_case_dir = case_dir.split(os.sep)
        splited_case_dir[1] = target_data_dir
        target_case_dir = os.sep.join(splited_case_dir)
        if not os.path.exists(target_case_dir):
            os.mkdir(target_case_dir)
        for nifty_path in nifty_path_list:
            target_case_dir = case_dir
            for nifty_path in nifty_path_list:
                splited_nifty_path = nifty_path.split(os.sep)
                splited_nifty_path[1] = target_data_dir
                target_nifty_path = os.sep.join(splited_nifty_path)
                register_images("./sri24/atlastImage.nii.gz", nifty_path, target_nifty_path)


