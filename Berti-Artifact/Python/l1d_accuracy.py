#!/usr/bin/python3
"""
fig10.py - L1D Prefetch Accuracy (Timely vs Late)
Updated for CS683 project - SPEC only, GAP removed
"""
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from scipy.stats import gmean

if __name__ == "__main__":
    rc('font', size=13)
    
    torder = ['IP-stride', 'MLOP', 'IPCP', 'Berti']
    
    time_a = {
        'IP-stride': [],
        'Berti': [],
        'IPCP': [],
        'MLOP': [],
    }
    
    late_a = {
        'IP-stride': [],
        'Berti': [],
        'IPCP': [],
        'MLOP': [],
    }
    
    translation = {
        'ip_stride+no': 'IP-stride',
        'mlop_dpc3+no': 'MLOP',
        'ipcp_isca2020+no': 'IPCP',
        'vberti+no': 'Berti'
    }
    
    bench = []
    
    # Read input CSV
    with open(sys.argv[1]) as f:
        raw = f.read().split('\n')
        
        for i in raw[:-1]:
            splitted = i.split(';')
            
            if len(splitted) == 1:
                bench.append(splitted[0])
            else:
                pref = "{}+{}".format(splitted[0], splitted[1])
                
                if pref not in translation:
                    continue
                
                time_a[translation[pref]].append(float(splitted[3]) * 100)
                late_a[translation[pref]].append(float(splitted[4]) * 100)
    
    # Create single plot
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # Collect data for SPEC17-MemInt
    x_timely = []
    x_late = []
    
    line = "SPEC17-MemInt"
    for prefetcher in torder:
        x_timely.append(time_a[prefetcher][0])
        x_late.append(late_a[prefetcher][0])
        line += "; {} (Timely: {:.1f}%, Late: {:.1f}%)".format(
            prefetcher, time_a[prefetcher][0], late_a[prefetcher][0])
    
    # Plot stacked bars
    ax.bar(np.arange(len(x_timely)), x_timely, color='gray', 
           edgecolor='black', label="Timely", zorder=3)
    ax.bar(np.arange(len(x_timely)), x_late, bottom=x_timely, 
           color='black', edgecolor='black', label="Late", zorder=2)
    
    # Styling
    ax.set_yticks([i for i in range(0, 101, 10)])
    ax.set_yticks([i for i in range(0, 101, 5)], minor=True)
    ax.set_ylim(0, 100)
    ax.set_xticks(np.arange(len(x_timely)))
    ax.set_xticklabels(torder, rotation=25, ha='right')
    ax.set_ylabel("L1D Prefetch Accuracy")
    ax.set_xlabel("(a) SPEC17-MemInt")
    
    # Grid
    ax.yaxis.grid(True, zorder=1, which='major')
    ax.yaxis.grid(True, zorder=1, which='minor', linestyle='--')
    
    # Print data
    print(line)
    
    # Legend at top
    legend = plt.legend(loc=9, bbox_to_anchor=(0.5, 1.15),
                       ncol=2, edgecolor='black', framealpha=1.0)
    
    plt.tight_layout()
    plt.savefig("fig10.pdf", bbox_inches='tight')
    print("\n✓ Figure 10 saved (SPEC only)")