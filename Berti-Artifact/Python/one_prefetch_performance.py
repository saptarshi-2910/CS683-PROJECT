#!/usr/bin/python3
"""
fig8.py - Speedup comparison across 6 prefetchers
IP-Stride, MLOP, IPCP, BINGO, PPF, Berti
"""
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from scipy.stats import gmean

HEIGHT = 1.15

if __name__ == "__main__":
    rc('font', size=13)
    name  = []
    
    # 6 configurations to display
    order = {
        'IP-Stride': [],
        'MLOP': [],
        'IPCP': [],
        'BINGO': [],
        'PPF': [],
        'Berti': [],
    }

    geo = {
        'IP-Stride': [],
        'MLOP': [],
        'IPCP': [],
        'BINGO': [],
        'PPF': [],
        'Berti': [],
    }

    color = {
        'IP-Stride': 'silver',
        'MLOP': 'whitesmoke',
        'IPCP': 'darkgray',
        'BINGO': 'gainsboro',
        'PPF': 'snow',
        'Berti': 'black',
    }

    pattern = {
        'IP-Stride': '\\\\\\',
        'MLOP': '',
        'IPCP': '',
        'BINGO': '///',
        'PPF': '///',
        'Berti': '',
    }

    # Translation map for the 6 configurations
    translation = {
        'ip_stride+no': 'IP-Stride',
        'mlop_dpc3+no': 'MLOP',
        'ipcp_isca2020+no': 'IPCP',
        'no+bingo_dpc3': 'BINGO',
        'no+ppf': 'PPF',
        'vberti+no': 'Berti'
    }

    translation_suite = ['SPEC17-MemInt']

    bench = []
    text = {}

    with open(sys.argv[1]) as f:
        raw = f.read().split('\n')

        last = None
        jump = False
        
        for idx, i in enumerate(raw[:-1]):
            splitted = i.split(';')

            if len(splitted) == 1:
                jump = False
                # Skip certain suites
                if (splitted[0] == "spec2k17_all") or (splitted[0] == "cvp") or (splitted[0] == "cloudsuite") or (splitted[0] == "gap"):
                    jump = True
                    continue
                bench.append(splitted[0])
            elif not jump:
                pref = "{}+{}".format(splitted[0], splitted[1])
                
                if pref not in translation:
                    continue
                
                height = float(splitted[2])
                
                # Handle bars that exceed HEIGHT
                if height > HEIGHT:
                    if translation[pref] not in text:
                        text[translation[pref]] = []
                    text[translation[pref]].append((len(order[translation[pref]]), height))
                    order[translation[pref]].append(HEIGHT)
                    geo[translation[pref]].append(height)
                else:
                    order[translation[pref]].append(height)
                    geo[translation[pref]].append(height)
                    
                name.append(pref)

    # Print what we found
    print("\nConfigurations found:")
    for pref in order:
        if len(order[pref]) > 0:
            print(f"  ✓ {pref}: {order[pref][0]:.4f}")
        else:
            print(f"  ✗ {pref}: NO DATA")

    # Create figure
    x = np.arange(len(bench))
    fig, ax = plt.subplots(figsize=(7, 2.5))
    
    # Bar positions for 6 prefetchers
    # Centered around 0: -.375, -.225, -.075, .075, .225, .375
    positions = [-.375, -.225, -.075, .075, .225, .375]
    WIDTH = 0.12
    
    # Plot each prefetcher in order
    prefetcher_order = ['IP-Stride', 'MLOP', 'IPCP', 'BINGO', 'PPF', 'Berti']
    
    for prefetcher, pos in zip(prefetcher_order, positions):
        if len(order[prefetcher]) > 0:
            ax.bar(x + pos, order[prefetcher], width=WIDTH, edgecolor='black', 
                   zorder=3, color=color[prefetcher], hatch=pattern[prefetcher], 
                   label=prefetcher)
            
            # Add text for values exceeding HEIGHT
            if prefetcher in text:
                for ii in text[prefetcher]:
                    ax.text(ii[0] + pos - 0.05, HEIGHT + 0.01, 
                           round(ii[1], 2), fontsize=9)

    # Y-axis
    below = 0.9
    step = 0.05
    ax.set_ylim((below, HEIGHT))
    ax.set_yticks([i for i in np.arange(below, HEIGHT + 0.01, step)])
    ax.set_yticks([i for i in np.arange(below, HEIGHT + 0.01, step/2)], minor=True)

    # X-axis
    ax.set_xticks([0])
    ax.set_xticklabels(translation_suite)
    ax.set_ylabel("Speedup")

    # Grid
    ax.yaxis.grid(True, zorder=1, which='major')
    ax.yaxis.grid(True, zorder=1, which='minor', linestyle='--')

    # Baseline at 1.0
    ax.axhline(y=1, color='black', linestyle='-', linewidth=1.5)

    # Legend - 2 rows of 3
    legend = plt.legend(loc=10, bbox_to_anchor=(0.5, 1.15),
                       ncol=3, edgecolor='black', framealpha=1.0)
    legend.get_frame().set_alpha(None)
    legend.get_frame().set_facecolor((0, 0, 0, 0))

    fig.tight_layout()
    plt.savefig("fig8.pdf", bbox_inches='tight')
    print("\n✓ Figure 8 saved as fig8.pdf")