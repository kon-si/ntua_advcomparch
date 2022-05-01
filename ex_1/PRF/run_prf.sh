#!/bin/bash

PARSEC_PATH=/data/advcomparch/parsec-3.0
PIN_EXE=/data/advcomparch/pin-3.22-98547-g7a303a835-gcc-linux/pin
PIN_TOOL=/data/advcomparch/advcomparch-ex1-helpcode/pintool/obj-intel64/simulator.so

CMDS_FILE=./cmds_simlarge.txt
outDir="/data/advcomparch/advcomparch-ex1-helpcode/PRF/outputs/"

export LD_LIBRARY_PATH=$PARSEC_PATH/pkgs/libs/hooks/inst/amd64-linux.gcc-serial/lib/

## Number of Blocks
CONFS="1 2 4 8 16 32 64"

L1size=32
L1assoc=8
L1bsize=64
L2size=1024
L2assoc=8
L2bsize=128
TLBe=64
TLBp=4096
TLBa=4

BENCHMARKS="blackscholes bodytrack canneal fluidanimate freqmine rtview swaptions streamcluster"

for BENCH in $BENCHMARKS; do
	cmd=$(cat ${CMDS_FILE} | grep "$BENCH")
for conf in $CONFS; do
	## Get parameter
    	L2prf=$(echo $conf)

	outFile=$(printf "%s.dcache_cslab.PRF_%02d.out" $BENCH ${L2prf})
	outFile="$outDir$outFile"

	pin_cmd="$PIN_EXE -t $PIN_TOOL -o $outFile -L1c ${L1size} -L1a ${L1assoc} -L1b ${L1bsize} -L2c ${L2size} -L2a ${L2assoc} -L2b ${L2bsize} -TLBe ${TLBe} -TLBp ${TLBp} -TLBa ${TLBa} -L2prf ${L2prf} -- $cmd"
	time $pin_cmd
done
done
