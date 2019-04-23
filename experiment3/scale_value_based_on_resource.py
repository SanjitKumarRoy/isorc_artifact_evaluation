#!/usr/bin/python

############################################################################################################################################
## Author: Sanjit Kumar Roy
## E-mail: sanjit.it@gmail.com
######################################
## Scale value of each taski/message based on number of resources such that each task's/message's average execution/transmission time
## remain same as previous. 
############################################################################################################################################

import sys
import time
import re
from fractions import gcd
import cplex
from cplex.exceptions import CplexError


###Global Variables.###
numberOfProcessor = 0   ##Number of Processor.##
numberOfBus = 0 ##Number of Bus.##
numberOfGraph = 0   ##Number of Graph.##
graphList = []  ##graphList holds all graphs.##


###Graph class to create graph object
class Graph:
    def __init__ (self, graphID, period, numberOfNode, adjacentList, childNodes, parentNodes, executionTime, taskNodes, messageNodes):
        self.graphID = graphID
        self.period = period
        self.numberOfNode = numberOfNode
        self.adjacentList = adjacentList
        self.childNodes = childNodes
        self.parentNodes = parentNodes
        self.executionTime = executionTime
        self.taskNodes = taskNodes
        self.messageNodes = messageNodes
        

    ###Display values of graph.###
    def valuesOfNode(self):
        print "\nGraph", self.graphID
        print "Period = ", self.period 
        print "Number of Nodes =", self.numberOfNode
        print "Adjacent List:"
        for i in self.adjacentList.keys():
            print i, ":", self.adjacentList[i]
        print "Execution Time:"
        for i in self.executionTime.keys():
            print i, ":", self.executionTime[i]
        print "Task Nodes:", self.taskNodes 
        print "Message Nodes:", self.messageNodes
#        print "Parent nodes List:"
#        for i in self.parentNodes.keys():
#            print i, ":", self.parentNodes[i]
#        print "Child nodes List:"
#        for i in self.childNodes.keys():
#            print i, ":", self.childNodes[i]
#        print "Service Levels:"
#        for i in self.serviceLevels.keys():
#            print i, ":", self.serviceLevels[i]


def readGraph(inFileName):
#    inFileName = "./inputFiles/input_graph10.txt"
    inFileObject = open(inFileName, "r")
    ##Read number of Processors.##
    line = inFileObject.readline()
    string = [int(x) for x in re.findall(r"\d+", line)]
    numberOfProcessor = string[0]
    ##Read number of Buses.##
    line = inFileObject.readline()
    string = [int(x) for x in re.findall(r"\d+", line)]
    numberOfBus = string[0]
    ##Read number of Graphs.##
    line = inFileObject.readline()
    string = [int(x) for x in re.findall(r"\d+", line)]
    numberOfGraph = string[0]
    
    for g in range(numberOfGraph):
        ##Skip empty line.##
        line = inFileObject.readline()
        ##Read graph id.##
        line = inFileObject.readline()
        string = [int(x) for x in re.findall(r"\d+", line)]
        graphID = string[0]
        ##Read Period.##
        line = inFileObject.readline()
        string = [int(x) for x in re.findall(r"\d+", line)]
        period = string[0]
        ##Read number of nodes in the graph.##
        line = inFileObject.readline()
        string = [int(x) for x in re.findall(r"\d+", line)]
        numberOfNode = string[0]
        ##Read Adjacent List.##
        line = inFileObject.readline()
        adjacentList = readList(inFileObject, numberOfNode)
        ##Read Execution Time.##
        line = inFileObject.readline()
        executionTime = readList(inFileObject, numberOfNode)
        ##Read task node list.##
        line = inFileObject.readline()
        taskNodes = [int(x) for x in re.findall(r"\d+", line)]
        ##Read message node list.##
        line = inFileObject.readline()
        messageNodes = [int(x) for x in re.findall(r"\d+", line)]

        ##Make parent nodes list.##
        parentNodes = {}
        for i in adjacentList.keys():
            parentNodes[i] = []
        for i in adjacentList.keys():
            for j in adjacentList[i]:
                parentNodes[j].append(i)
        ##Make child nodes list.##
        childNodes = {}
        for i in adjacentList.keys():
            childNodes[i] = []
            for j in adjacentList[i]:
                childNodes[i].append(j)

        ###Create graph object
        graph = Graph(graphID, period, numberOfNode, adjacentList, childNodes, parentNodes, executionTime, taskNodes, messageNodes)
        graphList.append(graph)

    inFileObject.close()

    return numberOfProcessor, numberOfBus, numberOfGraph


###Read multiple lines from file.###
def readList(inFileObject, numberOfNode):
    tempList = {}
    for n in range(numberOfNode):
        line = inFileObject.readline()
        string = [int(x) for x in re.findall(r"\d+", line)]
        i = string[0]
        tempList[i] = []
        for j in string[1:]:
            tempList[i].append(j)

    return tempList



###Scale up execution and transmission time.###
def scaleupTime(numberOfProcessor, numberOfBus):
    graph = graphList[0]

    modifiedExecution = {}
    for i in graph.taskNodes:
        modifiedExecution[i] = []
        avgExecution = sum(graph.executionTime[i]) / (float(len(graph.executionTime[i])))
        tempAvgExecution = 0
        for r in range(0, numberOfProcessor):
            tempAvgExecution = tempAvgExecution + graph.executionTime[i][r]
        tempAvgExecution = tempAvgExecution / (float(numberOfProcessor))
        for r in range(0, numberOfProcessor):
            modifiedExecution[i].append(int(round(graph.executionTime[i][r] * (avgExecution / (float(tempAvgExecution))))))

    for i in graph.messageNodes:
        modifiedExecution[i] = []
        avgExecution = sum(graph.executionTime[i]) / (float(len(graph.executionTime[i])))
        tempAvgExecution = 0
        for r in range(0, numberOfBus):
            tempAvgExecution = tempAvgExecution + graph.executionTime[i][r]
        tempAvgExecution = tempAvgExecution / (float(numberOfBus))
        for r in range(0, numberOfBus):
            modifiedExecution[i].append(int(round(graph.executionTime[i][r] * (avgExecution / (float(tempAvgExecution))))))


    return modifiedExecution



###Write graph details into output file.###
def writeInFile(modifiedExecution, outputFile):
    graph = graphList[0]

    f = open(outputFile, "w")
    f.write("Number of Processor = "+str(numberOfProcessor)+"\n")
    f.write("Number of Bus = "+str(numberOfBus)+"\n")
    f.write("Number of Graph = "+str(numberOfGraph)+"\n")
    f.write("\n")
    f.write("Graph "+str(graph.graphID)+"\n")
    f.write("Period = "+str(graph.period)+"\n")
    f.write("Number of Nodes = "+str(graph.numberOfNode)+"\n")
    f.write("Adjacent List:\n")
    for i in graph.adjacentList.keys():
        f.write(str(i)+" : "+str(graph.adjacentList[i])+"\n")
    f.write("Execution Time:\n")
    for i in graph.executionTime.keys():
        f.write(str(i)+" : "+str(modifiedExecution[i])+"\n")
    f.write("Task Nodes: "+str(graph.taskNodes)+"\n")
    f.write("Message Nodes :"+str(graph.messageNodes)+"\n")

    return 0

##############################################################################

## Input and Output files name. ##
inFile = sys.argv[1]
outFile = sys.argv[2]


## Read graph from file. ##
numberOfProcessor, numberOfBus, numberOfGraph = readGraph(inFile) 

###Display details of the system.##
#print "Number of Processor =", numberOfProcessor
#print "Number of Bus =", numberOfBus
#print "Number of Graph =", numberOfGraph
####Display graph###
#for graph in graphList:
#    graph.valuesOfNode()
#
#
#graph = graphList[0]




numberOfProcessor = int( sys.argv[3])
numberOfBus = int(sys.argv[4])

modifiedExecution = scaleupTime(numberOfProcessor, numberOfBus)
writeInFile(modifiedExecution, outFile)

