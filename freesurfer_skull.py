import os
import glob
import subprocess


def skull_strip():
    mgz_path = '/media/spgou/DATA/ZYJ/Dataset/skull-strip_mgz'
    files_dir = '/media/spgou/DATA/ZYJ/Dcm_process/some_nii_data'
    output_dir = '/media/spgou/DATA/ZYJ/Dataset/skull-strip_out'
    a = "#!/bin/bash export FREESURFER_HOME=$HOME/freesurfer;"
    b = "source $FREESURFER_HOME/SetUpFreeSurfer.sh;"
    c = "export SUBJECTS_DIR=" + mgz_path + ";"
    patients = os.listdir(files_dir)
    for patient in patients:
        input_patient_dir = os.path.join(files_dir, patient)
        out_patient_dir = os.path.join(output_dir, patient)
        if not os.path.exists(out_patient_dir):
            os.mkdir(out_patient_dir)
        output_patient_dir = os.path.join(output_dir, patient)
        if not os.path.exists(output_patient_dir):
            os.mkdir(output_patient_dir)
        nii_files = os.listdir(input_patient_dir)
        for nii_file in nii_files:
            nii_file_path = os.path.join(input_patient_dir, nii_file)
            file_name = nii_file.split('.')[0]
            cur_path = os.path.join(mgz_path, file_name)
            out_nii_file_path = os.path.join(out_patient_dir, nii_file)
            output_nii_file_path = os.path.join(output_patient_dir, nii_file)
            cmd = a + b + c + " recon-all -parallel -i " + nii_file_path + " -autorecon1 " + "-subjid " + cur_path + \
                  " && " + "mri_convert " + cur_path + "/mri/brainmask.mgz " + output_nii_file_path + ";"
            print(cmd)
            # os.system('./env_setting.sh')
            os.system(cmd)


if __name__ == "__main__":
    skull_strip()
