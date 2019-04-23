#!/bin/bash

rm ./outputFiles/*

echo -e "InputFile\tTotalNodes\t#TaskNodes\t#MessageNodes\t#Processors\t#Buses\tCCR\tDeadline\tOptimalScheduleLength\tExecutionTime(second)\tNumberOfConstraint\n" >>./outputFiles/output_ILP1.txt
echo -e "InputFile\tTotalNodes\t#TaskNodes\t#MessageNodes\t#Processors\t#Buses\tCCR\tDeadline\tOptimalScheduleLength\tExecutionTime(second)\tNumberOfConstraint\n" >>./outputFiles/output_ILP2.txt


for i in `seq 1 6`
do
	inputFile="./inputFiles/ptg$i.txt"
	outputFileILP1="./outputFiles/ptg${i}_ILP1.txt"
	outputFileILP2="./outputFiles/ptg${i}_ILP2.txt"

	##ILP1##
	echo "ILP1 is running on $inputFile" 
	./ILP1.py $inputFile $outputFileILP1 
	numberOfConstraint=`cat ./problem.lp | grep -i objective | sed 's/#/\t/g' | sed 's/:/\t/g' | awk -t '{print $2}'`
	numberOfConstraint=`expr $numberOfConstraint + 1`
	echo -e "Number of Constraints = $numberOfConstraint \n" >> $outputFileILP1
	echo -e "\t$numberOfConstraint\n" >> ./outputFiles/output_ILP1.txt

	##ILP2##
	echo "ILP2 is running on $inputFile" 
	./ILP2.py $inputFile $outputFileILP2
	numberOfConstraint=`cat ./problem.lp | grep -i objective | sed 's/#/\t/g' | sed 's/:/\t/g' | awk -t '{print $2}'`
	numberOfConstraint=`expr $numberOfConstraint + 1`
	echo -e "Number of Constraints = $numberOfConstraint \n" >> $outputFileILP2
	echo -e "\t$numberOfConstraint\n" >> ./outputFiles/output_ILP2.txt

	echo
done

#echo -e "See the output results in files \"./outputFiles/output_ILP1.txt\" and \"./outputFiles/output_ILP2.txt\""


echo -e "\n---------------------------------------------------------------------------------------------------\n"
echo -e "\t\t\t\t\t OUTPUT \t\t\t"
echo -e "\n---------------------------------------------------------------------------------------------------\n"
echo -e "################## Output of ILP1 ##################"
cat ./outputFiles/output_ILP1.txt
echo -e "\n---------------------------------------------------------------------------------------------------\n"
echo -e "################## Output of ILP2 ##################"
cat ./outputFiles/output_ILP2.txt
echo -e "\n---------------------------------------------------------------------------------------------------\n"
