#!/bin/bash

ccr="0.75"
deadline="100 110 120"
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
				inputFile="./original_input_files/input_graph4_ccr_${c}.txt"
				outputFile="input_graph4_ccr_${c}_deadline_${d}_processor_${p}_bus_${b}.txt"
				./scale_value_based_on_resource.py $inputFile $outputFile $p $b
#				echo $inputFile
#				echo $outputFile
#				echo $p
#				echo $b
			done
		done
	done
done

