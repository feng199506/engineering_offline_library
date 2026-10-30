# P04 振动诊断：频谱、包络与特征（合成轴承示意）

| 项 | 内容 |
| --- | --- |
| 数据 | **示意合成** 外圈故障脉冲调制；**不是** CWRU/NASA 真机数据 |
| 真实数据 | CWRU / NASA PCoE 仅列官方入口，本轮默认未下载整库 |
| 状态 | 已整理，未运行验证 |

## 物理示意（简化，非真实轴承动力学）

载波（“共振”）约 2 kHz，重复频率 40 Hz 的指数衰减脉冲串 + 高斯噪声。  
包络谱期望在 40 Hz 及其谐波出现峰。这是教学模型，不能当现场诊断结论。

## 运行

```bash
python3 make_signal.py
python3 analyze.py
```

## 评价指标

包络谱 40 Hz 峰是否高于邻带；时域峭度。未运行留空。

## 真实数据入口（未下载则不算离线）

- NASA PCoE bearing：https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository
- CWRU：https://engineering.case.edu/bearingdatacenter （条款自行遵守）
