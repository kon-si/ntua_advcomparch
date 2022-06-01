#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

predictors_to_plot = [ "  BTB-" ]
outputDir = "../graphs/4-3/"

for benchmark in ["403.gcc", "429.mcf", "434.zeusmp", "436.cactusADM", "445.gobmk", "450.soplex", "456.hmmer", "458.sjeng", "459.GemsFDTD", "462.libquantum", "470.lbm", "471.omnetpp", "473.astar", "483.xalancbmk"]:
	outFile = "../outputs/4-3/" + benchmark + ".cslab_branch.out"
	fp = open(outFile)

	x_Axis = []
	mpki_Axis1 = []
	mpki_Axis2 = []

	line = fp.readline()
	while line:
		tokens = line.split()
		if line.startswith("Total Instructions:"):
			total_ins = int(tokens[2])
		else:
			for pred_prefix in predictors_to_plot:
				if line.startswith(pred_prefix):
					predictor_string = tokens[0].split(':')[0]
					x_Axis.append(predictor_string)
					val = int(tokens[2]) / (total_ins / 1000.0)
					mpki_Axis1.append(val)
					val = int(tokens[4]) / (total_ins/1000.0)
					mpki_Axis2.append(val)
		line = fp.readline()

	fig, ax1 = plt.subplots()
	ax1.grid(True)

	xAx = np.arange(len(x_Axis))
	ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
	ax1.set_xticklabels(x_Axis, rotation=25)
	ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
	ax1.set_ylim(min(mpki_Axis1) - 0.05 * min(mpki_Axis1), max(mpki_Axis1) + 0.05 * max(mpki_Axis1))
	ax1.set_ylabel("Directions MPKI\n")
	line1 = ax1.plot(mpki_Axis1, label="Directions MPKI", color="#0392CF",marker='x')
	
	ax2 = ax1.twinx()
	ax2.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
	ax2.set_xticklabels(x_Axis, rotation=45)
	ax2.set_xlim(-0.5, len(x_Axis) - 0.5)
	ax2.set_ylim(min(mpki_Axis2) - 0.05 * min(mpki_Axis2), max(mpki_Axis2) + 0.05 * max(mpki_Axis2))
	ax2.set_ylabel("\nTarget MPKI")
	if benchmark == "470.lbm" or benchmark == "473.astar":
		ax2.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: '{:.7f}'.format(x)))
	line2 = ax2.plot(mpki_Axis2, label="Target MPKI", color="green",marker='o')
	
	lns = line1 + line2
	labs = [l.get_label() for l in lns]
	lgd = plt.legend(lns, labs)
	lgd.draw_frame(False)
	plt.title(benchmark + " MPKI")
	plt.savefig(outputDir + benchmark + '.png', bbox_inches="tight", frame=True, pad_inches=0.1)