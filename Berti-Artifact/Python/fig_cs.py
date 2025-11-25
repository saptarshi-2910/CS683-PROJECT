#!/usr/bin/python3
"""
Updated fig_cs.py for CS683 Project (Final Version)
Generates Figure 18 using memory-intensive SPEC CPU traces
WITHOUT MISB configurations (not built)
"""
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from scipy.stats import gmean
from pprint import pprint

if __name__ == "__main__":
    rc('font', size=13)

    # Colors for different prefetcher families
    color = {
            'MLOP': 'whitesmoke',
            'MLOP+Bingo': 'whitesmoke',
            'MLOP+SPP-PPF': 'whitesmoke',
            'IPCP': 'darkgray',
            'IPCP+IPCP': 'darkgray',
            'Berti': 'black',
            'Berti+Bingo': 'black',
            'Berti+SPP-PPF': 'black',
            }

    # Patterns to distinguish multi-level configs
    pattern = {
            'MLOP': '',              # Solid
            'MLOP+Bingo': '///',     # Diagonal
            'MLOP+SPP-PPF': '...',   # Dots
            'IPCP': '',              # Solid
            'IPCP+IPCP': '\\\\\\',   # Backslash
            'Berti': '',             # Solid
            'Berti+Bingo': '///',    # Diagonal
            'Berti+SPP-PPF': '...',  # Dots
            }

    # Map configuration names to display names
    translation = {
        'mlop_dpc3_no': 'MLOP',
        'mlop_dpc3_bingo_dpc3': 'MLOP+Bingo',
        'mlop_dpc3_ppf': 'MLOP+SPP-PPF',
        'ipcp_isca2020_no': 'IPCP',
        'ipcp_isca2020_ipcp_isca2020': 'IPCP+IPCP',
        'vberti_no': 'Berti',
        'vberti_ppf': 'Berti+SPP-PPF',
        'vberti_bingo_dpc3': 'Berti+Bingo',
            }

    dic = {}

    # Read CSV file
    with open(sys.argv[1]) as f:
        raw = f.read().split('\n')
        element = raw[0].split(';')[1:]  # Config names from header

        # Parse data rows
        for i in raw[1:-1]:
            aux = i.split(';')
            if len(aux) > 1 and aux[0]:  # Skip empty lines
                dic[aux[0]] = []
                for ii in aux[1:-1]:
                    try:
                        dic[aux[0]].append(float(ii))
                    except ValueError:
                        dic[aux[0]].append(0.0)

    # Updated figure size for 10 workloads
    fig, ax = plt.subplots(figsize=(10, 2))

    # Configurations to plot (8 total)
    to_graph = [
            'mlop_dpc3_no', 
            'mlop_dpc3_bingo_dpc3', 
            'mlop_dpc3_ppf',
            'ipcp_isca2020_no', 
            'ipcp_isca2020_ipcp_isca2020', 
            'vberti_no', 
            'vberti_bingo_dpc3',
            'vberti_ppf'
            ]

    # Organize data by configuration
    y = {}
    for i in dic:
        for ii, jj in zip(dic[i], element):
            if jj in to_graph:
                if jj not in y:
                    y[jj] = []
                y[jj].append(ii)

    # Bar positions for 8 configurations
    xst = [-.32, -.24, -.16, -.08, .0, .08, .16, .24]
    WIDTH = 0.08
    
    # Generate output line with all data
    line = ""
    workload_names = list(dic.keys())
    
    for pos, i in zip(xst, to_graph):
        if i not in y or len(y[i]) == 0:
            print(f"Warning: No data for configuration {i}")
            continue
            
        # Build description line
        config_name = translation[i]
        line += f"{config_name}: "
        for idx, val in enumerate(y[i]):
            if idx < len(workload_names):
                line += f"{workload_names[idx]}={val:.3f}, "
        line += "; "
        
        # Plot bars
        if i.split('_')[0] == "vberti":
            # Berti configs: white bars with black outline
            ax.bar(np.arange(len(y[i])) + pos, y[i], width=WIDTH,
                    color=color[translation[i]], edgecolor='snow',
                    hatch=pattern[translation[i]], zorder=3,
                    label=translation[i])
            ax.bar(np.arange(len(y[i])) + pos, y[i], width=WIDTH,
                    color='none', edgecolor='black', zorder=4, lw=1.2)
        else:
            # Other configs: normal bars
            ax.bar(np.arange(len(y[i])) + pos, y[i], width=WIDTH,
                    color=color[translation[i]], edgecolor='black',
                    hatch=pattern[translation[i]], zorder=4,
                    label=translation[i])
    
    print(line)

    # X-axis: workload names
    ax.set_xticks(np.arange(len(dic)))
    ax.set_xticklabels([i for i in dic], rotation=20, ha='right', fontsize=11)

    # Y-axis: speedup range
    top = 2.50
    ttop = top
    min_ = .5
    ax.set_ylim(min_, ttop)
    ax.set_yticks([i for i in np.arange(min_, top+.001, 0.25)])
    ax.set_yticks([i for i in np.arange(min_, top+.001, 0.025)], minor=True)

    # Grid
    ax.yaxis.grid(True, zorder=1, which='major')
    ax.yaxis.grid(True, zorder=1, which='minor', linestyle='--')

    # Baseline at 1.0
    ax.axhline(y=1, color='black', linewidth=1.5)

    # Labels
    ax.set_ylabel("Speedup")

    # Legend: 3 columns for 8 items
    legend = plt.legend(loc=10, bbox_to_anchor=(.5, 1.5),
          ncol=3, edgecolor='black', framealpha=1.0)
    legend.get_frame().set_alpha(None)
    legend.get_frame().set_facecolor((0, 0, 0, 0))

    # Save figure
    plt.tight_layout()
    plt.savefig("fig18.pdf", bbox_inches='tight')
    print("\n✓ Figure 18 saved as fig18.pdf")
    print(f"✓ Plotted {len(to_graph)} configurations across {len(dic)} workloads")
    sys.exit()