#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pydicom
import os
import pandas as pd
from multiprocessing import Pool


class DcmData(object):
    def __init__(self, path):
        self.path = path
        self.dcm_info = pydicom.read_file(path, force=True)
        self.dcm_info.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        self.Infos = {
            'ImageName': os.path.basename(path),
            'ImagePath': path,
            'PatientName': None,
            'PatientID': None,
            'PatientBirthDate': None,
            'PatientSex': None,
            'PatientAge': None,
            'PatientSize': None,
            'PatientWeight': None,
            'PregnancyStatus': None,

            'StudyID': None,
            'StudyDate': None,
            'StudyTime': None,
            'AccessionNumber': None,
            'SeriesDate': None,
            'SeriesTime': None,
            'SeriesDescription': None,
            'SeriesNumber': None,
            'SpecificCharacterSet': None,
            'ImageType': None,

            'Manufacturer': None,
            'ManufacturerModelName': None,
            'SoftwareVersions': None,
            'StationName': None,
            'ProtocolName': None,
            'AcquisitionMatrix': None,
            'PixelSpacing': None,
            'MagneticFieldStrength': None,
            'SpacingBetweenSlices': None,
            'SliceThickness': None,
            'PixelBandwidth': None,
            'PercentPhaseFieldOfView': None,
            'PercentSampling': None,

            'MRAcquisitionType': None,
            'InstanceNumber': None,
            'FOV': None,
        }
        # 'ImagePlane': None,
        # 'Matrix': None,

        for attribute in self.dcm_info:
            # if attribute.keyword == 'SOPInstanceUID':
            #     self.Infos['SOPInstanceUID'] = attribute.value

            if attribute.keyword == 'PatientName':
                self.Infos['PatientName'] = attribute.value

            elif attribute.keyword == 'PatientID':
                self.Infos['PatientID'] = attribute.value

            elif attribute.keyword == 'PatientBirthDate':
                self.Infos['PatientBirthDate'] = attribute.value

            elif attribute.keyword == 'PatientSex':
                self.Infos['PatientSex'] = attribute.value

            elif attribute.keyword == 'PatientAge':
                self.Infos['PatientAge'] = attribute.value

            elif attribute.keyword == 'PatientSize':
                self.Infos['PatientSize'] = attribute.value

            elif attribute.keyword == 'PatientWeight':
                self.Infos['PatientWeight'] = attribute.value

            elif attribute.keyword == 'PregnancyStatus':
                self.Infos['PregnancyStatus'] = attribute.value

            elif attribute.keyword == 'StudyID':
                self.Infos['StudyID'] = attribute.value

            elif attribute.keyword == 'StudyDate':
                self.Infos['StudyDate'] = attribute.value

            elif attribute.keyword == 'StudyTime':
                self.Infos['StudyTime'] = attribute.value

            elif attribute.keyword == 'AccessionNumber':
                self.Infos['AccessionNumber'] = attribute.value

            elif attribute.keyword == 'SeriesDescription':
                self.Infos['SeriesDescription'] = attribute.value

            elif attribute.keyword == 'SeriesNumber':
                self.Infos['SeriesNumber'] = attribute.value

            elif attribute.keyword == 'SpecificCharacterSet':
                self.Infos['SpecificCharacterSet'] = attribute.value

            elif attribute.keyword == 'ImageType':
                self.Infos['ImageType'] = attribute.value


            elif attribute.keyword == 'Manufacturer':
                self.Infos['Manufacturer'] = attribute.value

            elif attribute.keyword == 'ManufacturerModelName':
                self.Infos['ManufacturerModelName'] = attribute.value

            elif attribute.keyword == 'SoftwareVersions':
                self.Infos['SoftwareVersions'] = attribute.value

            elif attribute.keyword == 'StationName':
                self.Infos['StationName'] = attribute.value

            elif attribute.keyword == 'ProtocolName':
                self.Infos['ProtocolName'] = attribute.value

            elif attribute.keyword == 'AcquisitionMatrix':
                matrix = attribute.value
                # if matrix[1] != 0 and matrix[2] != 0:
                #     self.Infos['Matrix'] = str(matrix[1]) + 'x' + str(matrix[2])
                # elif matrix[0] != 0 and matrix[3] != 0:
                #     self.Infos['Matrix'] = str(matrix[0]) + 'x' + str(matrix[3])
                # else:
                #     self.Infos['Matrix'] = 'Others'

            elif attribute.keyword == 'PixelSpacing':
                self.Infos['PixelSpacing'] = attribute.value

            elif attribute.keyword == 'MagneticFieldStrength':
                self.Infos['MagneticFieldStrength'] = float(attribute.value)

            elif attribute.keyword == 'SpacingBetweenSlices':
                self.Infos['SpacingBetweenSlices'] = attribute.value if attribute.value is not None else 0

            elif attribute.keyword == 'SliceThickness':
                self.Infos['SliceThickness'] = attribute.value if attribute.value is not None else 0

            elif attribute.keyword == 'PixelBandwidth':
                self.Infos['PixelBandwidth'] = attribute.value if attribute.value is not None else 0

            elif attribute.keyword == 'PercentPhaseFieldOfView':
                self.Infos['PercentPhaseFieldOfView'] = attribute.value if attribute.value is not None else 0

            elif attribute.keyword == 'PercentSampling':
                self.Infos['PercentSampling'] = attribute.value if attribute.value is not None else 0


            elif attribute.keyword == 'MRAcquisitionType':
                self.Infos['MRAcquisitionType'] = attribute.value

            elif attribute.keyword == 'InstanceNumber':
                self.Infos['InstanceNumber'] = attribute.value

            # elif attribute.keyword == 'ImagePlane':
            #     self.Infos['ImagePlane'] = attribute.value

            # elif attribute.keyword == 'Matrix':
            #     self.Infos['Matrix'] = attribute.value

            elif attribute.keyword == 'ReconstructionDiameter':
                self.Infos['FOV'] = float(attribute.value) / 10

            # elif attribute.keyword == 'PixelData':
            #     self.PixelData = attribute.value

        # self.analyze_ImageType()
        # self.analyze_ImagePlane()

    def analyze_ImageType(self):
        if 'T1 mapping' in self.Infos['SeriesDescription']:
            ImageType = 'T1 mapping'
        elif 'T1' in self.Infos['SeriesDescription']:
            ImageType = 'T1'
        elif 'T2 FLAIR' in self.Infos['SeriesDescription']:
            ImageType = 'T2 FLAIR'
        elif 'T2' in self.Infos['SeriesDescription']:
            ImageType = 'T2'
        elif 'CUBE FLAIR' in self.Infos['SeriesDescription']:
            ImageType = 'CUBE FLAIR'
        else:
            ImageType = 'Others'
            # ImageType='T1'

        self.Infos['ImageType'] = ImageType

    def analyze_ImagePlane(self):
        if 'Ax' in self.Infos['SeriesDescription']:
            ImagePlane = 'Ax'
        elif 'AX' in self.Infos['SeriesDescription']:
            ImagePlane = 'Ax'
        elif 'Sag' in self.Infos['SeriesDescription']:
            ImagePlane = 'Sag'
        else:
            ImagePlane = 'Others'

        self.Infos['ImagePlane'] = ImagePlane

    def show_all_attributes(self):
        for attribute in self.dcm_info:
            if attribute.keyword != '' and attribute.keyword != 'PixelData':
                print('--{}:  {}'.format(attribute.keyword, attribute.value))

    def get_dataInfos(self):
        return self.Infos

    def get_SeriesDescription(self):
        return self.Infos['SeriesDescription']

    def get_Matrix(self):
        return self.Infos['Matrix']

    def get_image_type(self):
        return self.Infos['ImageType']

    def get_field_strength(self):
        return self.Infos['MagneticFieldStrength']

    def get_FOV(self):
        return self.Infos['FOV']

    def get_PixelData(self):
        return self.PixelData


def normal_save():
    dataset_path = r'G:\DCM_Dataset\2021-12-17胶质瘤-约760例\DICOM\PA0\ST0'
    all_data = pd.DataFrame()

    for paths, dirnames, filenames in os.walk(dataset_path):
        for dir in dirnames:
            dir_path = os.path.join(paths, dir)
            files = os.listdir(dir_path)
            img_path = os.path.join(dir_path, files[0])
            if os.path.isdir(img_path):
                continue
            # try:
            print(img_path)
            dcm_data = DcmData(img_path)
            data = dcm_data.Infos
            # dcm_data.show_all_attributes()
            print(data)
            info_data = pd.DataFrame.from_dict(data, orient='index').T
            all_data = pd.concat([all_data, info_data], axis=0)
            # except:
            #     print(f'img_path:{img_path}')
            #     continue

            # info_data = pd.DataFrame(dcm)
            #     print(info_data)

        all_data.to_excel('result.xlsx')

    # dcm_data = DcmData(dataset_path)
    # # dcm_data.show_all_attributes()
    # data =  dcm_data.Infos
    # print(data)
    # data = pd.DataFrame(data)
    # data.to_excel('data.xlsx')





if __name__ == '__main__':
    normal_save()
