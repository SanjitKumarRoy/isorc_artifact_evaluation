#!/bin/bash

rm ./outputFiles/*

echo -e "InputFile\tTotalNodes\t#TaskNodes\t#MessageNodes\t#Processors\t#Buses\tCCR\tDeadline\tOptimalScheduleLength\tExecutionTime(second)\n" >>./outputFiles/output.txt

ccr="0.25 0.5 0.75"
deadline="100 110 120"    ## Deadline is in percentage of actual schedule length.##
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
				if [ $c = "0.75" -a $p = "4" -a $b = 1 ]
				then
					inputFile="./inputFiles/input_graph4_ccr_${c}_deadline_${d}_processor_${p}_bus_${b}.txt"
					outputFile="./outputFiles/output_graph4_ccr_${c}_deadline_${d}_processor_${p}_bus_${b}.txt"
					echo "ILP2 is running on graph $inputFile"
#					./ILP2.py $inputFile $outputFile 
				else
					inputFile="./inputFiles/input_graph4_ccr_${c}_deadline_${d}_processor_${p}_bus_${b}.txt"
					outputFile="./outputFiles/output_graph4_ccr_${c}_deadline_${d}_processor_${p}_bus_${b}.txt"
					echo "ILP2 is running on graph $inputFile"
					./ILP2.py $inputFile $outputFile 
				fi
			done
		done
	done
done

echo -e "\n---------------------------------------------------------------------------------------------------\n"
echo -e "\t\t\t\t\t OUTPUT \t\t\t"
echo -e "\n---------------------------------------------------------------------------------------------------\n"
cat ./outputFiles/output.txt
echo -e "\n---------------------------------------------------------------------------------------------------\n"
