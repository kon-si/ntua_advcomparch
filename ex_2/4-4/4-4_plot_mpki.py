#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

predictors_to_plot = [ "RAS (4 e", "RAS (8", "RAS (16", "RAS (32", "RAS (48", "RAS (64"]
outputDir = "../graphs/4-4/"

mpki_Axis = []
mpki_dict = {}

for benchmark in ["403.gcc", "429.mcf", "434.zeusmp", "436.cactusADM", "445.gobmk", "450.soplex", "456.hmmer", "458.sjeng", "459.GemsFDTD", "462.libquantum", "470.lbm", "471.omnetpp", "473.astar", "483.xalancbmk"]:
	outFile = "../outputs/4-4/" + benchmark + ".cslab_branch.out"
	fp = open(outFile)

	x_Axis = []
	mpki_Axis = []

	line = fp.readline()
	while line:
		tokens = line.split()
		if line.startswith("Total Instructions:"):
			total_ins = int(tokens[2])
		else:
			for pred_prefix in predictors_to_plot:
				if line.startswith(pred_prefix):
					predictor_string = tokens[1].split('(')[1]
					correct_predictions = int(tokens[3])
					incorrect_predictions = int(tokens[4])
					x_Axis.append(predictor_string)
					val = incorrect_predictions / (total_ins / 1000.0)
					mpki_Axis.append(val)
					mpki_dict.setdefault(predictor_string, []).append(val)
		line = fp.readline()

	fig, ax1 = plt.subplots()
	ax1.grid(True)

	xAx = np.arange(len(x_Axis))
	ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
	ax1.set_xticklabels(x_Axis, rotation=25)
	ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
	ax1.set_ylim(min(mpki_Axis) - 0.05, max(mpki_Axis) + 0.05)
	ax1.set_ylabel("$MPKI$")
	ax1.set_xlabel("$RAS$ $Entries$")
	line1 = ax1.plot(mpki_Axis, label="mpki", color="#0392CF",marker='x')
	plt.title(benchmark + " MPKI")
	plt.savefig(outputDir + benchmark + '.png', bbox_inches="tight", frame=True, pad_inches=0.1)