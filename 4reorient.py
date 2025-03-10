import os
import numpy as np
import itk
from tqdm import tqdm


def reorient_to_rai(image):
    """
    Reorient image to RAI orientation.
    :param image: Input itk image.
    :return: Input image reoriented to RAI.
    """
    try:
        filter = itk.OrientImageFilter.New(image)
        filter.UseImageDirectionOn()
        filter.SetInput(image)
        m = itk.GetMatrixFromArray(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], np.float64))
        filter.SetDesiredCoordinateDirection(m)
        filter.Update()
        reoriented = filter.GetOutput()
    except itk.support.extras.TemplateTypeError:
        reoriented = None
    finally:
        return reoriented


def one_reorient_to_rai(case_dir, target_dir):
    """
    Reorient all images in a case to RAI orientation.
    :param case_dir: Input case directory.
    :return: None.
    """
    for modality in os.listdir(case_dir):
        modality_file = os.path.join(case_dir, modality)
        image = itk.imread(modality_file)
        reoriented = reorient_to_rai(image)
        if reoriented is not None:
            itk.imwrite(reoriented, os.path.join(target_dir, modality))

if __name__ == '__main__':
    data_dir = r"/media/spgou/ZYJ/Nii_Dataset"
    case_dir_list = [os.path.join(data_dir, case) for case in os.listdir(data_dir)]
    target_dir = r"/media/spgou/ZYJ/Nii_Dataset_RAI"
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    for case_dir in tqdm(case_dir_list):
        # splited_case_dir = case_dir.split(os.sep)
        # splited_case_dir[1] = target_dir
        # target_case_dir = os.sep.join(splited_case_dir)
        # if not os.path.exists(target_case_dir):
        #     os.mkdir(target_case_dir)
        target_case_dir = os.path.join(target_dir, case_dir.split(os.sep)[-1])
        if not os.path.exists(target_case_dir):
            os.mkdir(target_case_dir)

        nifty_path_list = [os.path.join(case_dir, nifty) for nifty in os.listdir(case_dir)]

        for nifty_path in nifty_path_list:
            # splited_nifty_path = nifty_path.split(os.sep)
            # splited_nifty_path[1] = target_dir
            # target_nifty_path = os.sep.join(splited_nifty_path)
            target_nifty_path = os.path.join(target_case_dir, nifty_path.split(os.sep)[-1])
            if os.path.exists(target_nifty_path):
                continue
            try:
                image = itk.imread(nifty_path)
            except RuntimeError:
                print(f"can't read {nifty_path}")
                continue
            reoriented = reorient_to_rai(image)
            if reoriented is None:
                print(f"error happened in func reorient_to_rai when dealing with {nifty_path}")
            else:
                reoriented.SetOrigin([0, 0, 0])
                m = itk.GetMatrixFromArray(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], np.float64))
                reoriented.SetDirection(m)
                reoriented.Update()
                itk.imwrite(reoriented, target_nifty_path)