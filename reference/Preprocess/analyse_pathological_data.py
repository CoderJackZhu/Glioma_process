#!/usr/bin/env python
# coding: utf-8

# ### Analyse the pathological data.
# 

# In[10]:


import os
import re
import pandas as pd
from tqdm import tqdm

# In[11]:


def analyze_pathological_data(data):
    if "免疫组化结果：" in data:
        data_split = data.split("免疫组化结果：")
    else:
        data_split = data.split("免疫组化：")

    """
    1. Analyze the subtype and the WHO grade of gliomas;
    """
    patho_data = data_split[0]
    patho_data = patho_data.replace("(", "（");
    patho_data = patho_data.replace(")", "）");
    WHO_grade = analyze_WHO_grade(patho_data)
    lesion_location = analyze_lesion_location(patho_data)
    gliomas_subtype = analyze_gliomas_subtype(patho_data)

    """
    2. Analyze the status of gene data.
    """
    gene_data, gene_data_list, GFAP, Ki67, P53, IDH, H3_K27M, Olig2, EGFR, ATRX, EMA, CD34, NeuN, CgA, Syn = "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""

    if len(data_split) > 1:
        gene_data = data_split[1]
        gene_data = gene_data.replace("；", "，");
        gene_data = gene_data.replace("。", "，");
        gene_data = gene_data.replace(",", "，");

        gene_data_list = gene_data.split("，")
        GFAP = analyze_gene_data(gene_data_list, "GFAP")
        Ki67 = analyze_gene_data(gene_data_list, "Ki67")
        P53 = analyze_gene_data(gene_data_list, "P53")
        IDH = analyze_gene_data(gene_data_list, "IDH")
        H3_K27M = analyze_gene_data(gene_data_list, "H3 K27M")
        Olig2 = analyze_gene_data(gene_data_list, "Olig2")
        EGFR = analyze_gene_data(gene_data_list, "EGFR")
        ATRX = analyze_gene_data(gene_data_list, "ATRX")
        EMA = analyze_gene_data(gene_data_list, "EMA")
        CD34 = analyze_gene_data(gene_data_list, "CD34")
        NeuN = analyze_gene_data(gene_data_list, "NeuN")
        CgA = analyze_gene_data(gene_data_list, "CgA")
        Syn = analyze_gene_data(gene_data_list, "Syn")

    return patho_data, WHO_grade, lesion_location, gliomas_subtype, gene_data, gene_data_list, GFAP, Ki67, P53, IDH, H3_K27M, Olig2, EGFR, ATRX, EMA, CD34, NeuN, CgA, Syn


def analyze_WHO_grade(patho_data):
    if any(_ in patho_data for _ in
           ["WHOⅣ", "WHO Ⅳ", "WHOIV", "WHO IV", "WHO4", "WHO 4", "Ⅳ级", "Ⅳ 级", "IV级", "IV 级"]):
        WHO_grade = 4
    elif any(_ in patho_data for _ in
             ["WHOⅢ", "WHO Ⅲ", "WHOIII", "WHO III", "WHO3", "WHO 3", "Ⅲ级", "Ⅲ 级", "III级", "III 级"]):
        WHO_grade = 3
    elif any(_ in patho_data for _ in
             ["WHOⅡ", "WHO Ⅱ", "WHO II", "WHOII", "WHO2", "WHO 2", "Ⅱ级", "Ⅱ 级", "II级", "II 级"]):
        WHO_grade = 2
    elif any(
            _ in patho_data for _ in ["WHOⅠ", "WHO Ⅰ", "WHOI", "WHO I", "WHO1", "WHO 1", "I级", "I 级", "Ⅰ级", "Ⅰ 级"]):
        WHO_grade = 1
    else:
        WHO_grade = ""

    return WHO_grade


def analyze_lesion_location(patho_data):
    lesion_location = patho_data.split("）")[0]
    start_index = lesion_location.find("（")

    return lesion_location[start_index + 1:]


def analyze_gliomas_subtype(patho_data):
    if any(_ in patho_data for _ in ["胶质母细胞", "胶质瘤母细胞瘤"]):
        gliomas_subtype = "胶质母细胞瘤"
    elif any(_ in patho_data for _ in ["少突胶质细胞瘤", "少突细胞瘤", "少突细胞胶质瘤", "少突胶质细胞质瘤"]):
        gliomas_subtype = "少突胶质瘤"
    elif any(_ in patho_data for _ in
             ["星形细胞瘤", "星型细胞瘤", "星形胶质细胞瘤", "星形细胞胶质", "星型细胞胶质瘤", "星形胶质瘤"]):
        gliomas_subtype = "星形细胞瘤"
    elif any(_ in patho_data for _ in ["节细胞胶质瘤", "节细胞细胞胶质瘤"]):
        gliomas_subtype = "节细胞胶质瘤"
    elif any(_ in patho_data for _ in ["中线胶质瘤"]):
        gliomas_subtype = "中线胶质瘤"
    else:
        gliomas_subtype = ""

    return gliomas_subtype


def analyze_gene_data(gene_data_list, gene_filter):
    gene_data = ""
    for data in gene_data_list:
        if gene_filter in data:
            gene_data = data

    return gene_data


# In[12]:


base_path = "F:\\Code\\Medical\\Glioma_process"
excel_path = os.path.join(base_path, "result_file/12321321.csv")
save_excel_path = os.path.join(base_path, "result_file/PathologicalData_DropNull_manualCorrected_analyzed.xlsx")

Data = pd.read_csv(excel_path, header=0)


# In[14]:


if __name__ == '__main__':
    # pathological_data=Data["病理诊断（手动矫正版本）"]
    pathological_data = Data.iloc[:, 2]
    # 加入很多新的列
    Data["pathological_data"] = ""
    Data["WHO_grade"] = ""
    Data["lesion_location"] = ""
    Data["gliomas_subtype"] = ""
    Data["gene_data"] = ""
    Data["gene_data_list"] = ""
    Data["GFAP"] = ""
    Data["Ki67"] = ""
    Data["P53"] = ""
    Data["IDH"] = ""
    Data["H3_K27M"] = ""
    Data["Olig2"] = ""
    Data["EGFR"] = ""
    Data["ATRX"] = ""
    Data["EMA"] = ""
    Data["CD34"] = ""
    Data["NeuN"] = ""
    Data["CgA"] = ""
    Data["Syn"] = ""

    # Data["pathological_data"], Data["WHO_grade"], Data["lesion_location"], Data["gliomas_subtype"], Data["gene_data"], Data[
    #     "gene_data_list"], Data["GFAP"], Data["Ki67"], Data["P53"], Data["IDH"], Data["H3_K27M"], Data["Olig2"], Data[
    #     "EGFR"], Data["ATRX"], Data["EMA"], Data["CD34"], Data["NeuN"], Data["CgA"], Data["Syn"] = zip(
    #     *pathological_data.apply(analyze_pathological_data))
    # Data.to_excel(save_excel_path)
    # 对于每行数据，分析病理数据，并将分析结果存入对应的列中
    # for data in pathological_data:
    #     Data.loc["pathological_data"], Data.loc["WHO_grade"], Data.loc["lesion_location"], Data.loc[
    #         "gliomas_subtype"], Data.loc["gene_data"], Data.loc["gene_data_list"], Data.loc["GFAP"], Data.loc[
    #         "Ki67"], Data.loc["P53"], Data.loc["IDH"], Data.loc["H3_K27M"], Data.loc["Olig2"], Data.loc[
    #         "EGFR"], Data.loc["ATRX"], Data.loc["EMA"], Data.loc["CD34"], Data.loc["NeuN"], Data.loc[
    #         "CgA"], Data.loc["Syn"] = analyze_pathological_data(data)
    for i in tqdm(range(len(pathological_data))):
        if type(pathological_data[i]) != str:
            continue
        path_data = analyze_pathological_data(pathological_data[i])
        Data.loc[i, "pathological_data"], Data.loc[i, "WHO_grade"], Data.loc[i, "lesion_location"], Data.loc[
            i, "gliomas_subtype"], Data.loc[i, "gene_data"], Data.loc[i, "gene_data_list"], Data.loc[i, "GFAP"], Data.loc[
            i, "Ki67"], Data.loc[i, "P53"], Data.loc[i, "IDH"], Data.loc[i, "H3_K27M"], Data.loc[i, "Olig2"], Data.loc[
            i, "EGFR"], Data.loc[i, "ATRX"], Data.loc[i, "EMA"], Data.loc[i, "CD34"], Data.loc[i, "NeuN"], Data.loc[
            i, "CgA"], Data.loc[i, "Syn"] = path_data
    Data.to_excel(save_excel_path)



