#!/bin/bash

ccr="0.25 0.5 1"
deadline="110 120"
processor="2 4"
bus="1 2"


for c in $ccr
do
	for d in $deadline
	do
		for p in $processor
		do
			for b in $bus
			do
#				inputFile="input_graph4_ccr_${c}.txt"
				inputFile="input_graph4_ccr_${c}_deadline_100_processor_${p}_bus_${b}.txt"
				outputFile="input_graph4_ccr_${c}_deadline_${d}_processor_${p}_bus_${b}.txt"
				cp $inputFile $outputFile
#				echo $inputFile
#				echo $outputFile
			done
		done
	done
done

