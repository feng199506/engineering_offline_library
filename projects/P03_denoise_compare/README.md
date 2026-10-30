# P03 去噪：数字滤波、小波、EMD 系列

| 项 | 内容 |
| --- | --- |
| 数据 | **示意合成**：干净块状/正弦 + 高斯噪声 |
| 状态 | 已整理，未运行验证 |
| 因果 | `filtfilt` 与全序列 EMD 为 **离线非因果**；Butterworth `lfilter` 为因果 |

## 目的

同一噪声实现上比较 SNR **和** 边缘 RMSE。禁止只报 SNR。

## 运行

```bash
python3 make_signal.py
python3 analyze.py
```

缺 PyEMD / pywt 时该项标记 skipped。

## 预期现象（逻辑）

- 低通 FIR/IIR：平滑正弦好，块边缘变钝。
- `filtfilt`：边缘对称变钝，看起来“相位好”，但是非因果。
- 小波软阈值：块边缘通常优于强低通，噪声模型不对时会切掉细节。
- EMD：可能把噪声拆进前几阶 IMF；端点处易畸变。未运行不得写“EMD 最好”。

## 评价指标

SNR、RMSE、边缘 10 点 RMSE、是否因果。
