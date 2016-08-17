# -*- coding: utf-8 -*-

import sys, numpy, scipy
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist
import csv
import scipy.stats as stats
import json
import networkx as nx
from networkx.readwrite import json_graph

def makeNestedJson(leaf) :
    leaf=json.loads(leaf)    
    
    #A tree is a directed graph - create one with a dummy root
    DG=nx.DiGraph()
    DG.add_node('root')

    #Construct the tree as a directed graph and annotate the nodes with attributes
    #Edges go from parent to child
    for e in leaf:
        DG.add_node(e['id'],label=e['label'])
        #If there's a parent, use it...
        if 'parent' in e: DG.add_edge(e['parent'],e['id'])
        #else create a dummy parent from the dummy root
        else: DG.add_edge('root',e['id'])


    #Get the tree as JSON
    data = json_graph.tree_data(DG,root='root')
    #and dump the data from the dummy root's children down...
    return json.dumps(data['children'])

# This function puts root and makes hierarchy tree 
def makeHier(data, length, typeRC, parentId, grandParentId):
    # put very first data (root) 
    hierData = str(int(data[len(data)-1])) + "."
    #print (hierData)
    # data : whole data, len(hierMatrix)-1 : data's length, hierData : current stored data array 
    getElem (data, len(data)-1, hierData, length, typeRC, parentId, grandParentId) 
    
    
# This function puts other data excluding root
# data : total hiermatrix, parentNum : cluster number, hier : total string which separate ".", length : each total length of col or row matrix, parentId : parent Id (it differs parent number)
def getElem(data, parentNum, hier, length, typeRC, parentId, grandParentId):
   #'parent' : parentId , 'id' : data[parentNum] (current Id)
    #print(rowLeafNum)
    #print(colLeafNum)
    # Check whether it is 
    
    if parentNum-4 >= 0 :
        #isChecked = 0        
        
        # Put current data
        
        if (parentNum != len(data)-1):
          
          #leafData.append(str(int(hierMatrix[-1])) + ".")  
            hier += str(int(data[parentNum])) + "."
            #
            if (typeRC == "row"):
                global rowLeafNum
                rowLeafNum = rowLeafNum + 1
                if int(data[parentNum]) > length:
                    global content
                    content['label'] = "null"
                else:
                    global content
                    content['label'] = rowNameArr[int(data[parentNum])][0]
                global content
                content['parent'] = int(grandParentId)
                global content
                content['id'] = int(data[parentNum])
                global leafData
                leafData += str(content) + ", "
                dotLeafData.append(hier)
            else : 
                global colLeafNum
                colLeafNum = colLeafNum + 1
                #print(colHeaders)
                #print(int(data[parentNum])-1)
                if int(data[parentNum]) > length:
                    global colContent
                    colContent['label'] = "null"
                else:
                    global colContent
                    colContent['label'] = colNameArr[int(data[parentNum])-1]
                global colContent
                colContent['parent'] = int(grandParentId)  
                global colContent
                colContent['id'] = int(data[parentNum])
                global colLeafData
                colLeafData += str(colContent) + ", "
                global dotcolLeafData
                dotcolLeafData.append(hier)
            #print ("gradParentId : " + str(int(grandParentId)))
            #print ("parentId : " + str(int(parentId)))
            #print ("id : " + str(int(data[parentNum])))

            #print (leafData[rowLeafNum])
            #print (colLeafData[colLeafNum])
            
            #print (hier)
            #print(content)
            #print(colContent)
            #print("leafleafleafleafleafleafleaf")
            #print(leafData)
            #print(colLeafData)
            
        if data[parentNum-3] >= length and data[parentNum-4] >= length:
            
            #print (parentNum-3 , data[parentNum-3])
            #print (parentNum-4 , data[parentNum-4])
            
            getElem(data, searchNum(data, numpy.where(data==data[parentNum-4]), parentNum-4), hier,length,typeRC, int(data[parentNum]-4), int(data[parentNum])) 
            getElem(data, searchNum(data, numpy.where(data==data[parentNum-3]), parentNum-3), hier,length,typeRC, int(data[parentNum]-3), int(data[parentNum]))
        
        elif data[parentNum-3] < length and data[parentNum-4] > length:
            #print (parentNum-4 , data[parentNum-4])
            hier += str(int(data[parentNum-3])) + "."
            if (typeRC == "row"):
                rowLeafNum = rowLeafNum + 1
                if int(data[parentNum-3]) > length:
                    global content
                    content['label'] = "null"
                else:
                    global content
                    content['label'] = rowNameArr[int(data[parentNum-3])][0]
                global content
                content['parent'] = int(int(data[parentNum]))
                global content
                content['id'] = int(data[parentNum-3])
                global leafData
                leafData += str(content) + ", "
                dotLeafData.append(hier)
            else : 
                colLeafNum = colLeafNum + 1
                if int(data[parentNum-3]) > length:
                    global colContent
                    colContent['label'] = "null"
                else:
                    global colContent
                    colContent['label'] = colNameArr[int(data[parentNum-3])-1]
                global colContent
                colContent['parent'] = int(int(data[parentNum]))  
                global colContent
                colContent['id'] = int(data[parentNum-3])
                global colLeafData
                colLeafData += str(colContent) + ", "
                global dotcolLeafData
                dotcolLeafData.append(hier)
            #print(content)
            #print (leafData[rowLeafNum])
            #print (colLeafData[colLeafNum])
            removeNum = len(str(int(data[parentNum-3]))) + 1
            hier = hier[:-removeNum]
            getElem(data, searchNum(data, numpy.where(data==data[parentNum-4]), parentNum-4), hier, length,typeRC, int(data[parentNum]-4), int(data[parentNum]))
        elif data[parentNum-3] > length and data[parentNum-4] < length:
            #print (parentNum-3 , data[parentNum-3])
            hier += str(int(data[parentNum-4])) + "."
            if (typeRC == "row"):
                rowLeafNum = rowLeafNum + 1
                if int(data[parentNum-4]) > length:
                    global content
                    content['label'] = "null"
                else:
                    global content
                    content['label'] = rowNameArr[int(data[parentNum-4])][0]
                global content
                content['parent'] = int(int(data[parentNum]))
                global content
                content['id'] = int(data[parentNum-4])
                global leafData
                leafData += str(content) + ", "
                global dotLeafData
                dotLeafData.append(hier)
            else : 
                colLeafNum = colLeafNum + 1
                if int(data[parentNum-4]) > length:
                    global colContent
                    colContent['label'] = "null"
                else:
                    global colContent
                    colContent['label'] = colNameArr[int(data[parentNum-4])-1]
                global colContent
                colContent['parent'] = int(int(data[parentNum]))  
                global colContent
                colContent['id'] = int(data[parentNum-4])
                global colLeafData
                colLeafData += str(colContent) + ", "
                global dotcolLeafData
                dotcolLeafData.append(hier)
            #print(content)
            removeNum = len(str(int(data[parentNum-4]))) + 1
            hier = hier[:-removeNum]
            getElem(data, searchNum(data, numpy.where(data==data[parentNum-3]), parentNum-3), hier, length,typeRC, int(data[parentNum]-3), int(data[parentNum]))
            #print (leafData[rowLeafNum])
            #print (colLeafData[colLeafNum])
        else:
            hier += str(int(data[parentNum-4])) + "."
            if (typeRC == "row"):
                rowLeafNum = rowLeafNum + 1
                if int(data[parentNum-4]) > length:
                    global content
                    content['label'] = "null"
                else:
                    global content
                    content['label'] = rowNameArr[int(data[parentNum-4])][0]
                global content
                content['parent'] = int(int(data[parentNum]))
                global content
                content['id'] = int(data[parentNum-4])
                leafData += str(content) + ", "
                dotLeafData.append(hier)
            else : 
                colLeafNum = colLeafNum + 1
                if int(data[parentNum-4]) > length:
                    global colContent
                    colContent['label'] = "null"
                else:
                    global colContent
                    colContent['label'] = colNameArr[int(data[parentNum-4])-1]
                global colContent
                colContent['parent'] = int(int(data[parentNum]))  
                global colContent
                colContent['id'] = int(data[parentNum-4])
                global colLeafData
                colLeafData += str(colContent) + ", "
                global dotcolLeafData
                dotcolLeafData.append(hier)
            #print(content)
            #print (parentNum-4 , data[parentNum-4])            
            #print(hier)
            removeNum = len(str(int(data[parentNum-4]))) + 1
            hier = hier[:-removeNum]
            hier += str(int(data[parentNum-3])) + "."
            #print (parentNum-3 , data[parentNum-3])
            #print(hier)
            #print (parentNum-3 , data[parentNum-3])
            #print (parentNum-4 , data[parentNum-4])
            if (typeRC == "row"):
                rowLeafNum = rowLeafNum + 1
                #print("length : " + str(length))
                #print("int(data[parentNum]): " + str(int(data[parentNum])))
                if int(data[parentNum-3]) > length:
                    global content
                    content['label'] = "null"
                else:
                    global content
                    content['label'] = rowNameArr[int(data[parentNum-3])][0]
                global content
                content['parent'] = int(int(data[parentNum]))
                global content
                content['id'] = int(data[parentNum-3])
                leafData += str(content) + ", "
                dotLeafData.append(hier)
            else : 
                colLeafNum = colLeafNum + 1
                if int(data[parentNum-3]) > length:
                    global colContent
                    colContent['label'] = "null"
                else:
                    global colContent
                    colContent['label'] = colNameArr[int(data[parentNum-3])-1]
                global colContent
                colContent['parent'] = int(int(data[parentNum]))  
                global colContent
                colContent['id'] = int(data[parentNum-3])
                global colLeafData
                colLeafData += str(colContent) + ", "
                global dotcolLeafData
                dotcolLeafData.append(hier)
            #print (leafData[rowLeafNum])
            #print (colLeafData[colLeafNum])
            
            #print(content)
            #print(rowNameArr[int(data[parentNum-3])])
        """if (data[parentNum-4] <= len(linkageMatrix)):
            hier += str(int(data[parentNum-4])) + "."
            leafData.append(hier)
            #print (hier)
            isChecked = 1
           # print (parentNum-3 , data[parentNum-3])
            
        if (data[parentNum-3] <= len(linkageMatrix)):
            if isChecked == 1 :
                removeNum = len(str(int(data[parentNum-4]))) + 1
                hier = hier[:-removeNum]
            hier += str(int(data[parentNum-3])) + "."
            leafData.append(hier)
            #print (parentNum-4 , data[parentNum-4])
            #print (hier)"""

def searchNum (data, index, pId):
    if index[0][0]< pId and ((index[0][0] % 5 == 0) or (index[0][0] % 5 == 1) or (index[0][0] % 5 == 4)):
        return index[0][0]
    else:
        return -1

def runFun(clusterType):
    #open the file assuming the data above is in a file called 'dataFile'
    inFile = open('/Users/ichung-gi/Documents/ChunggiLee.github.io/Heatmap/n50_heatmap_test.data','r')
    #save the column/row headers (conditions/genes) into an array
    colHeaders = inFile.readline().strip().split()[1:]
    rowHeaders = []
    dataMatrix = []
    #print(colHeaders)

    #Extract row data
    for line in inFile:
        #print(line)
        data = line.strip().split('\t')
        #if len(data) < 5:
        #    data.insert(0,"nameless")
        rowHeaders.append([data[0]])
        #print(rowHeaders)
        dataMatrix.append([float(x) for x in data[1:]])

    #Extract col data
    colDataMatrix= []
    for i in range(0, len(colHeaders)):
        colDataMatrix.append([row[i] for row in dataMatrix])

    #print(colDataMatrix[0])
    global rowNameArr
    rowNameArr = rowHeaders
    global colNameArr
    colNameArr = colHeaders

    #convert native data array into a numpy array
    #print(dataMatrix)
    dataMatrix = numpy.array(dataMatrix)
    colDataMatrix = numpy.array(colDataMatrix)
    #log2 transform
    dataMatrix = numpy.log2(dataMatrix)
    colDataMatrix = numpy.log2(colDataMatrix)
    #zscore transform
    dataMatrix = stats.zscore(dataMatrix,1,1)
    colDataMatrix = stats.zscore(colDataMatrix,1,1)
    #print(dataMatrix)
    #print(colDataMatrix)

    print("s1")

    distanceMatrix = dist.pdist(dataMatrix)
    colDistanceMatrix = dist.pdist(colDataMatrix)
    #print("dataMatrix : " )
    #print(distanceMatrix)

    print("s2")
    
    distanceSquareMatrix = dist.squareform(distanceMatrix)
    colDistanceSquareMatrix = dist.squareform(colDistanceMatrix)
    print("s3")
    #clusterType = "ward"
    linkageMatrix = hier.linkage(distanceSquareMatrix, clusterType)
    colLinkageMatrix = hier.linkage(colDistanceSquareMatrix, clusterType)

    #print(distanceSquareMatrix)
    print("s4")

    heatmapOrder = hier.leaves_list(linkageMatrix)
    hierMatrix = [[]]
    colHierMatrix = [[]]

    print("s5")

    newNum = len(linkageMatrix)
    colNewNum = len(colLinkageMatrix)

    for i in range(0, len(linkageMatrix)):
        newNum += 1
        hierMatrix =  numpy.array(numpy.append(hierMatrix, numpy.append(linkageMatrix[i], [newNum])))

    for i in range(0, len(colLinkageMatrix)):
        colNewNum += 1
        colHierMatrix =  numpy.array(numpy.append(colHierMatrix, numpy.append(colLinkageMatrix[i], [colNewNum])))

    print("s6")
    #print ("heatmapOrder : ")
    #print ( heatmapOrder)
    #print(linkageMatrix)
    #print(hierMatrix)
    #print(hierMatrix[-1])
    #print(colHierMatrix)
    
    content['label'] = "root"
    content['parent'] = "root"
    content['id'] = int(hierMatrix[-1])
    global leafData
    leafData += str(content) + ", "
    #leafData.append(str(int(hierMatrix[-1])) + ".")  
    colContent['label'] = "root"
    colContent['parent'] = "root"
    colContent['id'] = int(colHierMatrix[-1])
    global colLeafData
    colLeafData += str(colContent) + ", "
    
    dotLeafData.append(str(int(hierMatrix[-1]))+".")
    global dotcolLeafData
    dotcolLeafData.append(str(int(colHierMatrix[-1]))+".")
    #colLeafData.append(str(int(colHierMatrix[-1])) + ".")
    makeHier(hierMatrix, len(linkageMatrix), "row", int(hierMatrix[-1]), len(linkageMatrix)) 
    makeHier(colHierMatrix, len(colLinkageMatrix)+1, "col", int(colHierMatrix[-1]),len(colLinkageMatrix))


    #print (leafData)
    for i in range(len(dotLeafData)):
        global dotLeafData
        dotLeafData[i] = dotLeafData[i][:-1]
        #print(leafData[i])
	
    for i in range(len(dotcolLeafData)):
        global dotcolLeafData
        dotcolLeafData[i] = dotcolLeafData[i][:-1]
        

    orderedDataMatrix = dataMatrix[heatmapOrder,:]
    
    print("s7")
    #print(orderedDataMatrix)
    rowHeaders = numpy.array(rowHeaders)
    orderedRowHeaders = rowHeaders[heatmapOrder,:]
    #print(orderedRowHeaders)
    print("s8")
    matrixOutput = []
    row = 0
    for rowData in orderedDataMatrix:
        col = 0
        rowOutput = []
        for colData in rowData:
            rowOutput.append([colData, row, col])
            col += 1
        matrixOutput.append(rowOutput)
        row += 1
    print("s9")
    
    global leafData
    leafData = leafData[:-2]
    leafData += "]"
    #print (leafData)
    global colLeafData
    colLeafData = colLeafData[:-2]
    global colLeafData
    colLeafData += "]"
    #print (colLeafData)
    #maxData = 'var ' + clusterType + 'maxData = ' + str(numpy.amax(dataMatrix)) + ";\n"
    #minData = 'var ' + clusterType + 'minData = ' + str(numpy.amin(dataMatrix)) + ";\n"
    maxData = 'var ' + 'maxData = ' + str(numpy.amax(dataMatrix)) + ";\n"
    minData = 'var ' + 'minData = ' + str(numpy.amin(dataMatrix)) + ";\n"
    data = 'var ' + clusterType + 'data = ' + str(matrixOutput) + ";\n"
    cols = 'var ' + clusterType + 'cols = ' + str(colHeaders) + ";\n"
    #row  = 'var rows = ' + str([x for x in orderedRowHeaders]) + ";\n"
    #print ('var maxData = ' + str(numpy.amax(dataMatrix)) + ";")
    #print ('var minData = ' + str(numpy.amin(dataMatrix)) + ";")
    #print ('var data = ' + str(matrixOutput) + ";")
    #print ('var cols = ' + str(colHeaders) + ";")
    oneDimensionOrderedRowHeaders = []
    for i in range(len(orderedRowHeaders)):
        oneDimensionOrderedRowHeaders.append(orderedRowHeaders[i][0])
    
    row = 'var ' + clusterType + 'rows = ' + str(oneDimensionOrderedRowHeaders) + ";\n"
    #print ('var rows = ' + str(oneDimensionOrderedRowHeaders) + ";\n")
    
    #print (json.dumps(leafData, sort_keys=False, indent=4))
    #print (json.dumps(colLeafData, sort_keys=False, indent=4))
    global leafData
    leafData = leafData.replace("/", "")   
    global colLeafData
    colLeafData = colLeafData.replace("/", "")
    global leafData
    leafData = leafData.replace("\'", "\"")   
    global colLeafData
    colLeafData = colLeafData.replace("\'", "\"")
    
    
    #print(type(leafData))
    #print(leafData)
    #print (makeNestedJson(leafData))
    """
    file = open("/Users/ichung-gi/Documents/ChunggiLee.github.io/Heatmap/rowJsonData.js","w")
    file.write("var " + clusterType + "RowJson = " + str(makeNestedJson(leafData)) + ";")
    file.close()
    
    file = open("/Users/ichung-gi/Documents/ChunggiLee.github.io/Heatmap/colJsonData.js","w")
    file.write("var " + clusterType + "ColJson = " + str(makeNestedJson(colLeafData)) + ";")
    file.close()
    
    file = open("/Users/ichung-gi/Documents/ChunggiLee.github.io/Heatmap/rowJsonData.json","w")
    file.write(str(makeNestedJson(leafData)))
    file.close()
    
    file = open("/Users/ichung-gi/Documents/ChunggiLee.github.io/Heatmap/colJsonData.json","w")
    file.write(str(makeNestedJson(colLeafData)))
    file.close()
    """
    
    #Store heatmap infomation to js
    
    file = open("/Users/ichung-gi/Documents/ChunggiLee.github.io/Heatmap/genomixdata.js","a")
    file.write(maxData)
    file.write(minData)
    file.write(data)
    file.write(cols)
    file.write(row)
    file.close()
    
    #print (leafData)
    
    
    # Store hiararchy data infomation to csv file.
    csv_file = open("/Users/ichung-gi/Documents/ChunggiLee.github.io/Heatmap/" + clusterType + "tree.csv","w")
    cw = csv.writer(csv_file, delimiter=',', quotechar='|')
    cw.writerow(("id","value"))
    
    for i in range (len(dotLeafData)):
        if int(dotLeafData[i][-1]) <= len(linkageMatrix):
            num = ""
            for j in range( len(dotLeafData[i])):
                k = 1 + j
                #print(leafData[i][-k])
                if dotLeafData[i][-k] == ".":
                    break
                else :
                    num += dotLeafData[i][-k]
                    
            #print(num)       
            cw.writerow((" "+str(dotLeafData[i]),""))
        else :
            #print()
            cw.writerow((" "+str(dotLeafData[i]),""))
            
    csv_file.close()
    
    csv_file = open("/Users/ichung-gi/Documents/ChunggiLee.github.io/Heatmap/" + clusterType + "coltree.csv","w")
    cw = csv.writer(csv_file, delimiter=',', quotechar='|')
    cw.writerow(("id","value"))
    
    for i in range (len(dotcolLeafData)):
        if int(dotcolLeafData[i][-1]) <= len(colLinkageMatrix):
            num = ""
            for j in range( len(dotcolLeafData[i])):
                k = 1 + j
                #print(leafData[i][-k])
                if dotcolLeafData[i][-k] == ".":
                    break
                else :
                    global dotcolLeafData
                    num += dotcolLeafData[i][-k]
                    
            #print(num)       
            cw.writerow((" "+str(dotcolLeafData[i]),""))
        else :
            #print()
            cw.writerow((" "+str(dotcolLeafData[i]),""))
            
    csv_file.close()

def init():
	cluster=["single","complete","average","weighted","centroid","median","ward"]
	for i in range(0, 1):#len(cluster)):
         #typeRC = ""
         global leafData
         leafData ="["
         global colLeafData
         colLeafData = "["
         global dotLeafData
         dotLeafData = []
         global dotcolLeafData
         dotcolLeafData = []
         global content
         content ={}
         global colContent
         colContent = {}
         global rowNameArr
         rowNameArr = []
         global colNameArr
         colNameArr = []
         global rowLeafNum
         rowLeafNum = 0
         global colLeafNum
         colLeafNum = 0
         runFun(cluster[i])
    
init()
    
