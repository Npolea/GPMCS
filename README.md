# GPMCS 实验配置与绘图

本仓库首批仅含实验命令、Fig2–Fig6 绘图脚本和文章直接引用的结果汇总 CSV。

## 实验命令

数据分区由已有 config 决定 alpha；运行前备份配置和分区文件，不覆盖已有数据。

```powershell
# PFLlib dataset 目录；仅在需要重建分区时运行
python generate_FashionMNIST.py noniid - exdir
python generate_Cifar10.py noniid - exdir
python generate_Cifar100.py noniid - exdir
```

基线命令从 `PFLlib-master - basev/system` 运行。统一 CNN、20 客户端、每轮 8 客户端、每客户端本地训练 1 epoch、`-gr 150`。下面为 GPFL 的 CIFAR-100 示例：

```powershell
python main.py -data Cifar100 -m CNN -algo GPFL -gr 150 -did 0 -nc 20 -ncl 100 -jr 0.4 -ls 1 -lbs 10 -lr 0.005 -lam 0.01 -mu 0.1
```

主表其他方法在同一命令中替换 `-algo`，并按方法设置参数：

| 方法 | 参数 |
|---|---|
| GPFL | `-lam 0.01 -mu 0.1` |
| FedProto | CIFAR-100/Fashion-MNIST：`-lam 1.0`；CIFAR-10：`-lbs 32 -lr 0.01 -lam 0.1` |
| FedPer、FedAvg、LG-FedAvg | 无额外参数；LG-FedAvg 的 CIFAR-10 用 `-lbs 50 -lr 0.1` |
| FedRep | `-pls 1` |
| FedBABU | `-fte 10` |
| FedProx | `-mu 0.1` |

CIFAR-10 选择器比较使用现有 CIFAR-10 分区和相同 GPFL 参数：

```powershell
python main.py -data Cifar10 -m CNN -algo GPFL_UCB -gr 150 -did 0 -nc 20 -ncl 10 -jr 0.4 -ls 1 -lbs 10 -lr 0.005 -lam 0.01 -mu 0.1
python main.py -data Cifar10 -m CNN -algo GPFL_PoC -gr 150 -did 0 -nc 20 -ncl 10 -jr 0.4 -ls 1 -lbs 10 -lr 0.005 -lam 0.01 -mu 0.1 -seed 0
```

`GPFL_UCB`、`GPFL_PoC` 是本地扩展。此处命令是配置示例，不代表本仓库包含全部运行记录。

## 绘图

脚本按文章图号位于 `plotting/current/`。输入放在 `data/`，图件输出到 `figures/`；脚本路径均相对于脚本位置。对应 XLSX 和 CIFAR-10 原始选择日志未纳入本次上传，补齐输入后再运行。

| 图片 | 脚本 | 输入 |
|---|---|---|
| Fig2a、Fig2b | `plotting/current/Fig2_client_distribution.py` | `config-cifar10-0.1.json`、`config-cifar10-0.5.json` |
| Fig3a–Fig3c | `plotting/current/Fig3_validation_curves.py` | `cifar100-0.1.xlsx`、`cifar10-0.1.xlsx`、`fmnist-0.1.xlsx` |
| Fig4 | `plotting/current/Fig4_client_selection.py` | `Fig4.xlsx` |
| Fig5 | `plotting/current/Fig5_ablation_validation.py` | `Fig5.xlsx` |
| Fig6 | `plotting/current/Fig6_participation.py` | `data/original_js/seed0..2/rounds.jsonl` |

运行示例：

```powershell
python plotting/current/Fig2_client_distribution.py --alpha 0.1
python plotting/current/Fig3_validation_curves.py --panel a --input data/cifar100-0.1.xlsx
python plotting/current/Fig4_client_selection.py
python plotting/current/Fig5_ablation_validation.py
python plotting/current/Fig6_participation.py
```

绘图依赖为 `numpy`、`pandas`、`matplotlib`；读取 Excel 另需 `openpyxl`。Fig6 的输入目录为 `data/original_js/seed0..2/`，并需 `data/R3_11_existing_logs_diagnostic.json`。Fig1 是结构图，没有对应 Python 脚本。XLSX 和 Fig6 原始日志未随本批上传。

## 结果汇总

`logs/` 暂时保留文章所用的逐种子汇总 CSV：Table 4 Local-only、Table 5 耦合控制、Table 7/Fig6 参与记录、S3 资源压力测试和 FigS1 GPFL+PoC。
