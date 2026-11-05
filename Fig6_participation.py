"""Reproduce R3-11 participation plots from the existing original-JS logs.

No training or log modification. Counts use t=45..150; wait histories
include preceding rounds and terminal (right-censored) nonselection.
"""
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MultipleLocator
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data'
OUT = ROOT / 'figures'
OUT.mkdir(parents=True, exist_ok=True)
FONT = font_manager.findfont('Times New Roman', fallback_to_default=False)
font_manager.fontManager.addfont(FONT)
plt.rcParams.update({
    'font.family': 'Times New Roman',
    'font.size': 12,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelcolor': '#242B35',
    'text.color': '#242B35',
    'xtick.color': '#424955',
    'ytick.color': '#424955',
    'axes.unicode_minus': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'path',
    'savefig.facecolor': 'white',
})

counts_all, waits_all, source_hashes = [], [], {}
diagnostic = json.loads((DATA/'R3_11_existing_logs_diagnostic.json').read_text(encoding='utf-8'))
for seed in range(3):
    directory = DATA/'original_js'/f'seed{seed}'
    source = directory/'rounds.jsonl'
    rows = [json.loads(s) for s in source.read_text(encoding='utf-8').splitlines()]
    assert len(rows) == 151
    counts = np.zeros(20, dtype=int)
    wait = np.zeros(20, dtype=int)
    longest = np.zeros(20, dtype=int)
    for t, row in enumerate(rows):
        assert row['round_index'] == t
        selected = row['selection']['selected']
        assert len(set(selected)) == 8
        assert sorted(row['selection']['available']) == list(range(20))
        wait += 1
        wait[selected] = 0
        if t >= 45:
            counts[selected] += 1
            longest = np.maximum(longest, wait)
    assert counts.tolist() == diagnostic['runs'][seed]['late_counts']
    assert int(longest.max()) == diagnostic['runs'][seed]['late_max_observed_consecutive_nonselection']
    assert counts.sum() == 848
    counts_all.append(counts)
    waits_all.append(longest)
    source_hashes[str(source.relative_to(DATA))] = hashlib.sha256(source.read_bytes()).hexdigest()

counts_all = np.array(counts_all)
waits_all = np.array(waits_all)
colors = ['#A5A3C3', '#AFD3D9', '#B9D2C0']
edges = ['#625F81', '#4C7982', '#5C8069']
x = np.arange(20)
width = 0.235
fig, axes = plt.subplots(2, 1, figsize=(10.4, 7.2), sharex=True)
fig.subplots_adjust(left=.085, right=.985, bottom=.125, top=.805, hspace=.27)
fig.suptitle('Post-exploration client participation', x=.535, y=.978,
             fontsize=18, fontweight='bold')
fig.text(.535, .935, 'CIFAR-10  |  alpha = 0.1  |  20 clients, 8 selected per round  |  Seeds 0–2',
         ha='center', va='center', fontsize=12, color='#505967')

for ax, values, title, ylabel in zip(
        axes, (counts_all, waits_all),
        ('(a) Participation counts', '(b) Longest observed nonselection'),
        ('Selection count', 'Consecutive unselected rounds')):
    for seed in range(3):
        ax.bar(x+(seed-1)*width, values[seed], width=width,
               facecolor=colors[seed], edgecolor=edges[seed], linewidth=.55,
               label=f'Seed {seed}', zorder=3)
    ax.set_title(title, loc='left', pad=9)
    ax.set_ylabel(ylabel, labelpad=10)
    ax.set_xlim(-.65,19.65)
    ax.set_ylim(0,64)
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.grid(True, linestyle='--', linewidth=.5, alpha=.65, color='#CBD2DA')
    ax.set_axisbelow(True)
    for side in ('top','right'):
        ax.spines[side].set_visible(False)
    for side in ('left','bottom'):
        ax.spines[side].set_color('#79828D')
        ax.spines[side].set_linewidth(.7)
    ax.tick_params(axis='both', labelsize=11, length=3, width=.6)

axes[0].axhline(42.4, color='#436289', linestyle=(0,(5,3)), linewidth=1.25, zorder=4)
axes[0].text(19.55,43.6,'Mean = 42.4',ha='right',va='bottom',fontsize=11,
             color='#345479',bbox={'facecolor':'white','edgecolor':'none','pad':1.3,'alpha':.92})
for seed in range(3):
    client = int(np.argmax(waits_all[seed]))
    value = int(waits_all[seed,client])
    axes[1].annotate(str(value),(client+(seed-1)*width,value),
                     xytext=(0,4),textcoords='offset points',ha='center',va='bottom',
                     fontsize=11, fontweight='bold',color=edges[seed])
axes[1].set_xticks(x)
axes[1].set_xlabel('Client ID',labelpad=8)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(.535,.898),
           ncol=3, frameon=False, fontsize=12, columnspacing=2.5,
           handlelength=1.6, handletextpad=.65)
fig.text(.085,.040,'Window: rounds 45–150 (106 rounds), after 45 exploration rounds.',
         fontsize=10.5,color='#596370')
fig.text(.085,.015,'Waiting history is retained across the window boundary; terminal unselected streaks are included.',
         fontsize=10.5,color='#596370')

stem = OUT/'Fig6'
fig.savefig(stem.with_suffix('.png'), dpi=600)
fig.savefig(stem.with_suffix('.pdf'))
fig.savefig(stem.with_suffix('.svg'))
fig.savefig(OUT/'R3_11_participation_preview.png', dpi=150)
plt.close(fig)
with (OUT/'Fig6_participation_data.csv').open('w',newline='',encoding='utf-8') as stream:
    writer = csv.writer(stream)
    writer.writerow(['seed','client_id','post_exploration_selection_count','longest_observed_nonselection_rounds'])
    for seed in range(3):
        for client in range(20):
            writer.writerow([seed,client,int(counts_all[seed,client]),int(waits_all[seed,client])])
(OUT/'Fig6_provenance.json').write_text(json.dumps({
    'font':Path(FONT).name,'dpi':600,'pixel_dimensions':[6240,4320],
    'method':'GPMCS original_js','dataset':'CIFAR-10',
    'alpha':.1,'alpha_basis':'Author correction confirmed 2026-09-28; original metadata retain 0.5.',
    'window':'round indices 45 through 150 inclusive',
    'max_observed_nonselection_per_seed':waits_all.max(axis=1).tolist(),
    'interpretation':'Observed counts and waiting, not comparative fairness or a guaranteed waiting bound.',
    'source_sha256':source_hashes,
},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Saved Fig6 PNG (600 dpi), PDF, SVG, CSV, and provenance in:',OUT)
print('Times New Roman:',FONT)
