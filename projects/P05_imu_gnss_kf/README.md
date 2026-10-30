# P05 状态估计：Kalman 与合成 IMU/GNSS 融合

| 项 | 内容 |
| --- | --- |
| 数据 | **示意合成** 2D 匀速 + 加速度计偏置 + 稀疏 GNSS 位置 |
| 状态 | 已整理，未运行验证，**未接 IMU/GNSS 硬件** |
| 环境 | `01_scientific_notebook_*` 或 `11_optimization_control_*` |

## 模型

状态 \([p_x,p_y,v_x,v_y,b_{ax},b_{ay}]\)。IMU 100 Hz 加速度（含偏置与噪声）；GNSS 5 Hz 位置。

对比：

- 因果 KF（只用到当前）。
- 可选离线 RTS 平滑（用未来，**不可当机载指标**）。

## 运行

```bash
python3 simulate.py
python3 filter_run.py
```

## 评价指标

位置 RMSE、速度 RMSE、NEES（一致性）。平滑 RMSE 必须单独成列。

## 常见错误

GNSS 与 IMU 用同一数组下标却假装有 20 ms 延迟。本仿真延迟为 0，已在 README 标明，不是真实接收机。
