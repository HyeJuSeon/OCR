# OCR

[실전기계학습 팀프로젝트]

## Overview

원본 데이터에 Canny edge detection, Sharpening filter, Unsharp masking을 적용하여 성능을 비교하고자 했다.

## Dataset

- AI Hub 야외 실제 촬영 한글 이미지
  - 가로형 간판


## Model


[What Is Wrong With Scene Text Recognition Model Comparisons? Dataset and Model Analysis](https://arxiv.org/abs/1904.01906)

`TPS-ResNet-BiLSTM-CTC`

<br>

If your custom data is Korean,

```
git clone https://github.com/HyeJuSeon/deep-text-recognition-benchmark
```

## Training
- RGB
<img src="/img/origin_data_result.png">

- Canny edge
<img src="/img/canny_data_result.png">

- Sharpening filter
<img src="/img/sharp_data_result.png">

- Unsharp masking
<img src="/img/unsharp_data_result.png">

<br>

## Evaluation
|  |Accuracy|
|----|----|
|RGB|81%|
|Canny edge|74.24%|
|Sharpening filter|80.51%|
|Unsharp masking|80.51%|

<br>

## Link
[models](https://drive.google.com/drive/folders/1k4PlPYZxsDcPkDgD5aKbZq3qD30mmB8-?usp=sharing)

[발표자료](https://drive.google.com/file/d/1UOL4adUSCpo6L0f_WGP-9wk5945wewZN/view?usp=sharing)
