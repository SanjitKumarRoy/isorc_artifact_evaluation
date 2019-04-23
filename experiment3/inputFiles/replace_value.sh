#!/bin/bash

ccr="0.25 0.5 1"
deadline="100 125 150"
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
				inputFile="input_graph4_ccr_${c}_deadline_${d}_processor_${p}_bus_${b}.txt"
				### Replace value for #processor and #bus.###
#				sed -i "1s/4/$p/" $inputFile
#				sed -i "2s/1/$b/" $inputFile

				###Print line 1 and 2 of the given file.###
				echo -e "\n$inputFile"
				cat $inputFile | sed -n "1,2p"
			done
		done
	done
done

