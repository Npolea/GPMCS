# 绘图脚本

按图片编号运行，数据放在仓库根目录 `data/`，图片输出到 `figures/`。

| 图片 | 命令 |
|---|---|
| Fig2a/b | `python plotting/current/Fig2_client_distribution.py --alpha 0.1`（或 `0.5`）|
| Fig3a-c | `python plotting/current/Fig3_validation_curves.py --panel a`（`b`、`c` 同理）|
| Fig4 | `python plotting/current/Fig4_client_selection.py` |
| Fig5 | `python plotting/current/Fig5_ablation_validation.py` |
| Fig6 | `python plotting/current/Fig6_participation.py` |

输入文件放在 `data/`，详见各脚本中的默认文件名；不包含原始数据文件。

