#!/usr/bin/env python3
class Node:
#the initialization of the node class, it will take a string for example"X" as the identifier, so that I know which table is it
    def __init__(self,identifier):
        self.identify = identifier
        self.DVlist = []
        self.neighbors = []
        self.minValue = {}
#addneighbor method,take a string as input, put it into the list neighbors,if nerghbors number grater than 1, sort it   
    def addneighbor(self,neighbor):
        self.neighbors.append(neighbor)
        if len(self.neighbors)>1:
            self.neighbors.sort(key=str.lower)
#from each of the dictionary find out the min value, remind that the first element is the y index, which is a lower cased charactor    
    def renewMin(self):        
        for dict in self.DVlist:
            key = getFirst(dict).upper()
            remainingDic = list(dict.items())[1:]
            result = compare(remainingDic)
            newDict = {key: result}
            self.minValue.update(newDict)
    
#assisstant method for renewMin(), it taks data from each dictionary, and if the value is an integer it will put it into the list
#if there is one number, that is the min value it will output, if there is no integers, return INF         
def compare(data):
    numbers = [item[1] for item in data if isinstance(item[1], int)]
    if len(numbers) == 1:
        result = numbers[0]
    elif len(numbers) == 0:
        return "INF"
    else:
        result = min(numbers)
    return result            
#printTable method, take the collection nodes as input, it is based on DVlist attribute of the node        
def printTable(nodes,t):
    t = str(t)
    for node in nodes:
        print(node.identify + " Distance Table at t=" + t)
        for dic1 in node.DVlist:
            value1 = getFirst(dic1).upper()
            print("\t" + value1, end="")
        print()
        for dic in node.DVlist:
            value = getFirst(dic).upper()
            print (value, end ="" )
            numbers = dic.values()
            for i, number in enumerate(numbers):
                if (i>=1):
                    number = str(number)
                    print("\t" + number, end = "")
            print()
        print()
#addRow function, for all the router in the network, all the node will have the router * y factor excapt it self
#it also has a sorting method at the end
def addRow(nodes,segment):
    for node in nodes:
        for charactor in segment:
            if charactor == node.identify:
                continue
            if len(node.DVlist)==0:
                dict = {charactor.lower(): 0}
                node.DVlist.append(dict)
            else:
                isInDic = False
                for dictionary in node.DVlist:
                    if charactor in dictionary:
                        isInDic = True
                if isInDic == True:
                    continue
                else:
                    dict = {charactor.lower(): 0}
                    node.DVlist.append(dict)
                    node.DVlist = sorted(node.DVlist, key = lambda x:list(x.keys())[0])
#sorting method, take a node as input, generate a new sorted DVlist to cover the origin one
def sorting(node):
    newDVlist = []
    for dic in node.DVlist:
        firstPart = list(dic.items())[:1]
        remainingDic = list(dic.items())[1:]
        sortedDic = sorted(remainingDic, key=lambda x: x[0])
        sortedDic = firstPart + sortedDic
        sortedDict = {k: v for k, v in sortedDic}
        newDVlist.append(sortedDict)
    newDVlist = sorted(newDVlist, key = lambda x:list(x.keys())[0])
    node.DVlist=newDVlist
#after generated full of "INF" table, this method helps to allocate number for the table          
def addValue(node,node1,num):
    cha1 = node.identify
    cha2 = node1.identify
    num = int(num)
    for dict in node1.DVlist:
        dictName = getFirst(dict).upper()
        if cha1 == dictName:
            add = {cha1:num}
            dict.update(add)            
    for dict1 in node.DVlist:
        dictName2 = getFirst(dict1).upper()
        if cha2 == dictName2:
            add = {cha2:num}
            dict1.update(add)  
            
#getFirst method, every useful, it's relies on the itrator to return the first key of the input dictionary
def getFirst(dic):
    return next(iter(dic))  
#the main algorithm, everytime it changes the value, it will change the flag, so that it not only renew the value but can also determine whether the loop should keep going
#it has lot of unique case, sometimes the link between routers broke, so one it find out the findDis() method return an INF, it knows
#sometimes, the other table tell it that there is no min value, which means the link has broken, in this case, the blank will becomes INF as well
#it is named algorithm3, because I used to have three algorithms for this assessment, after my understanding getting better, I realized one algorithm is enough           
def algorithm3(nodes):
    changed = False
    for node in nodes:
        nodeName = node.identify
        for i, dic in enumerate(node.DVlist):
            rowName = getFirst(dic).upper()
            for key, value in dic.items():
                if value == 0:
                    continue
                elif key == rowName:
                    continue
                else:
                    num1 = findDis(key,node)
                    if num1 == "INF" or num1 is None:
                        if node.DVlist[i][key]!= "INF":
                            if changed == False:
                                changed = True
                        node.DVlist[i][key] = "INF"
                        continue
                    num2 = findOp(key,rowName,nodes)
                    if num2 == "INF" or num2 is None:
                        if node.DVlist[i][key]!= "INF":
                            if changed == False:
                                changed = True
                        node.DVlist[i][key] = "INF"
                        continue
                    else:
                        num2 = splitHorizon(key,rowName,nodes,num2,nodeName)
                        if num2 == "INF":
                            if node.DVlist[i][key]!= "INF":
                                if changed == False:
                                    changed = True
                            node.DVlist[i][key] = "INF"
                            continue
                    SUM = num1 + num2
                    if SUM != node.DVlist[i][key]:
                        if changed == False:
                            changed = True
                    node.DVlist[i][key] = SUM
    return changed
#key method in this file, it was trigered only if XYZ find out for YZ, the shortest path was go through X
#it will return the second lowest distance                    
def splitHorizon(key,rowName,nodes,num2,nodeName):
    for node in nodes:
        if node.identify == key:
            for dic in node.DVlist:
                dicName = getFirst(dic).upper()
                if dicName == rowName:
                    newList = []
                    flag = False
                    for key1, value in dic.items():
                        if value == "INF":
                            continue
                        elif value == num2:
                            if key1 == nodeName:
                                flag = True
                            dicts = {key1:value}
                            newList.append(dicts)
                    if len(newList) == 1:  
                        if flag == True:
                            secondDic = {}
                            for key2, value2 in dic.items():
                                num = 0
                                if value2 == "INF":
                                    continue
                                elif value2 > num2:
                                    num = num+1
                                    newDic = {key2:value2}
                                    secondDic.update(newDic)
                            if num != 0:
                                secondList = secondDic.values()
                            else:
                                return "INF"
                            num2 = min(secondList)    
                    return num2
#assisstance method take key as input to search for its value in the dictionary                    
def findDis(keyIn, node):
    for Dic in node.DVlist:
        dicName = getFirst(Dic).upper()
        if dicName == keyIn:
            for key, value in Dic.items():
                if key == keyIn:
                    return value
#find the optional path, min(D(Y))               
def findOp(keyIn, rowName,nodes):
    for node in nodes:          
        id = node.identify
        if id == keyIn:
            for key,value in  node.minValue.items():
                if key ==rowName:
                    return value
                           
#print routing table, relies on the minValue attribute of the nodes       
def printRoutingTable(nodes):
    for node in nodes:
        cha = node.identify
        print(cha + " Routing Table:")
        list1 = list(node.minValue.items())
        for n, pairs in enumerate(list1):
            print(pairs[0] + ",",end ="")
            Charactor = getNH(node,n,pairs[1])
            print(Charactor + "," + str(pairs[1]))
        print()     
#get next hop method, only return the first key it find out
def getNH(node,n,value):
    alreadyGet = False
    dic = node.DVlist[n]
    for key, values in dic.items():
        if value == values and alreadyGet == False:
            alreadyGet = True
            return key
#create DVtable for nodes, all the value at this stage is INF    
def createTable(nodes,segment):
    for node in nodes:
        nodeName = node.identify
        for dic in node.DVlist:
            new = {}
            for cha in segment:
                if cha == nodeName:
                    continue
                new = {cha:"INF"}
                dic.update(new)     
#assisstance method help the dictionary find the key for specific value 
def findKeyByValue(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None  
#this method only apply when value == -1, will allocate INF for all the table has the cha1 and cha2 as its x factor      
def deNeighbor(cha1,cha2,nodes):
        for node in nodes:
            if node.identify == cha1:
                for i in range(len(node.DVlist)):
                    node.DVlist[i][cha2] = "INF"
            if node.identify == cha2:
                for i in range(len(node.DVlist)):
                    node.DVlist[i][cha1] = "INF"   
#allocate INF after  the link is broken                               
def allocateINF(nodes,charactor2):
    for node in nodes:
        for i in range(len(node.DVlist)):
            if charactor2 == getFirst(node.DVlist[i]).upper():
                for j in range(len(node.neighbors)):
                    newDict = {node.neighbors[j]:"INF"}
                    node.DVlist[i].update(newDict)
        for dicts in node.DVlist:
            new = {charactor2:"INF"}
            dicts.update(new)    
                
                                                                      
def main():
    segment1 = []
    segment2 = []
    segment3 = []
    nodes = []
    
    findD = False
    findU = False
    
#allocating value into the three segments, so that treat them seperately
    while True:
        line = input().split()
        if line [0] == "END":
            break
        
        if findD == False:
            if line[0] != "DISTANCEVECTOR":
                segment1.append(line)
            else:
                findD = True
                continue
        
        if findD ==True and findU == False:
            if line[0] != "UPDATE":
                segment2.append(line)
            else:
                findU = True
                continue
                
        if findD ==True and findU == True:
            segment3.append(line)
#change list into string    
    segment1 = [' '.join(item) for item in segment1]
    segment1.sort(key = str.lower)
    
    for element in segment1:
        node = Node(element)
        nodes.append(node)
#creating rows and tabls with INF as default value    
    addRow(nodes,segment1)
    createTable(nodes,segment1)
#dealing with the first segment    
    for listS in segment2:
        charactor1 = listS[0]
        charactor2 = listS[1]
        num = listS[2]
        if charactor1 in segment1 and charactor2 in segment1:
            for node in nodes:
                if node.identify == charactor1:
                    node1=node
                    node.addneighbor(charactor2)
                if node.identify == charactor2:
                    node2 = node
                    node.addneighbor(charactor1)
        elif charactor1 in segment1 and charactor2 not in segment1:
            node1 = Node(charactor2)
            node1.addneighbor(charactor1)
            nodes.append(node1)
            segment1.append(charactor2)
            addRow(nodes,segment1)
            allocateINF(nodes,charactor2)
            for node in nodes:
                if node.identify == charactor1:
                    node.addneighbor(charactor2)
                    node2 = node
        elif charactor1 not in segment1 and charactor2 in segment1:
            node1 = Node(charactor1)
            node1.addneighbor(charactor2)
            nodes.append(node1)
            segment1.append(charactor1)
            addRow(nodes,segment1)
            allocateINF(nodes,charactor1)
            for node in nodes:
                if node.identify == charactor2:
                    node.addneighbor(charactor1)
                    node2 =node
        addValue(node1,node2,num)
        sorting(node1)
        sorting(node2)
    
    printTable(nodes,0)
   #generate the min table 
    for node in nodes:
        node.renewMin()
    t=1
    while True:
            
            flag = True
            changeBoo = algorithm3(nodes)
#avoiding the first comparison
            if t != 1:
                if changeBoo == False:
                    for node in nodes:
                        node.renewMin()                   
                    break
            
            printTable(nodes,t)

            for node in nodes:
                oldDic = node.minValue.copy()
                node.renewMin()
                newDic = node.minValue.copy()
                if oldDic != newDic:
                    flag = False
            t= t +1 
#if the min table didn't change, end   
            if flag == True:
                break
            
    
    printRoutingTable(nodes)
#deal with the third segment updating 
    if len(segment3) != 0:
        for listS in segment3:
            charactor1 = listS[0]
            charactor2 = listS[1]
            num = listS[2]
            if charactor1 in segment1 and charactor2 in segment1:
                if num == "-1":
                    deNeighbor(charactor1,charactor2,nodes)
                else:
                    for node in nodes:
                        if node.identify == charactor1:
                            node1 = node
                        if node.identify == charactor2:
                            node2 = node
                    addValue(node1,node2,num)
            elif charactor1 in segment1 and charactor2 not in segment1:
                node1 = Node(charactor2)
                node1.addneighbor(charactor1)
                nodes.append(node1)
                segment1.append(charactor2)
                addRow(nodes,segment1)
                allocateINF(nodes,charactor2)
                for node in nodes:
                    if node.identify == charactor1:
                        node.addneighbor(charactor2)
                        node2 = node
                addValue(node1,node2,num)
                sorting(node1)
                sorting(node2) 
            elif charactor1 not in segment1 and charactor2 in segment1:
                node1 = Node(charactor1)
                node1.addneighbor(charactor2)
                nodes.append(node1)
                segment1.append(charactor1)
                addRow(nodes,segment1)
                allocateINF(nodes,charactor1)
                for node in nodes:
                    if node.identify == charactor2:
                        node.addneighbor(charactor1)
                        node2 =node
                addValue(node1,node2,num)
                sorting(node1)
                sorting(node2) 
        num2 = t 
        while True:
            
            flag = True
            boo = algorithm3(nodes)
            if num2 != t:
                if boo == False:
                    for node in nodes:
                        node.renewMin()
                
                    break
            
            printTable(nodes,t)

            for node in nodes:
                oldDic = node.minValue.copy()
                node.renewMin()
                newDic = node.minValue.copy()
                if oldDic != newDic:
                    flag = False
                
            if flag == True:
                break
            t = t+1
        printRoutingTable(nodes)
        
main()
        
        
        
    
        
    
    