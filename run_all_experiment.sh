#!/bin/bash

## This program will run all the programs related to the example, experiments and case study as given in our paper. ##


## Run Example ##
## Expected running time is 30 seconds ##
echo -e "******************************************** Example *************************************"
cd ./example/
./run_ilp_on_example.sh
cd -

## Expected running time is 1.5 hours ##
## Run Experiment-1 ##
echo -e "\n\n\n\n******************************************** Experiment-1 *************************************"
cd ./experiment1/
./run_ilp_on_ptg.sh
cd -


## Expected running time is 2 hours ##
## Run Experiment-2 ##
echo -e "\n\n\n\n******************************************** Experiment-2 *************************************"
cd ./experiment2/
./run_ilp_on_ptg.sh
cd -

## Expected running time is 1.5 days ##
## Run Experiment-3 ##
echo -e "\n\n\n\n******************************************** Experiment-3 *************************************"
cd ./experiment3/
./run_ilp_vary_ccr_processor_bus.sh
cd -

## Expected running time is 7 to 8 hours ##
## Run Case Study ##
echo -e "\n\n\n\n******************************************** Case Study *************************************"
cd ./case_study/
./run_ilp_on_case_study.sh
cd -
