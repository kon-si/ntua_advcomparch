#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

total, conditionalNotTaken, conditionalTaken, unconditional, calls, returns = 0, 0, 0, 0, 0, 0
instructions = []
benches = []
outputDir = "../graphs/4-1/"

for benchmark in ["403.gcc", "429.mcf", "434.zeusmp", "436.cactusADM", "445.gobmk", "450.soplex", "456.hmmer", "458.sjeng", "459.GemsFDTD", "462.libquantum", "470.lbm", "471.omnetpp", "473.astar", "483.xalancbmk"]:
	outFile = "../outputs/4-1/" + benchmark + ".cslab_branch_stats.out"
	fp = open(outFile)
	benches.append(benchmark)

	line = fp.readline()
	while line:
		line = line.strip()
		tokens = line.split()
		if line.startswith("Total Instructions:"):
			total = float(tokens[2])
		elif line.startswith("Total-Branches"):
			totalBranches = float(tokens[1])
		elif line.startswith("Conditional-Taken-Branches:"):
			conditionalTaken = float(tokens[1])
		elif line.startswith("Conditional-NotTaken"):
			conditionalNotTaken = float(tokens[1])
		elif line.startswith("Unconditional-Branches"):
			unconditional = float(tokens[1])
		elif line.startswith("Calls"):
			calls = float(tokens[1])
		elif line.startswith("Returns"):
			returns = float(tokens[1])
		line = fp.readline()

	conditionalTaken = (conditionalTaken / totalBranches) * 100
	conditionalNotTaken = (conditionalNotTaken / totalBranches) * 100
	unconditional = (unconditional / totalBranches) * 100
	calls = (calls / totalBranches) * 100
	returns = (returns / totalBranches) * 100
	instructions.append(total)

	labels = ['Conditional Branch-Taken: ' + "{:.2f}".format(conditionalTaken) + '%',
        'Conditional Branch-NotTaken: ' + "{:.2f}".format(conditionalNotTaken) + '%',
        'Unconditional Branch: ' + "{:.2f}".format(unconditional) + '%',
        'Function Calls: ' + "{:.2f}".format(calls) + '%',
        'Function Returns: ' + "{:.2f}".format(returns) + '%']

	sizes = [conditionalTaken, conditionalNotTaken, unconditional, calls, returns]

	fig = plt.figure()
	ax = plt.subplot(111)
	plt.axis('equal')

	radius = 1 
	wedges, texts = plt.pie(sizes, radius=radius, wedgeprops=dict(width=0.4), startangle=180, colors = ['#0392CF', '#EE4035', '#7BC043', '#F37736', '#ffe662'])
	bbox_props = dict(boxstyle="square,pad=0.1", fc="w", ec="k", lw=0.72)
	kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")

	for i, p in enumerate(wedges):
		ang = (p.theta2 - p.theta1)/2. + p.theta1
		y = radius*np.sin(np.deg2rad(ang))
		x = radius*np.cos(np.deg2rad(ang))
		horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
		connectionstyle = "angle,angleA=0,angleB={}".format(ang)
		kw["arrowprops"].update({"connectionstyle": connectionstyle})
	
	percentage = float(totalBranches)/total*100
	stats = benchmark + '\nInstruction Count: ' + str(int(total)) + '\nBranch Instruction Count: ' + str(int(totalBranches)) + " ({:.2f}% ".format(percentage)  + "of the Instruction Count)"
	box = ax.get_position()
	ax.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0.5))
	plt.title(stats, fontsize=12)
	plt.savefig(outputDir + benchmark + '.png', bbox_inches="tight", frame=True, pad_inches=0.1)
	
plt.figure()
fig, ax = plt.subplots()
ax.grid(axis='x')
ax.set_axisbelow(True)
matplotlib.axes.Axes.ticklabel_format(ax, axis='x', style='sci', useMathText=True)
y_pos = np.arange(len(benches))
matplotlib.axes.Axes.tick_params(ax, colors='k')
p = ax.barh(y_pos, instructions, height=0.4, align='center', color='#0392CF')
ax.set_yticks(y_pos)
ax.set_yticklabels(benches)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Number of Instructions', color='k')
ax.set_title('Instruction Count', color='k')
plt.savefig(outputDir + "total.png",bbox_inches="tight", frame=True, pad_inches=0.1)