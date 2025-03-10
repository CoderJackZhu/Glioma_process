import ants
import os
from tqdm import tqdm
import nibabel as nib
# import multiprocessing
# import gc
import traceback
# multiprocessing.set_start_method('spawn')
# multiprocessing.Semaphore(1).release()
# gc.collect()
'''
Register images and save the results.
'''


def register_images(fixed_image_path, moving_image_path, save_registered_path):
    try:
        fixed_img = ants.image_read(fixed_image_path)
        moving_img = ants.image_read(moving_image_path)

    # # 转换为单通道图像
    # moving_img = ants.to_single_component_image(moving_img)
    #
    # fixed_img_resampled = ants.resample_image(fixed_img, (240, 240, 155), use_voxels=True)
    # moving_img_resampled = ants.resample_image(moving_img, (240, 240, 155), use_voxels=True)

        registered_results = ants.registration(fixed=fixed_img, moving=moving_img, type_of_transform='Rigid')
        registered_moving_image = registered_results['warpedmovout']
        transform_from_move_to_fix = registered_results['fwdtransforms']
        transform_from_fix_to_move = registered_results['invtransforms']

        ants.image_write(registered_moving_image, save_registered_path)

    except Exception as e:
        print(f"error happened in func register_images when dealing with {moving_image_path}")
        with open("./result_file/registration_error_log.txt", "a") as f:
            f.write(f"error happened in func register_images when dealing with {moving_image_path}\n")


if __name__ == '__main__':
    data_dir = "/media/spgou/ZYJ/Dataset/Nii_Dataset_RAI"
    target_data_dir = "/media/spgou/DATA/ZYJ/Dataset/Nii_Dataset_RAI_Registered"
    atlas_template = "reference/sri24_rai/atlastImage.nii.gz"
    erly_template = "reference/sri24_rai/erly_unstrip.nii"
    late_template = "reference/sri24_rai/late_unstrip.nii"
    spgr_template = "reference/sri24_rai/spgr_unstrip.nii"

    if not os.path.exists(target_data_dir):
        os.mkdir(target_data_dir)

    case_dir_list = [os.path.join(data_dir, case) for case in os.listdir(data_dir)]

    for case_dir in tqdm(case_dir_list):
        nifty_path_list = [os.path.join(case_dir, nifty) for nifty in os.listdir(case_dir)]
        # splited_case_dir = case_dir.split(os.sep)
        # splited_case_dir[1] = target_data_dir
        # target_case_dir = os.sep.join(splited_case_dir)
        target_case_dir = os.path.join(target_data_dir, case_dir.split(os.sep)[-1])
        if not os.path.exists(target_case_dir):
            os.mkdir(target_case_dir)

        for nifty_path in nifty_path_list:
            # target_case_dir = case_dir
            # for nifty_path in nifty_path_list:
            # splited_nifty_path = nifty_path.split(os.sep)
            # splited_nifty_path[1] = target_data_dir
            # target_nifty_path = os.sep.join(splited_nifty_path)
            modality = nifty_path.split(os.sep)[-1].split('.')[0].split('_')[1]
            if modality == 'T2FLAIR':
                # atlas_template = erly_template
                target_nifty_path = os.path.join(target_case_dir, nifty_path.split(os.sep)[-1].split('.')[0] + '_spgr.nii.gz')
                if os.path.exists(target_nifty_path):
                    continue
                register_images(spgr_template, nifty_path, target_nifty_path)

                target_nifty_path = os.path.join(target_case_dir, nifty_path.split(os.sep)[-1].split('.')[0] + '_late.nii.gz')
                if os.path.exists(target_nifty_path):
                    continue
                register_images(late_template, nifty_path, target_nifty_path)
            elif modality == 'T1' or modality == 'T1+C':
                target_nifty_path = os.path.join(target_case_dir, nifty_path.split(os.sep)[-1].split('.')[0] + '_spgr.nii.gz')
                if os.path.exists(target_nifty_path):
                    continue
                register_images(spgr_template, nifty_path, target_nifty_path)

            elif modality == 'T2':
                target_nifty_path = os.path.join(target_case_dir, nifty_path.split(os.sep)[-1].split('.')[0] + '_late.nii.gz')
                if os.path.exists(target_nifty_path):
                    continue
                register_images(late_template, nifty_path, target_nifty_path)
            else:
                print(f"error happened in func register_images when dealing with {nifty_path}")
                with open("./result_file/registration_modality_error.txt", "a") as f:
                    f.write(f"error happened in func register_images when dealing with {nifty_path}\n")
                continue



