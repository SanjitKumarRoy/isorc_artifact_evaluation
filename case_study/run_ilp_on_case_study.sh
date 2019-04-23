#!/bin/bash

rm ./outputFiles/*

#echo -e "ILP:\tInputFile\tTotalNode\t#taskNode\t#messageNode\tCCR\tDeadline\tOptimalScheduleLength\tExecutionTime(second)\n" >>./outputFiles/output.txt

inputFile="./inputFiles/case_study.txt"
outputFileILP2="./outputFiles/case_study_ILP2.txt"

##ILP2##
./ILP2.py $inputFile $outputFileILP2
numberOfConstraint=`cat ./problem.lp | grep -i objective | sed 's/#/\t/g' | sed 's/:/\t/g' | awk -t '{print $2}'`; numberOfConstraint=`expr $numberOfConstraint + 1`;
echo -e "Number of Constraints = $numberOfConstraint \n" >> $outputFileILP2

echo -e "\n---------------------------------------------------------------------------------------------------\n"
echo -e "\t\t\t\t\t OUTPUT \t\t\t"
echo -e "\n---------------------------------------------------------------------------------------------------\n"
echo -e "################## Output of ILP2 ##################"
cat ./outputFiles/case_study_ILP2.txt
echo -e "\n---------------------------------------------------------------------------------------------------\n"
