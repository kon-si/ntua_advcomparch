#!/bin/bash

PARSEC_PATH=/data/advcomparch/parsec-3.0
PIN_EXE=/data/advcomparch/pin-3.22-98547-g7a303a835-gcc-linux/pin
PIN_TOOL=/data/advcomparch/advcomparch-ex1-helpcode/pintool/obj-intel64/simulator.so

CMDS_FILE=./cmds_simlarge.txt
outDir="/data/advcomparch/advcomparch-ex1-helpcode/L2/outputs/"

export LD_LIBRARY_PATH=$PARSEC_PATH/pkgs/libs/hooks/inst/amd64-linux.gcc-serial/lib/

## Triples of <cache_size>_<associativity>_<block_size>
CONFS="512_8_64 512_8_128 512_8_256 1024_8_64 1024_8_128 1024_8_256 1024_16_64 1024_16_128 1024_16_256 2048_16_64 2048_16_128 2048_16_256"

L1size=32
L1assoc=8
L1bsize=64
TLBe=64
TLBp=4096
TLBa=4
L2prf=0

BENCHMARKS="blackscholes bodytrack canneal fluidanimate freqmine rtview swaptions streamcluster"

for BENCH in $BENCHMARKS; do
	cmd=$(cat ${CMDS_FILE} | grep "$BENCH")
for conf in $CONFS; do
	## Get parameters
    L2size=$(echo $conf | cut -d'_' -f1)
    L2assoc=$(echo $conf | cut -d'_' -f2)
    L2bsize=$(echo $conf | cut -d'_' -f3)

	outFile=$(printf "%s.dcache_cslab.L2_%04d_%02d_%03d.out" $BENCH ${L2size} ${L2assoc} ${L2bsize})
	outFile="$outDir$outFile"

	pin_cmd="$PIN_EXE -t $PIN_TOOL -o $outFile -L1c ${L1size} -L1a ${L1assoc} -L1b ${L1bsize} -L2c ${L2size} -L2a ${L2assoc} -L2b ${L2bsize} -TLBe ${TLBe} -TLBp ${TLBp} -TLBa ${TLBa} -L2prf ${L2prf} -- $cmd"
	time $pin_cmd
done
done