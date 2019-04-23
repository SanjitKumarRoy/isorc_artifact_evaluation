#!/usr/bin/python

############################################################################################################################################
## Author: Sanjit Kumar Roy
## E-mail: sanjit.it@gmail.com
######################################
## Title: (Single DAG, Heterogeneous processors and buses, Optimal Schedule, Transmission time 0, if both tasks scheduled on same processor.) ILP for finding optimal schedule of a given task graph (DAG) where nodes represent tasks and messages. The system consists of a set of heterogeneous processors and heterogeneous buses.

## Assumption: A message node has only one parent and one child task node. The source and sink nodes of DAG are task node. If both parent and child task nodes of a message nodes get scheduled on same processor, then the message node is discarded.

######################################
## N.B: ASAP-ALAP based formulation i.e., [ASAP-ALAP] of node is used for binary 'x' variables.
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
hyperPeriod = 0 ##Hyperperiod of applications (DAGs).
graphList = []  ##graphList holds all graphs.##


###Graph class to create graph object
class Graph:
    def __init__ (self, graphID, period, numberOfNode, adjacentList, childNodes, parentNodes, executionTime, taskNodes, messageNodes, asap, alap):
        self.graphID = graphID
        self.period = period
        self.numberOfNode = numberOfNode
        self.adjacentList = adjacentList
        self.childNodes = childNodes
        self.parentNodes = parentNodes
        self.executionTime = executionTime
        self.taskNodes = taskNodes
        self.messageNodes = messageNodes
        self.asap = asap
        self.alap = alap
        
        self.numberOfInstance = 0

    ###Display values of graph.###
    def valuesOfNode(self):
        print "\nGraph:", self.graphID
        print "Period = ", self.period 
        print "Number of Node:", self.numberOfNode
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
        print "ASAP time, ALAP time:"
        for i in self.adjacentList.keys():
            print i, ": [",self.asap[i],"-",self.alap[i],"]"



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
#        ##Read Reward.##
#        line = inFileObject.readline()
#        rewards = readList(inFileObject, numberOfNode)
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

        asap, alap = computeAsapAlap(period, adjacentList, executionTime, taskNodes, messageNodes, parentNodes, childNodes)

        ###Create graph object
        graph = Graph(graphID, period, numberOfNode, adjacentList, childNodes, parentNodes, executionTime, taskNodes, messageNodes, asap, alap)
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


###Compute ASAP and ALAP of each task and message node.###
def computeAsapAlap(period, adjacentList, executionTime, taskNodes, messageNodes, parentNodes, childNodes):
    ##Compute asap alap of each task nodes and message nodes.##
    ##The asap and alap of tasks nodes are calculated after removing message nodes from the task graph. The asap and alap of message nodes are calculated as, asap: sum of execution time and asap time of parent task node, alap: difference of execution time of message node and alap time of child task node.##

    ##Compute ASAP time of task and message nodes.##
    ##Compute in degree of each node.## 
    inDegree = {}
    for i in adjacentList.keys():
        inDegree[i] = len(parentNodes[i]) 
    asap = {}
    ##Initially assign asap time 1 to all nodes.##
    for i in adjacentList.keys():
        asap[i] = 1 
    while(len(inDegree.keys()) > 0):
        for i in inDegree.keys():
            if inDegree[i] == 0:
                for j in adjacentList[i]:
                    inDegree[j] = inDegree[j] - 1
                    if i in taskNodes:
                        if asap[j] < asap[i] + min(executionTime[i]):
                            asap[j] = asap[i] + min(executionTime[i])
                    else:
                        if asap[j] < asap[i]:
                            asap[j] = asap[i] 
                del inDegree[i]
        if not inDegree.keys():
            break

    ##Compute ALAP time of task and message nodes.##
    ##Compute out degree of each node.## 
    outDegree = {}
    for i in adjacentList.keys():
        outDegree[i] = len(adjacentList[i])
    alap = {}
    ##Initially assign difference of period and execution time as the alap time to all nodes.##
    for i in adjacentList.keys():
        alap[i] = period - min(executionTime[i]) + 1
    while(len(outDegree.keys()) > 0):
        for i in outDegree.keys():
            if outDegree[i] == 0:
                for j in parentNodes[i]:
                    outDegree[j] = outDegree[j] - 1
                    if i in taskNodes:
                        if alap[j] > alap[i] - min(executionTime[j]):
                            alap[j] = alap[i] - min(executionTime[j])
                    else:
                        if alap[j] > (alap[i] + min(executionTime[i])) - min(executionTime[j]):
                            alap[j] = (alap[i] + min(executionTime[i])) - min(executionTime[j])
                del outDegree[i]
        if not outDegree.keys():
            break

    return asap, alap


###Calculate hyperperiod.###
def calculateHyperperiod(graphList):
    periods = []
    for graph in graphList:
        periods.append(graph.period)
    hyperPeriod = periods[0]
    for n in periods[1:]:
        hyperPeriod = (hyperPeriod * n) / gcd(hyperPeriod, n)
    
    for graph in graphList:
        graph.numberOfInstance = hyperPeriod / graph.period

    return hyperPeriod








###Populate the cplex problem by row.###
def populatebyrow(prob, graphList):
    
    ###########################################################################################################
    ###Make variables list.###

    constantC = 10000

    xVariables = []
    uVariables = []
    yVariables = []
    
    ###Find 'X' variable list.###
    for graph in graphList:
        g = graph.graphID
        ##'X' variables for Task Nodes.##
        for i in graph.taskNodes:
            for r in range(1, numberOfProcessor + 1):
                for t in range(graph.asap[i], graph.alap[i] + 1):
                    myString = "x"+(str)(i)+","+(str)(r)+","+(str)(t)
                    xVariables.append(myString)
    
        ##'X' variables for Message Nodes.##
        for i in graph.messageNodes:
            for r in range(1, numberOfBus + 1):
                for t in range(graph.asap[i], graph.alap[i] + 1):
                    myString = "x"+(str)(i)+","+(str)(r)+","+(str)(t)
                    xVariables.append(myString)

    ###Find 'U' variable list.###
    for graph in graphList:
        g = graph.graphID
        for k in graph.messageNodes:
            parentNode = graph.parentNodes[k][0]
            childNode = graph.childNodes[k][0]
            for r in range(1, numberOfProcessor + 1):
                for t1 in range(graph.asap[parentNode], graph.alap[parentNode] + 1): 
                    for t2 in range(graph.asap[childNode], graph.alap[childNode] + 1): 
                        myString = "u"+(str)(k)+","+(str)(r)+","+(str)(t1)+","+(str)(t2)
                        uVariables.append(myString)
    
    ###Find 'Y' variable list.###
    for graph in graphList:
        g = graph.graphID
        for k in graph.messageNodes:
            myString = "y"+(str)(k)
            yVariables.append(myString)


    ###Make list for myColNames, myObj, myUb, myLb, myCtype.###
    myColNames = []
    myObj = []
    myUb = []
    myLb = []
    myCtype = []
    
    ###Add variable 'Z' for the objective function which is different from previously taken variables 'Z'.###
    myColNames.append("Z")
    myObj.append(1)
    myUb.append(cplex.infinity)
    myLb.append(0)
    myCtype = "C"

    ##Add 'X' variables to myColNames. ##
    for x in xVariables:
        myColNames.append(x)
        myObj.append(0)
        myUb.append(1)
        myLb.append(0)
        myCtype = myCtype+"B"

    ##Add 'U' variables to myColNames. ##
    for u in uVariables:
        myColNames.append(u)
        myObj.append(0)
        myUb.append(1)
        myLb.append(0)
        myCtype = myCtype+"B"

    ##Add 'Y' variables to myColNames. ##
    for y in yVariables:
        myColNames.append(y)
        myObj.append(0)
        myUb.append(1)
        myLb.append(0)
        myCtype = myCtype+"B"
    

    ###########################################################################################################
    ###Make rows from all constraints (equations).###
    myRhs = []
    myRowNames = []
    mySense = ""
    myRows = []

    ###Equation 1 & 2 (Unique start time)###
    for graph in graphList:
        g = graph.graphID
        ##Unique start time for Task Nodes.##
        for i in graph.taskNodes:
            rowName = "Unique Start Time eq1 (Task"+(str)(i)+"):"
            variables = []
            coefficients = []
            for r in range(1, numberOfProcessor + 1):
                for t in range(graph.asap[i], graph.alap[i] + 1):
                    myString = "x"+(str)(i)+","+(str)(r)+","+(str)(t)
                    if myString in myColNames:
                        variables.append(myString)
                        coefficients.append(1)
            myRows.append([variables, coefficients])
            myRowNames.append(rowName)
            myRhs.append(1)
            mySense = mySense+"E"

        ##Unique start time for Message Nodes.##
        for k in graph.messageNodes:
            rowName = "Unique Start Time eq2 (Message"+(str)(k)+")"
            variables = []
            coefficients = []
            for r in range(1, numberOfBus + 1):
                for t in range(graph.asap[k], graph.alap[k] + 1):
                    myString = "x"+(str)(k)+","+(str)(r)+","+(str)(t)
                    if myString in myColNames:
                        variables.append(myString)
                        coefficients.append(1)
            myRows.append([variables, coefficients])
            myRowNames.append(rowName)
            myRhs.append(1)
            mySense = mySense+"L"
                
        ##Unique start time for Message Nodes.##
        for k in graph.messageNodes:
            rowName = "Message Handling eq2 (Message"+(str)(k)+")"
            variables = []
            coefficients = []
            for r in range(1, numberOfBus + 1):
                for t in range(graph.asap[k], graph.alap[k] + 1):
                    myString = "x"+(str)(k)+","+(str)(r)+","+(str)(t)
                    variables.append(myString)
                    coefficients.append(1)
            variables.append("y"+(str)(k))
            coefficients.append(1)
            myRows.append([variables, coefficients])
            myRowNames.append(rowName)
            myRhs.append(1)
            mySense = mySense+"E"


    ##Resource Constraints for Processors.##
    ###Equation 7 & 8 (Resource Constraints)###
    for r in range(1, numberOfProcessor + 1):
        for t in range(1, hyperPeriod + 1):
            rowName = "Resource Constraints eq7 (Processor) Time"+(str)(t)+":"
            variables = []
            coefficients = []
            for graph in graphList:
                g = graph.graphID
                if t <= graph.period:
                    for i in graph.taskNodes:
                        for tPrime in range((t-graph.executionTime[i][r-1] + 1), t + 1):
                            myString = "x"+(str)(i)+","+(str)(r)+","+(str)(tPrime)
                            if myString in myColNames:
                                variables.append(myString)
                                coefficients.append(1)
            ##If variable list is not empty then add to myRows.##                                        
            if len(variables) > 0:                                         
                myRows.append([variables, coefficients])
                myRowNames.append(rowName)
                myRhs.append(1)
                mySense = mySense+"L"

    ##Resource Constraints for Bus.##
    for r in range(1, numberOfBus + 1):
        for t in range(1, hyperPeriod + 1):
            rowName = "Resource Constraints eq8 (Bus) Time"+(str)(t)+":"
            variables = []
            coefficients = []
            for graph in graphList:
                g = graph.graphID
                if t <= graph.period:
                    for k in graph.messageNodes:
                        for tPrime in range((t-graph.executionTime[k][r-1] + 1), t + 1):
                            myString = "x"+(str)(k)+","+(str)(r)+","+(str)(tPrime)
                            if myString in myColNames:
                                variables.append(myString)
                                coefficients.append(1)
            ##If variable list is not empty then add to myRows.##                                        
            if len(variables) > 0:                                         
                myRows.append([variables, coefficients])
                myRowNames.append(rowName)
                myRhs.append(1)
                mySense = mySense+"L"


#    ###Equation 6 (Message handling i.e., discard message if both parent and child task nodes scheduled in same processor)###
#    for graph in graphList:
#        g = graph.graphID
#        ##Make Unique start time of Message Nodes 0, if both parent and child task nodes of are scheduled in same processor.##
#        for k in graph.messageNodes:
#            rowName = "Message Handling eq6 (Message"+(str)(k)+")"
#            variables = []
#            coefficients = []
#            for r in range(1, numberOfBus + 1):
#                for t in range(graph.asap[k], graph.alap[k] + 1):
#                    myString = "x"+(str)(k)+","+(str)(r)+","+(str)(t)
#                    variables.append(myString)
#                    coefficients.append(1)
#            variables.append("y"+(str)(k))
#            coefficients.append(1)
#            myRows.append([variables, coefficients])
#            myRowNames.append(rowName)
#            myRhs.append(1)
#            mySense = mySense+"E"


    ###Equation 3###
    for graph in graphList:
        g = graph.graphID
        for k in graph.messageNodes:
            parentNode = graph.parentNodes[k][0]
            childNode = graph.childNodes[k][0]
            rowName = "Linearization eq3 (Message"+(str)(k)+")"
            variables = []
            coefficients = []
            for r in range(1, numberOfProcessor + 1):
                for t1 in range(graph.asap[parentNode], graph.alap[parentNode] + 1): 
                    for t2 in range(graph.asap[childNode], graph.alap[childNode] + 1): 
                        myString = "u"+(str)(k)+","+(str)(r)+","+(str)(t1)+","+(str)(t2)
                        variables.append(myString)
                        coefficients.append(1)
            variables.append("y"+(str)(k))
            coefficients.append(-1)
            myRows.append([variables, coefficients])
            myRowNames.append(rowName)
            myRhs.append(0)
            mySense = mySense+"E"


    ###Equation 4, 5 & 6 (Linearization of equation 3).###
    for graph in graphList:
        g = graph.graphID
        for k in graph.messageNodes:
            parentNode = graph.parentNodes[k][0]
            childNode = graph.childNodes[k][0]
            rowName = "Linearization eq4 (Message"+(str)(k)+")"
            rowName1 = "Linearization eq5 (Message"+(str)(k)+")"
            rowName2 = "Linearization eq6 (Message"+(str)(k)+")"
            tempRows = []
            tempRowNames = []
            tempRhs = []
            tempSense = "" 
            for r in range(1, numberOfProcessor + 1):
                for t1 in range(graph.asap[parentNode], graph.alap[parentNode] + 1): 
                    for t2 in range(graph.asap[childNode], graph.alap[childNode] + 1): 
                        myString = "u"+(str)(k)+","+(str)(r)+","+(str)(t1)+","+(str)(t2)
                        myString1 = "x"+(str)(parentNode)+","+(str)(r)+","+(str)(t1)
                        myString2 = "x"+(str)(childNode)+","+(str)(r)+","+(str)(t2)

                        ##Equation 4 ##
                        tempRows.append([[myString, myString1], [1, -1]])
                        tempRowNames.append(rowName)
                        tempRhs.append(0)
                        tempSense = tempSense+"L"

                        ##Equation 5 ##
                        tempRows.append([[myString, myString2], [1, -1]])
                        tempRowNames.append(rowName1)
                        tempRhs.append(0)
                        tempSense = tempSense+"L"

                        ##Equation 6 ##
                        tempRows.append([[myString, myString1, myString2], [1, -1, -1]])
                        tempRowNames.append(rowName2)
                        tempRhs.append(-1)
                        tempSense = tempSense+"G"

            myRows = myRows + tempRows
            myRowNames = myRowNames + tempRowNames
            myRhs = myRhs + tempRhs
            mySense = mySense + tempSense


    ###Equation 15 (Dependency Constraints).###
    for graph in graphList:
        g = graph.graphID
        for k in graph.messageNodes:
            rowName = "Dependency Constraints eq15 (Message"+(str)(k)+")"
            parentNode = graph.parentNodes[k][0]
            childNode = graph.childNodes[k][0]
            variables = []
            coefficients = []

            ##For Parent Node.##
            for r in range(1, numberOfProcessor + 1):
                for t1 in range(graph.asap[parentNode], graph.alap[parentNode] + 1):
                    myString = "x"+(str)(parentNode)+","+(str)(r)+","+(str)(t1)
                    variables.append(myString)
                    coefficients.append(t1 + graph.executionTime[parentNode][r-1])

            ##For Child Node.##
            for r in range(1, numberOfProcessor + 1):
                for t2 in range(graph.asap[childNode], graph.alap[childNode] + 1):
                    myString = "x"+(str)(childNode)+","+(str)(r)+","+(str)(t2)
                    variables.append(myString)
                    coefficients.append(-t2)

            myRows.append([variables, coefficients])
            myRowNames.append(rowName)
            myRhs.append(0)
            mySense = mySense+"L"


    ###Equation 16 (Dependency Constraints).###
    for graph in graphList:
        g = graph.graphID
        for k in graph.messageNodes:
            rowName = "Dependency Constraints eq16 (Message"+(str)(k)+")"
            parentNode = graph.parentNodes[k][0]
            childNode = graph.childNodes[k][0]
            variables = []
            coefficients = []

            ##For Parent Node.##
            for r in range(1, numberOfProcessor + 1):
                for t1 in range(graph.asap[parentNode], graph.alap[parentNode] + 1):
                    myString = "x"+(str)(parentNode)+","+(str)(r)+","+(str)(t1)
                    variables.append(myString)
                    coefficients.append(t1 + graph.executionTime[parentNode][r-1])

            ##For Message Node.##
            for r in range(1, numberOfBus + 1):
                for t in range(graph.asap[k], graph.alap[k] + 1):
                    myString = "x"+(str)(k)+","+(str)(r)+","+(str)(t)
                    variables.append(myString)
                    coefficients.append(-t)

            myString = "y"+(str)(k)
            variables.append(myString)
            coefficients.append(-constantC)

            myRows.append([variables, coefficients])
            myRowNames.append(rowName)
            myRhs.append(0)
            mySense = mySense+"L"


    ###Equation 13 (Dependency Constraints).###
    for graph in graphList:
        g = graph.graphID
        for k in graph.messageNodes:
            rowName = "Dependency Constraints eq13 (Message"+(str)(k)+")"
            childNode = graph.childNodes[k][0]
            variables = []
            coefficients = []

            ##For Message Node.##
            for r in range(1, numberOfBus + 1):
                for t in range(graph.asap[k], graph.alap[k] + 1):
                    myString = "x"+(str)(k)+","+(str)(r)+","+(str)(t)
                    variables.append(myString)
                    coefficients.append(t + graph.executionTime[k][r-1])

            ##For Child Node.##
            for r in range(1, numberOfProcessor + 1):
                for t2 in range(graph.asap[childNode], graph.alap[childNode] + 1):
                    myString = "x"+(str)(childNode)+","+(str)(r)+","+(str)(t2)
                    variables.append(myString)
                    coefficients.append(-t2)

            myRows.append([variables, coefficients])
            myRowNames.append(rowName)
            myRhs.append(0)
            mySense = mySense+"L"


    ###Equation 14 (Objective Function).###
    rowName = "Objective Function"
    variables = ["Z"]
    coefficients = [1]
    for graph in graphList:
        g = graph.graphID
        ##Find sink node "f".##
        for f in graph.adjacentList.keys():
            if len(graph.adjacentList[f]) == 0:
                for r in range(1, numberOfProcessor + 1):
                    for t in range(graph.asap[f], graph.alap[f] + 1):
                        myString = "x"+(str)(f)+","+(str)(r)+","+(str)(t)
                        variables.append(myString)
                        coefficients.append(-(t + graph.executionTime[f][r-1] -1))

    myRows.append([variables, coefficients])
    myRowNames.append(rowName)
    myRhs.append(0)
    mySense = mySense+"G"

    ###########################################################################################################
    

    ####Populate problem by row.####
    prob.objective.set_sense(prob.objective.sense.maximize)
    prob.objective.set_sense(prob.objective.sense.minimize)
    prob.variables.add(obj=myObj, lb=myLb, types=myCtype, names=myColNames)
    prob.linear_constraints.add(lin_expr=myRows, senses=mySense, rhs=myRhs, names=myRowNames)


def mipex1():
    try:
        myProb = cplex.Cplex()
        handle = populatebyrow(myProb, graphList)
        myProb.set_log_stream(None)
        myProb.set_error_stream(None)
        myProb.set_warning_stream(None)
        myProb.set_results_stream(None)

        start = time.time()
        myProb.solve()
        finish = time.time()

        numberOfVariable = myProb.variables.get_num()
        varNames = myProb.variables.get_names()
        solution = myProb.solution.get_values()


    except CplexError as e:
        print "CplexError: ", e
        return

    myProb.write("problem.lp")
    myProb.solution.write("solution.sol")
    runningTime = finish - start

    return numberOfVariable, solution, varNames, runningTime
                                


###Run Cplex and print results.###
def runCplex(outFileName):
    numberOfVariable, solution, varNames, runningTime = mipex1()

    outFileObject = open(outFileName, "a")

    graph = graphList[0]
    outFileObject.write("###################################################OUTPUT##########################################################\n\n")
    outFileObject.write("Number of Nodes = "+str(graph.numberOfNode)+"\t(Task Nodes = "+str(len(graph.taskNodes))+"\tMessage Nodes = "+str(len(graph.messageNodes))+")\n")
    outFileObject.write("Processors = "+str(numberOfProcessor)+"\n");
    outFileObject.write("Buses = "+str(numberOfBus)+"\n");
    outFileObject.write("Given Deadline = "+str(graph.period)+"\n");

    outFileObject.write("--------------------------------------------------------------\n")
    outFileObject.write("\nDetails of Schedule:\n")
#    print "\nDetails of Schedule:"
    
    result = []
    for n in range(numberOfVariable):
        if solution[n] > 0:
    #    if solution[n] > 0 and "x" in varNames[n]:
            result.append([varNames[n], solution[n]])
    result.sort()
    
    outFileObject.write("Node_ID\tStart_Time\tFinish_Time\tExecution_Time\tResource_ID\n")
    outFileObject.write("--------------------------------------------------------------\n")
#    print "Node_ID\tStart_Time\tFinish_Time\tExecution_Time\tResource_ID"
#    print "--------------------------------------------------------------------------------------\n"
    graph = graphList[0]

    for n in range(len(result)):
        #print result[n][0], ":", result[n][1]
        ##Find index value associated with variable 'X'.##
        string = result[n][0]
        if 'x' in string:
            string = string[:1] + "," + string[1:]
            index = []
            for s in string.split(","):
                if s.isdigit():
                    index.append(int(s))
            i = index[0]
            r = index[1]
            t = index[2]
            if i in graph.taskNodes:
                outFileObject.write("T"+str(i)+"\t\t"+str(t)+"\t\t"+str(t + graph.executionTime[i][r-1] - 1)+"\t\t"+str(graph.executionTime[i][r-1])+"\t\tP"+str(r)+"\n")
#                print "T", i, "\t\t", t, "\t\t", (t + graph.executionTime[i][r-1] - 1), "\t\t", graph.executionTime[i][r-1], "\t\tP", r
            if i in graph.messageNodes:
                outFileObject.write("M"+str(i)+"\t\t"+str(t)+"\t\t"+str(t + graph.executionTime[i][r-1] - 1)+"\t\t"+str(graph.executionTime[i][r-1])+"\t\tB"+str(r)+"\n")
#                print "M", i, "\t\t", t, "\t\t", (t + graph.executionTime[i][r-1] - 1), "\t\t", graph.executionTime[i][r-1], "\t\tB", r
    outFileObject.write("--------------------------------------------------------------\n")
#    print "--------------------------------------------------------------------------------------\n"
    outFileObject.write("Total variables = "+str(numberOfVariable)+"\n")
#    print "Total variables =", numberOfVariable, "\n"
    outFileObject.write("Program Execution Time = "+str(runningTime)+" Seconds\n")
#    print "Program Execution Time =", runningTime, "Seconds"
    outFileObject.write("Schedule Length = "+str(solution[0])+"\n")
#    print "Optimal Schedule Length = ", solution[0]
#    print "--------------------------------------------------------------------------------------\n"
    outFileObject.write("--------------------------------------------------------------\n")
#    outFileObject.write("\n#################################################################################################################\n\n\n")
    outFileObject.close()

    ## deadline, optimalScheduleLength, runningTime##
    result = [graph.period, solution[0], runningTime]
    return result

inFile = sys.argv[1]
outFile = sys.argv[2]
numberOfProcessor, numberOfBus, numberOfGraph = readGraph(inFile) ##Read graph from file.##
hyperPeriod = calculateHyperperiod(graphList)

###Display details of the system.##
#print "Number of Processor:", numberOfProcessor
#print "Number of Bus:", numberOfBus
#print "Number of Graph:", numberOfGraph
#print "Hyperperiod = ", hyperPeriod
####Display graph###
#for graph in graphList:
#    graph.valuesOfNode()

## Run Cplex Optimization Solver ##
result = runCplex(outFile)


f = open("./outputFiles/output_ILP2.txt", "a")

graph = graphList[0]
## Find average task executation time.##
avgExecutation = 0
for i in graph.taskNodes:
    avgExecutation = avgExecutation + sum(graph.executionTime[i])
avgExecutation = float(avgExecutation) / (len(graph.taskNodes)* numberOfProcessor)
## Find average message transmission time.##
avgTransmission = 0
for i in graph.messageNodes:
    avgTransmission = avgTransmission + sum(graph.executionTime[i])
avgTransmission = float(avgTransmission) / (len(graph.messageNodes)* numberOfBus)
## CCR = Communication to Computation Ratio.##
ccr = round((avgTransmission / avgExecutation), 3)

#print "avgExecutation =", avgExecutation, "\navgTransmission =", avgTransmission

### numberOfNode, numberOfTask, numberOfMessage, numberOfProcessor, numberOfBus, CCR, result[Deadline, scheduleLength, runningTime] ###
f.write(str(inFile)+"\t"+str(graph.numberOfNode)+"\t"+str(len(graph.taskNodes))+"\t"+str(len(graph.messageNodes))+"\t"+str(numberOfProcessor)+"\t"+str(numberOfBus)+"\t"+str(ccr)+"\t"+str(result[0])+"\t"+str(result[1])+"\t"+str(round(result[2], 4)))
#f.write(str(inFile)+"\t"+str(graph.numberOfNode)+"\t"+str(len(graph.taskNodes))+"\t"+str(len(graph.messageNodes))+"\t"+str(numberOfProcessor)+"\t"+str(numberOfBus)+"\t"+str(ccr)+"\t"+str(result[0])+"\t"+str(result[1])+"\t"+str(round(result[2], 4))+"\n")
f.close()

#print "End of ILP"
