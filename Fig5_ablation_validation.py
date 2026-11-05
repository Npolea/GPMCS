import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=Path('data/XRex-10.5.xlsx'))
    args = parser.parse_args()
    source = args.input if args.input.is_absolute() else ROOT / args.input
    df = pd.read_excel(source)
    df.columns = df.columns.str.strip()
    x = df.index.to_numpy()
    plt.rcParams['font.family'] = 'Times New Roman'
    fig, ax = plt.subplots(figsize=(10, 6))
    lines = [('DPFO', 'w/o DPFO', '#70AD47'), ('RANDOM', 'w/o SACE Algorithm', '#5B9BD5'),
             ('DSGA', 'w/o DSGA', '#B565C0'), ('GPMCS', 'GPMCS', '#C00000')]
    for column, label, color in lines:
        kw = {'marker': 'o', 'markersize': 6, 'markevery': 15} if column == 'GPMCS' else {}
        ax.plot(x, df[column], label=label, color=color, linewidth=3, **kw)
    ax.grid(True, color='lightgray', linewidth=1.2, alpha=.8)
    ax.set_xlabel('Iterations', fontsize=16, fontweight='bold')
    ax.set_ylabel('Accuracy', fontsize=16, fontweight='bold')
    ax.set_xlim(0, len(x)-1)
    ax.set_ylim(0, .8)
    ax.tick_params(labelsize=14)
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
        spine.set_color('black')
    ax.legend(loc='lower right', frameon=False, prop={'weight': 'bold', 'size': 13})
    fig.tight_layout()
    output = ROOT / 'figures'
    output.mkdir(parents=True, exist_ok=True)
    fig.savefig(output / 'Fig5.png', dpi=600, bbox_inches='tight')
    fig.savefig(output / 'Fig5.pdf', bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
