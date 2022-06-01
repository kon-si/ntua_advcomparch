#!/bin/bash

PIN_EXE=/home/konsi/advcomparch/pin-3.22-98547-g7a303a835-gcc-linux/pin
PIN_TOOL=/home/konsi/advcomparch/advcomparch-22-ex2-helpcode/pintool/obj-intel64/cslab_branch.so
outDir="/home/konsi/advcomparch/advcomparch-22-ex2-helpcode/outputs/4-4"

BENCHMARKS="403.gcc 429.mcf 434.zeusmp 436.cactusADM 445.gobmk 450.soplex 456.hmmer 458.sjeng 459.GemsFDTD 462.libquantum 470.lbm 471.omnetpp 473.astar 483.xalancbmk"
for BENCH in $BENCHMARKS; do
	cd ../spec_execs_train_inputs/$BENCH

	line=$(cat speccmds.cmd)
	stdout_file=$(echo $line | cut -d' ' -f2)
	stderr_file=$(echo $line | cut -d' ' -f4)
	cmd=$(echo $line | cut -d' ' -f5-)

	pinOutFile="$outDir/${BENCH}.cslab_branch.out"
	pin_cmd="$PIN_EXE -t $PIN_TOOL -o $pinOutFile -- $cmd 1> $stdout_file 2> $stderr_file"
	echo "PIN_CMD: $pin_cmd"
	/bin/bash -c "time $pin_cmd"

	cd ../../scripts
done