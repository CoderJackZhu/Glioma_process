# 胶质瘤数据处理
## CaPTK数据处理流程
处理流程：

1. CaPTk: dcm图像转nii
- 这一步要确保将图像匿名化，匿名化可以按上次我发你的那个匿名对应表格来处理，保证匿名化后的数据可以反推回去真实的病人id
- 匿名化包含 1)确保a头部文件里没有病人隐私信息;2) ai文件命名时，使用匿名化后的 id 来命名，不要使用真是的病人id 命名。
- 研究下 CaPTk 匿名化选项里，都做了哪些处理。如果不清楚的话，慎用。弄清楚以后，刚好可以看下我们有没有遗漏什么需要匿名化的信息。目前，我们只匿名化了病人姓名和 id
- 抽查dcm,转ni.转换效果，不要因为技术问题丢失图片。

2. CaPTK:将匿名化后的ni 扔进 BraTs pipeline 里进行图像预处理就行。

- 随机抽查 CaPTK 预处理后的效果，包含1)方向 RAI; 2)四个序列已经成功配准;3)resampling 成了mmxammx1mm;4)去头骨成功。

3.分清术前、术后图像。术前术后，就是按上次张医生说的，在报告日期前算是术前影像，报告日期后是术后影像。

4.下一步:使用病人术前的 MRI影像(含 T1T1CET2Flair 四个序列)，来预测病人的 WHO 等级、肿瘤亚型、基因变异情况。

## CaPTK代码结构
1. 根据融合后的表格信息批量转换dcm为nii文件
2. 对转完之后的文件重命名为正常的id+data+modality，放到id+date文件夹里面
3. 筛选出具有四个模态的对应日期的病人
4. 分清术前和术后的病人
5. 读取匿名化表格并将nii文件按照新的id匿名化
6. 使用BraTS pipeline进行预处理
7. 挑选出四个模态文件和分割文件

## 其他问题
fsl的安装非常麻烦，可以使用nipype，python库，可以直接使用pip安装
例如，使用
```python
 from nipype.interfaces.fsl import BET
>>> BET.help()
```