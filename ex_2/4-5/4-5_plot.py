#!/usr/bin/env python

import matplotlib
from matplotlib import colors
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

outputDir = "../graphs/4-5/"
predictors_to_plot = [ "  Static", "  BTFNT", "  Pentium", "  Nbit", "  Local", "  Global", "  Tournament", "  ALPHA"]

def plot(outputDir, benchname, axes, sortit=True):
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.grid(axis='x')
    ax.set_axisbelow(True)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    percentage = [str(x) for x in np.arange(0, 160, 10)]
    bar_thickness = 0.6
    combos_count = len(axes)
    y_pos = (combos_count+ 1) * bar_thickness * np.arange(len(benches))
    matplotlib.axes.Axes.tick_params(ax, colors='k')

    counter = 0
    handles = []
    labels = []
    maxval = -1

    if sortit:
        axes = sorted(axes, key=lambda tup: tup[1], reverse=True)
    colors = ['#0392CF', '#EE4035', '#ff878d','#006fa3', '#7BC043', '#F37736', '#af3579','#ffe662',  '#ff878d','#9391c4',  '#0392CF', '#EE4035', '#7BC043', '#F37736', '#af3579','#ffe662',  '#9391c4']
    ind = 0
    for (combo, val) in axes:
        p = ax.barh(y_pos + bar_thickness*counter, np.array(val), height=0.7*bar_thickness, align='center', color = colors[ind])
        labels.append('[ MPKI: ' + "{:.3f}".format(val)+ ' ]' + combo)
        handles.append(p)
        maxval = max(maxval, val)
        plt.text(x = val + 1 , y = -0.05 + counter *bar_thickness , s = "{:.3f}".format(val), size = 10)
        counter += 1
        ind += 1

    ax.set_yticks(y_pos + 0.5*combos_count*bar_thickness)
    ax.set_yticklabels([])
    ax.set_ylim(-0.5, bar_thickness*(combos_count+1)*len(benches))
    ax.set_xlim([0, maxval])
    print(maxval)
    percentage = [str(x) for x in np.arange(0, maxval + 10, 10)]
    x_pos = np.arange(len(percentage))
    ax.set_xticks(10*x_pos)
    ax.set_xticklabels(percentage)
    ax.legend(handles[::-1], labels[::-1], loc='upper center', bbox_to_anchor=(0.5, -0.09),
          frameon=False, ncol=1)
    plt.xlabel('MPKI')
    plt.ylabel('Predictors')
    plt.title(benchname + " MPKI comparison with different predictors")
    plt.savefig(outputDir + benchname + '.png', bbox_inches="tight", frame=True, pad_inches=0.1)

axes = dict()
for benchmark in ["403.gcc", "429.mcf", "434.zeusmp", "436.cactusADM", "445.gobmk", "450.soplex", "456.hmmer", "458.sjeng", "459.GemsFDTD", "462.libquantum", "470.lbm", "471.omnetpp", "473.astar", "483.xalancbmk"]:
    outFile = "../outputs/4-5/" + benchmark + ".cslab_branch.out"
    fp = open(outFile)
    curaxes = []
    benches = []

    line = fp.readline()
    while line:
        if line.startswith("Total Instructions"):
            total_instructions = float(line.split(":")[1])
        for pred_prefix in predictors_to_plot:
            if line.startswith(pred_prefix):
                if benchmark not in benches:
                    benches.append(benchmark)
                tokens = line.split(":")
                combo = tokens[0]
                tokens = tokens[1].split()
                correct = float(tokens[0])
                incorrect = float(tokens[1])
                missprediction_rate = incorrect / total_instructions * 1000
                curaxes.append((combo, missprediction_rate))
                axes.setdefault(combo, []).append(missprediction_rate)
        line = fp.readline()

    plot(outputDir, benchmark, curaxes)
    fp.close()