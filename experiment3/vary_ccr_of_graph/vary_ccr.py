#!/usr/bin/python

#####################################################################################
## Author: Sanjit Kumar Roy
## E-Mail: sanjit.it@gmail.com
#######################################
## Description: This program compute execution time for tasks and transmission time for messages as per given CCR (Communication to Computation Ratio).
## Input: #nodes, #task nodes, #message nodes, #processors, #buses and CCR value.
## Output: Execution time for tasks & messages as per #processors, #buses.
#####################################################################################

import random


numberOfNode = 25 
numberOfTaskNodes = 10
numberOfMessageNodes = 15 
numberOfProcessor = 4 
numberOfBus = 2
ccr = 0.25 

outFile = "./graph_ccr_"+str(ccr)+".txt"

## Task execution range and message transmission time.##
tExecutionLow = 5
tExecutionHigh = 15 
mTransmissionLow = 5 
mTransmissionHigh = 15 



## Generate execution time for each node.##
tExecutionTime = []
for i in range(1, numberOfTaskNodes * numberOfProcessor + 1):
    tExecutionTime.append(random.randint(tExecutionLow, tExecutionHigh))

## Generate transmission time for each node.##
mTransmissionTime = []
for i in range(1, numberOfMessageNodes * numberOfBus + 1):
    mTransmissionTime.append(random.randint(mTransmissionLow, mTransmissionHigh))

## Average execution time and transmission time.##
avgExecutionTime = (float(sum(tExecutionTime)) / (numberOfTaskNodes * numberOfProcessor))
avgTransmissionTime = (float(sum(mTransmissionTime)) / (numberOfMessageNodes * numberOfBus))            

## Compute scaling factor for transmission time.##
tempAvgTransmissionTime = avgExecutionTime * ccr
scalingFactor = tempAvgTransmissionTime / float(avgTransmissionTime)

## Scale each transmission time using scaling factor.##
for i in range(0, numberOfMessageNodes * numberOfBus):
    tempValue = mTransmissionTime[i]
    mTransmissionTime[i] = int(round(mTransmissionTime[i] * scalingFactor))

## Verifying modified ccr.##
avgTransmissionTime = (float(sum(mTransmissionTime)) / (numberOfMessageNodes * numberOfBus))            
modifiedCCR = float(avgTransmissionTime) / avgExecutionTime

## Assign valus to tasks and messages.##
op = open(outFile, "w")
op.write("Execution Time:\n")
## For tasks: ##
print "Task Execution Time:", tExecutionTime 
for i in range(1, numberOfTaskNodes + 1):
    op.write(str(i)+" : [")
    for r in range(1, numberOfProcessor + 1):
        selectedIndex = random.choice(range(0, len(tExecutionTime)))
        if r != numberOfProcessor:
            op.write(str(tExecutionTime[selectedIndex])+", ")
        else:
            op.write(str(tExecutionTime[selectedIndex])+"]\n")
        tExecutionTime.remove(tExecutionTime[selectedIndex])
## For messages: ##
print "Message Transmission Time:", mTransmissionTime
for i in range(numberOfTaskNodes + 1, numberOfTaskNodes + numberOfMessageNodes+ 1):
    op.write(str(i)+" : [")
    for r in range(1, numberOfBus + 1):
        selectedIndex = random.choice(range(0, len(mTransmissionTime)))
        if r != numberOfBus:
            op.write(str(mTransmissionTime[selectedIndex])+", ")
        else:
            op.write(str(mTransmissionTime[selectedIndex])+"]\n")
        mTransmissionTime.remove(mTransmissionTime[selectedIndex])

## Write task and message node index.##
## For task nodes index.##
op.write("Task Nodes: [")
for i in range(1, numberOfTaskNodes + 1):
    if i != numberOfTaskNodes:
        op.write(str(i)+", ")
    else:
        op.write(str(i)+"]\n")
## For message node index.##
op.write("Message Nodes: [")
for i in range(numberOfTaskNodes + 1, numberOfTaskNodes + numberOfMessageNodes + 1):
    if i != (numberOfTaskNodes + numberOfMessageNodes):
        op.write(str(i)+", ")
    else:
        op.write(str(i)+"]\n")

op.close()


print "Given CCR =", ccr, "\nModified CCR =", modifiedCCR
print "Average Execution Time =", avgExecutionTime, "\nAverage Transmission Time =", avgTransmissionTime
