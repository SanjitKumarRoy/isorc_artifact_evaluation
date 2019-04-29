# ISORC'19 Artifact Evaluation
### Paper Title: Optimal Scheduling of Precedence-constrained Task Graphs on Heterogeneous Distributed Systems with Shared Buses
### Author: Sanjit Kumar Roy, Sayani Sinha, Kankana Maji, Rajesh Devaraj and Arnab Sarkar

## A. Artifact Appendix
### A.1 Abstract
In this artifact, we provided all the benchmark PTGs (Precedence Constrained Task Graphs) along with program and shell script to regenerate the output results.

### A.2 Artifact check-list (meta-information)
* **Program:** ILP1.py and ILP2.py

* **Binary:** Source code and shell scripts are available.

* **Data set:** Benchmark PTGs (Precedence Constrained Task Graphs) are taken from various research papers as given in our paper. Data are randomly generated and remain fixed throughout the experiment.

* **Hardware:** Pentium 4 and above, ~4 GB Disk Space, Minimum 1 GB Memory. For additional information please see: <https://www.ibm.com/software/reports/compatibility/clarity-reports/report/html/softwareReqsForProduct?deliverableId=E57328F0919E11E8A5E6A380334DFF95&osPlatform=Linux>

* **Execution:** Automated using shell script.

* **Metrics:** Number of constraints generated, time required to generate a solution by the ILP1 and ILP2, time required in various test scenarios like varying number of nodes, number of processors, number of buses, CCR and deadline.

* **Output:** Schedule, number of constraints, running time.

* **Experiments:** We use six benchmark PTGs from major research papers. The execution and communication times of nodes are randomly generated and appropriately scaled to maintain the CCR.
 
* **How much disk space required (approximately)?:** ~4 GB

* **How much time is needed to prepare workflow (approximately)?:** To install the IBM CPLEX optimizer, it takes ~20 minutes.

* **How much time is needed to complete experiments (approximately)?:** It takes ~2 days to complete all the experiment. The Example, Experiment-1 and Experiment-2 take ~2 hours. Experiment-3 takes ~1 day. The case study takes ~8 hours.
  
* **Publicly available?:** IBM CPLEX optimizer is not publicly available. But source code for out ILP formulation and the data are available on Github: <https://github.com/SanjitKumarRoy/isorc_artifact_evaluation>

### A.3 Description

### A.3.1 How delivered
Our benchmark PTGs, source code, scripts are available on Github: 
<https://github.com/SanjitKumarRoy/isorc_artifact_evaluation>


### A.3.2 Hardware dependencies
All the experiments are carried out on a system having Intel(R) Xeon(R) CPU. 

### A.3.3 Software dependencies
We use IBM CPLEX optimizer version 12.6.2.0 running on Linux Kernel 2.6.32-042stab123.1.

### A.4 Installation
To install the CPLEX optimizer in Ubuntu first get the binary version of the IBM CPLEX optimizer and then run the following commands:
```
$ chmod +x cplex_studioXXX.linux-x86.bin
$ ./cplex_studioXXX.linux-x86.bin
```
where, XXX is the version of the CPLEX optimizer. To install the CPLEX-Python modules on your system, use the script setup.py located in yourCplexhome/python/VERSION/PLATFORM. To run the script use the following command:
```
$ python setup.py install
```
For additional information please see: <https://www.ibm.com/support/knowledgecenter/SSSA5P\_12.8.0/ilog.odms.studio.help/pdf/gscplex.pdf>


### A.5 Experiment workflow
After installation of the IBM CPLEX optimizer, you can run all the experiments using the following command:
```
$ ./run_all_experiment.sh
```
Use following commands to run the example, experiments and case study separately,
```
$ ./run_example.sh
$ ./run_experiment1.sh
$ ./run_experiment2.sh
$ ./run_experiment3.sh
$ ./run_case_study.sh
```

**Output files:**

Example
```
./example/outputFiles/example_ILP1.txt
./example/outputFiles/example_ILP2.txt
```
Experiment-1
```
./experiment1/outputFiles/output_ILP1.txt
./experiment1/outputFiles/output_ILP2.txt
```
Experiment-2
```
./experiment2/outputFiles/output_ILP1.txt
./experiment2/outputFiles/output_ILP2.txt
```
Experiment-3
```
./experiment3/outputFiles/output.txt
```
Case Study
```
./case_study/outputFiles/case_study_ILP2.txt
```

### A.6 Evaluation and expected result
Once the experiments are done the results will be displayed on the screen. Further, you can see the output of the experiments in the above mentioned output files.

### A.7 Experiment customization
Scripts are available to run all the experiments together as well as separately. 

### A.8 Notes
* In the output schedule, the *time step t* is the time between *t - 1* and *t* (where *t = 1, 2, ...*). For example, let start and finish times of a task in the output schedule are 1 and 7, respectively. In the Gantt chart representation, the start and finish times will be 0 and 7, respectively.

* The IBM CPLEX supports both multithreaded and distributed parallel optimization. The implementation of CPLEX on multiprocessor system will be beneficial in terms of solution speed.

### A.9 Methodology
The artifact of this paper reviewed according to the guidelines at:
<http://ctuning.org/ae/reviewing-20190108.html>