import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--alpha', choices=['0.1', '0.5'], default='0.1')
    args = parser.parse_args()
    config_path = ROOT / 'data' / f'config-cifar10-{args.alpha}.json'
    output = ROOT / 'figures'
    output.mkdir(parents=True, exist_ok=True)
    config = json.loads(config_path.read_text(encoding='utf-8'))
    n_clients = config['num_clients']
    n_classes = config['num_classes']
    counts = np.zeros((n_clients, n_classes), dtype=float)
    for client, labels in enumerate(config['Size of samples for labels in clients']):
        for label, count in labels:
            counts[client, label] = count
    totals = counts.sum(axis=1, keepdims=True)
    totals[totals == 0] = 1
    cmap = LinearSegmentedColormap.from_list(
        'light_blue_red', ['#eaf3f8', '#d7e8f2', '#f7f7f7', '#f6c6cf', '#e8899d', '#c93f5c']
    )
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    image = ax.imshow((counts / totals).T, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    ax.set_xlabel('Client ID')
    ax.set_ylabel('Class label')
    ax.set_xticks(np.arange(n_clients), [str(i) for i in range(n_clients)], fontsize=8)
    ax.set_yticks(np.arange(n_classes), [str(i) for i in range(n_classes)], fontsize=9)
    ax.set_xticks(np.arange(-.5, n_clients, 1), minor=True)
    ax.set_yticks(np.arange(-.5, n_classes, 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=.7)
    ax.tick_params(which='minor', bottom=False, left=False)
    fig.colorbar(image, ax=ax, fraction=.035, pad=.025, label='Class proportion')
    ax.set_title(f"CIFAR-10 Client-Class Distribution ($\\alpha$={args.alpha})")
    fig.tight_layout()
    panel = 'a' if args.alpha == '0.1' else 'b'
    stem = output / f'Fig2{panel}'
    fig.savefig(stem.with_suffix('.pdf'), bbox_inches='tight')
    fig.savefig(stem.with_suffix('.png'), dpi=600, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
