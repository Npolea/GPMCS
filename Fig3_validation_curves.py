import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DEFAULTS = {'a': 'cifar100-0.1.xlsx', 'b': 'cifar10-0.1.xlsx', 'c': 'fmnist-0.1.xlsx'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--panel', choices=DEFAULTS, required=True)
    parser.add_argument('--input', type=Path)
    args = parser.parse_args()
    source = args.input if args.input else ROOT / 'data' / DEFAULTS[args.panel]
    if not source.is_absolute():
        source = ROOT / source
    df = pd.read_excel(source)
    x = df.index.to_numpy()
    plt.rcParams['font.family'] = 'Times New Roman'
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {'LG-FedAvg': '#5B9BD5', 'FedAvg': '#7F7F7F', 'GPFL': '#92D050',
              'FedProto': '#DDA0DD', 'GPMCS': '#C00000'}
    for name, color in colors.items():
        kw = {'marker': 'o', 'markersize': 8, 'markevery': 15} if name == 'GPMCS' else {}
        ax.plot(x, df[name], label='GPMCS (Ours)' if name == 'GPMCS' else name,
                color=color, linewidth=3, **kw)
    ax.grid(True, color='lightgray', linewidth=1.2)
    ax.set_xlabel('Iterations', fontsize=16, fontweight='bold')
    ax.set_ylabel('Accuracy', fontsize=16, fontweight='bold')
    ax.set_xlim(0, len(x)-1)
    ax.set_ylim(0, df.max().max()+.1)
    ax.tick_params(labelsize=14)
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
        spine.set_color('black')
    ax.legend(loc='lower right', ncol=2, frameon=False, prop={'weight': 'bold', 'size': 14})
    fig.tight_layout()
    output = ROOT / 'figures'
    output.mkdir(parents=True, exist_ok=True)
    fig.savefig(output / f'Fig3{args.panel}.png', dpi=600, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
