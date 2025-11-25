#!/usr/bin/python3
"""
parse_cs.py - Updated for CS683 Project
Parses single.csv and averages by benchmark name
"""
import sys
import numpy as np

# ALL 10 traces from your screenshot
elem = {
    'bwaves': {},
    'gcc': {},
    'gobmk': {},
    'cactusADM': {},
    'GemsFDTD': {},
    'hmmer': {},
    'namd': {},
    'omnetpp': {},
    'sphinx3': {},
    'wrf': {}
}

if len(sys.argv) < 2:
    print("Usage: python3 parse_cs.py <input_csv_file>")
    print("Example: python3 parse_cs.py single.csv")
    sys.exit(1)

try:
    with open(sys.argv[1]) as f:
        raw = f.read().split('\n')
except FileNotFoundError:
    print(f"Error: File '{sys.argv[1]}' not found!")
    sys.exit(1)

# Check if file has data
if len(raw) < 2:
    print("Error: Input file is empty or has insufficient data")
    sys.exit(1)

# Get header (configuration names)
head = raw[1].split(';')
print(f"DEBUG: Found {len(head)} columns in header", file=sys.stderr)

# Process data rows
processed_count = 0
for i in raw[2:-1]:
    if not i.strip():  # Skip empty lines
        continue
        
    name = ''
    for iidx, ii in enumerate(i.split(';')[:-1]):
        if iidx == 0:
            # Extract benchmark name (part before first _)
            name = ii.split('_')[0]
            print(f"DEBUG: Processing trace: {ii} -> benchmark: {name}", file=sys.stderr)
            continue
        
        # Skip if trace name not in our dict
        if name not in elem:
            print(f"DEBUG: Skipping unknown benchmark: {name}", file=sys.stderr)
            continue
        
        # Store value for this configuration
        if iidx not in elem[name]:
            elem[name][iidx] = []
        
        try:
            elem[name][iidx].append(float(ii))
        except ValueError:
            print(f"DEBUG: Could not convert '{ii}' to float", file=sys.stderr)
            continue
    
    if name in elem:
        processed_count += 1

print(f"DEBUG: Processed {processed_count} traces", file=sys.stderr)

# Print header
print(raw[1])

# Print averaged data for each benchmark
output_count = 0
for i in sorted(elem.keys()):
    if len(elem[i]) > 0:
        string = "{};".format(i.capitalize())
        for ii in sorted(elem[i].keys()):
            avg = np.average(elem[i][ii])
            string = "{}{:.6f};".format(string, avg)
        print(string)
        output_count += 1

print(f"DEBUG: Output {output_count} benchmarks", file=sys.stderr)

if output_count == 0:
    print("\nWARNING: No data was output! Check that:", file=sys.stderr)
    print("  1. Input CSV has correct format", file=sys.stderr)
    print("  2. Trace names start with: bwaves, gcc, gobmk, cactusADM, GemsFDTD, hmmer, namd, omnetpp, sphinx3, wrf", file=sys.stderr)