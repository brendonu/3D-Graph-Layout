import re
from sys import addaudithook, float_repr_style
import math
import random
import numpy as np
from matplotlib import pyplot as plt

debug = False
attractiveForce = 0
repulsiveForceStrength = 1000
attractiveForceStrength = 1000

# Parse a single bibtex citation, store each entry in the citation as a key-value pair.
# Store references as a numbered dictionary instead of as one large string.
def parseBibtexEntry():
    adjacency_list = []
    
    with open('Testing/list_1_graphs (1).lst', 'r') as f:
        for line in f:
            if not line or ':' not in line:
                continue
            # Splitting line by ":" to separate node from its connections
            node, connections = line.split(":")
            node = node.strip()
            # Splitting the connections and removing any leading/trailing whitespace
            connected_nodes = connections.strip().split()

            # Assuming the previous code expected a "flag" (e.g., True/False or some other data)
            # you could add a default value here, or infer it from the data
            flag = True  # or some logic to determine the flag value

            # Adding the connections to the adjacency list
            for conn in connected_nodes:
                adjacency_list.append([node, conn, flag])

    # Now process the adjacency list as before
    node_references_count = {}
    for node, neighbor, _ in adjacency_list:
        if neighbor not in node_references_count:
            node_references_count[neighbor] = 0
        node_references_count[neighbor] += 1

    adjacencyListNumTimesReferenced = sorted(node_references_count.items(), key=lambda x: x[1], reverse=True)

    generated_spherical_coords = generateCoords(adjacencyListNumTimesReferenced, adjacency_list)

    return adjacency_list, adjacencyListNumTimesReferenced, generated_spherical_coords


#Starting from the Middle and Moving Outwards
def generateCoordsMiddle( adjacencyListNumTimesReferenced, adjacencyList):
    coordsDict = {}

    coordsDict = generateCoords(adjacencyListNumTimesReferenced, adjacencyList)

    #print(coordsDict)
    counter = 0
    columns = math.floor(math.sqrt(len(coordsDict)))+1

    coordsList = []
    for elem in coordsDict:
        coordsList.append(elem)

    permlist1 = []
    for i in range(len(coordsDict)):
        num = i + math.floor(len(coordsDict)/3)
        permlist1.append(coordsList[num % len(coordsDict)])

    permlist1 = np.array(permlist1)

    counter = 0
    for elem in permlist1:
        column = counter % columns
        row = (counter - column)/columns

        coordsDict[elem] = [2*math.pi*(column+1)/columns,(math.pi*(row+1))/(columns+1)]

        counter += 1

    return coordsDict

#Structured Arrangement of Points
def generateCoordsPrimePrime(adjacencyListNumTimesReferenced, adjacencyList):
    coordsDict = {}

    coordsDict = generateCoords(adjacencyListNumTimesReferenced, adjacencyList)

    #print(coordsDict)
    counter = 0
    columns = math.floor(math.sqrt(len(coordsDict)))+1

    coordsList = []
    for elem in coordsDict:
        coordsList.append(elem)

    permlist1 = []
    for i in range(len(coordsDict)):
        num = (29*i) % len(coordsList)
        permlist1.append( coordsList[num])

    permlist1 = np.array(permlist1)

    counter = 0
    for elem in permlist1:
        column = counter % columns
        row = (counter - column)/columns
        coordsDict[elem] = [2*math.pi*(column+1)/columns,(math.pi*(row+1))/(columns+1)]

        counter += 1



    return coordsDict


def generateCoordsTriplePrime(adjacencyListNumTimesReferenced, adjacencyList):
    coordsDict = {}

    coordsDict = generateCoords(adjacencyListNumTimesReferenced, adjacencyList)
    counter = 0
    columns = math.floor(math.sqrt(len(coordsDict)))+1

    coordsList = []

#Random Arrangement of Points
def generateCoordsPrime(adjacencyListNumTimesReferenced, adjacencyList):
    coordsDict = {}

    coordsDict = generateCoords(adjacencyListNumTimesReferenced, adjacencyList)
    counter = 0
    columns = math.floor(math.sqrt(len(coordsDict)))+1

    coordsList = []
    for elem in coordsDict:
        coordsList.append(elem)

    permlist1 = np.random.permutation(coordsList)

    counter = 0
    for elem in permlist1:
        column = counter % columns
        row = (counter - column)/columns
        print(coordsDict[elem])
        coordsDict[elem] = [2*math.pi*(column+1)/columns,(math.pi*(row+1))/(columns+1)]
        print(coordsDict[elem])
        counter += 1
    
    number = 1

    lenList = []
    for i in range(5):
        permlist3 = np.random.permutation(coordsList)
        counter = 0

        for elem in permlist3:
            column = counter % columns
            row = (counter - column)/columns

            coordsDict[elem] = [2*math.pi*(column+1)/columns,(math.pi*(row+1))/(columns+1)]
            counter += 1

        total_length = calcTotalDist(coordsDict,adjacencyList)

        lenList.append(total_length)

    intervalList = []
    for i in range(40,80,1):
        intervalList.append(i)

    plt.hist(lenList, bins = intervalList)
    plt.show()



    
    for i in range(5):
        permlist2 = np.random.permutation(coordsList)
        counter = 0
        for elem in permlist1:
            column = counter % columns
            row = (counter - column)/columns

            coordsDict[elem] = [2*math.pi*(column+1)/columns,(math.pi*(row+1))/(columns+1)]
            counter += 1
        len1 = calcTotalDist(coordsDict,adjacencyList)
        #print(len1)

        counter = 0
        for elem in permlist2:
            column = counter % columns
            row = (counter - column)/columns

            coordsDict[elem] = [2*math.pi*(column+1)/columns,(math.pi*(row+1))/(columns+1)]
            counter += 1
        len2 = calcTotalDist(coordsDict,adjacencyList)
        print(len2)
        print()

        if len2 > len1:
            permlist1 = permlist2

    counter = 0
    for elem in permlist1:
        column = counter % columns
        row = (counter - column)/columns

        coordsDict[elem] = [2*math.pi*(column+1)/columns,(math.pi*(row+1))/(columns+1)]
        counter += 1
    print()
    print(calcTotalDist(coordsDict,adjacencyList))
    return coordsDict

def compareTwoOrders(coordsDict1,coordsDict2):
    if calcTotalDist(coordsDict2) >= calcTotalDist(coordsDict1):
        return coordsDict1
    else:
        return coordsDict2

def calcTotalDist(coordsDict,adjacencyList):
    totalDist = 0
    counter = 0
    for pair in adjacencyList:
        if pair[2] == True:
            totalDist = totalDist + distFunc(coordsDict[pair[0]],coordsDict[pair[1]])
            counter += 1
    return totalDist

def distFunc(point1,point2):
    phi1 = point1[0]
    phi2 = point2[0]
    theta1 = point1[1]
    theta2 = point2[1]

    x1 = math.cos(phi2)*math.sin(theta2)
    x2 = math.sin(phi2)*math.sin(theta2)
    x3 = math.cos(theta2)

    second_point = np.array([[x1],
                             [x2],
                             [x3]])

    anti_phi_rotation = np.array([[math.cos(-phi1),-math.sin(-phi1),0],
                                  [math.sin(-phi1),math.cos(phi1),0],
                                  [0,0,1]])

    anti_theta_rotation = np.array([[math.cos(-theta1),0,math.sin(-theta1)],
                                    [0,1,0],
                                    [-math.sin(-theta1),0,math.cos(-theta1)]])

    second_point_rotated = np.dot(anti_theta_rotation,np.dot(anti_phi_rotation,second_point))

    if abs(second_point_rotated[2]-1) <= 0.0001:
        theta_value = 0
    elif abs(second_point_rotated[2]+1) <= 0.0001:
        theta_value = math.pi
    else:
        theta_value = math.acos(second_point_rotated[2])
    
    return theta_value



def generateCoords(adjacencyListNumTimesReferenced, adjacencyList):
    coordsDict = {}

    referencesMostReferenced = []
    referencesSecondMostReferenced = []

    referencesMostReferencedNumOfReferences = []
    referencesSecondMostReferencedNumOfReferences = []

    #for element in adjacencyListNumTimesReferenced:
    #    print(element)

    mostReferencedDOI = adjacencyListNumTimesReferenced[0][0]
    secondMostReferencedDOI = adjacencyListNumTimesReferenced[1][0]


    for element in adjacencyList:
        if element[1] == mostReferencedDOI:
            if element[2] == True:
                referencesMostReferenced.append(element)
        if element[1] == secondMostReferencedDOI:
            if element[2] == True:
                referencesSecondMostReferenced.append(element)


    for element in referencesMostReferenced:
        currDOI = element[0]
        counter = 0
        for item in adjacencyList:
            if item[1] == currDOI:
                if item[2] == True:
                    counter = counter + 1
        referencesMostReferencedNumOfReferences.append([currDOI,counter])

    for element in referencesSecondMostReferenced:
        currDOI = element[0]
        counter = 0
        for item in adjacencyList:
            if item[1] == currDOI:
                if item[2] == True:
                    counter = counter + 1
        
        referencesSecondMostReferencedNumOfReferences.append([currDOI,counter])

    referencesMostReferencedNumOfReferences.sort(key = sortKey)
    referencesSecondMostReferencedNumOfReferences.sort(key = sortKey)

    n1 = 7
    n2 = 2*n1
    n3 = 3*n1
    n4 = len(referencesMostReferencedNumOfReferences) - n1-n2-n3
    theta1 = math.pi/12
    buffer = math.pi/36
    theta2 = 2*theta1
    theta3 = 3*theta1
    theta4 = 4*theta1
    includedCounter = 0

    for element in referencesMostReferenced:
        includedCounter += 1

    for element in referencesSecondMostReferenced:
        inReferencesMostReferenced = False

        for elem in referencesMostReferenced:
            if elem[0] == element[0]:
                inReferencesMostReferenced = True

        if not inReferencesMostReferenced:
            includedCounter += 1

    excludedCounter = len(adjacencyListNumTimesReferenced)-includedCounter
    if debug:
        print("excludedCounter")
        print(excludedCounter)

    extraTheta = 2*math.pi/excludedCounter
        


    mostListCounter = 0
    secondMostListCounter = 0
    extraCounter = 0

    #for element in referencesMostReferenced:
    #    print(element)

    inMostListCounter = 0

    for i in range(len(adjacencyListNumTimesReferenced)):
        inMostList = False
        inSecondMostList = False

        if i == 0:
            coordsDict[mostReferencedDOI] = [0,0]
        if i == 1:
            coordsDict[secondMostReferencedDOI] = [0,math.pi]



        if i != 0 and i != 1:
            current = adjacencyListNumTimesReferenced[i][0]


            for element in referencesMostReferenced:
                if element[0] == current:
                    inMostList = True
            for element in referencesSecondMostReferenced:
                if element[0] == current:
                    inSecondMostList = True

            if inMostList:
                inMostListCounter += 1
                if mostListCounter < n1:
                    coordsDict[current] = [2*math.pi*mostListCounter/n1,theta1]
                    mostListCounter = mostListCounter + 1
                elif mostListCounter < n1 + n2:
                    coordsDict[current] = [2*math.pi*mostListCounter/n2 + buffer,theta2]
                    mostListCounter = mostListCounter + 1
                elif mostListCounter < n1 + n2 + n3:
                    coordsDict[current] = [2*math.pi*mostListCounter/n3 + 2*buffer,theta3]
                    mostListCounter = mostListCounter + 1
                else:
                    coordsDict[current] = [2*math.pi*mostListCounter/n4 + 3*buffer, theta4]
                    mostListCounter = mostListCounter + 1

            
            if inSecondMostList:
                if not inMostList:
                    if secondMostListCounter < n1:
                        coordsDict[current] = [2*math.pi*secondMostListCounter/n1,math.pi-theta1]
                        secondMostListCounter = secondMostListCounter + 1
                    elif secondMostListCounter < n1 + n2:
                        coordsDict[current] = [2*math.pi*secondMostListCounter/n2 + buffer,math.pi-theta2]
                        secondMostListCounter = secondMostListCounter + 1
                    elif secondMostListCounter < n1 + n2 + n3:
                        coordsDict[current] = [2*math.pi*secondMostListCounter/n3 + 2*buffer,math.pi-theta3]
                        secondMostListCounter = secondMostListCounter + 1
                    else:
                        coordsDict[current] = [2*math.pi*secondMostListCounter/n4 + 3*buffer, math.pi-theta4]
                        secondMostListCounter = secondMostListCounter + 1


            if i != 0 and i != 1:
                if not inMostList:
                    if not inSecondMostList:
                        coordsDict[current] = [2*math.pi*extraCounter/excludedCounter, math.pi/2]
                        extraCounter += 1

    return coordsDict

def generateCoords2(adjacencyListNumTimesReferenced, adjacencyList):
    
    adjacencyListInGraph = []

    for entry in adjacencyList:
        if entry[2] == True:
            adjacencyListInGraph.append(entry)


    coordsDict = generateCoords(adjacencyListNumTimesReferenced, adjacencyList)

    for element in coordsDict:

        coordsDict[element] = [2*math.pi*random.random(),math.pi*random.random()]

    surfaceArea = 4*math.pi

    k = math.sqrt(surfaceArea/len(adjacencyListNumTimesReferenced))

    vertexList = []

    for element in coordsDict:
        phi = coordsDict[element][0]
        theta = coordsDict[element][1]

        x = math.cos(phi)*math.sin(theta)
        y = math.sin(phi)*math.sin(theta)
        z = math.cos(theta)

        vertexList.append([[x,y,z],[0,0,0],element])


    for i in range(200):
        for v in vertexList: 
            v[1] = [0,0,0]
            for u in vertexList:
                if u[0][0] != v[0][0] or u[0][1] != v[0][1] or u[0][2] != v[0][2]:

                    delta = [v[0][0]-u[0][0],v[0][1]-u[0][1],v[0][2]-u[0][2]]
                    deltalength = math.sqrt(math.pow(v[0][0]-u[0][0],2)+math.pow(v[0][1]-u[0][1],2)+math.pow(v[0][2]-u[0][2],2))
                    for element in delta:
                        element = element/deltalength * math.pow(k,2)/deltalength


                    v[1][0] = v[1][0] + repulsiveForceStrength*delta[0]
                    v[1][1] = v[1][1] + repulsiveForceStrength*delta[1]
                    v[1][2] = v[1][2] + repulsiveForceStrength*delta[2]
        
        for e in adjacencyListInGraph:

            u = e[0]
            v = e[1]

            for element in vertexList:
                if element[2] == u:
                    u = element
                if element[2] == v:
                    v = element

            delta = [v[0][0]-u[0][0],v[0][1]-u[0][1],v[0][2]-u[0][2]]
            deltalength = math.sqrt(math.pow(v[0][0]-u[0][0],2)+math.pow(v[0][1]-u[0][1],2)+math.pow(v[0][2]-u[0][2],2))


            for element in delta:
                element = element/deltalength * math.pow(deltalength,2)/k


            v[1][0] = v[1][0]-attractiveForce*delta[0]
            v[1][1] = v[1][1]-attractiveForce*delta[1]
            v[1][2] = v[1][2]-attractiveForce*delta[2]

            u[1][0] = u[1][0]+attractiveForce*delta[0]
            u[1][1] = u[1][1]+attractiveForce*delta[1]
            u[1][2] = u[1][2]+attractiveForce*delta[2]

        for v in vertexList:

            dispVec = [v[1][0],v[1][1],v[1][2]]
            dispVecLen = math.sqrt(math.pow(v[1][0],2)+math.pow(v[1][1],2)+math.pow(v[1][2],2))
            dispVec = [dispVec[0]/dispVecLen,dispVec[1]/dispVecLen,dispVec[2]/dispVecLen]

            v[0][0] = v[0][0] + dispVec[0]
            v[0][1] = v[0][1] + dispVec[1]
            v[0][2] = v[0][2] + dispVec[2]

    for element in vertexList:
        cartCoords = element[0]

        x = cartCoords[0]
        y = cartCoords[1]
        z = cartCoords[2]
        length = math.sqrt(math.pow(x,2) + math.pow(y,2) + math.pow(z,2))

        xNorm = x/length
        yNorm = y/length
        zNorm = z/length

        theta = math.acos(zNorm)

        phi = math.atan2(yNorm,xNorm)

        coordsDict[element[2]] = [phi,theta]
    
    return coordsDict

def generateCoords3(adjacencyListNumTimesReferenced, adjacencyList):
    
    adjacencyListInGraph = []

    for entry in adjacencyList:
        if entry[2] == True:
            adjacencyListInGraph.append(entry)


    coordsDict = generateCoords(adjacencyListNumTimesReferenced, adjacencyList)

    for element in coordsDict:

        coordsDict[element] = [2*math.pi*random.random(),math.pi*random.random()]

    surfaceArea = 4*math.pi

    eqAngle = math.sqrt(surfaceArea/len(adjacencyListNumTimesReferenced))

    vertexList = []

    for element in coordsDict:
        phi = coordsDict[element][0]
        theta = coordsDict[element][1]

        x = math.cos(phi)*math.sin(theta)
        y = math.sin(phi)*math.sin(theta)
        z = math.cos(theta)

        vertexList.append([[x,y,z],[0,0,0],element])



    for i in range(25):
        #print(i)
        for v in vertexList: 
            v[1] = [0,0,0]
            for u in vertexList:
                if u[0][0] != v[0][0] or u[0][1] != v[0][1] or u[0][2] != v[0][2]:

                    delta, arcLength = calcDisp(u[0],v[0])
                    deltaLength = math.sqrt(math.pow(delta[0],2) + math.pow(delta[1],2) + math.pow(delta[2],2))
                    
                    for i in range(len(delta)):
                        delta[i] = delta[i]/deltaLength

                    repulsiveForceStrength = 1
                    correctionStrength = math.pow(eqAngle,2)/arcLength

                    v[1][0] = v[1][0] + repulsiveForceStrength*delta[0]*correctionStrength
                    v[1][1] = v[1][1] + repulsiveForceStrength*delta[1]*correctionStrength
                    v[1][2] = v[1][2] + repulsiveForceStrength*delta[2]*correctionStrength
        
        for e in adjacencyListInGraph:

            u = e[0]
            v = e[1]

            for element in vertexList:
                if element[2] == u:
                    u = element
                if element[2] == v:
                    v = element

            delta, arcLength = calcDisp(u[0],v[0])
            deltaLength = math.sqrt(math.pow(delta[0],2) + math.pow(delta[1],2) + math.pow(delta[2],2))


            correctionStrength = math.pow(arcLength,2)/eqAngle
            attractiveForce = 1

            v[1][0] = v[1][0]-attractiveForce*delta[0]*correctionStrength
            v[1][1] = v[1][1]-attractiveForce*delta[1]*correctionStrength
            v[1][2] = v[1][2]-attractiveForce*delta[2]*correctionStrength

            u[1][0] = u[1][0]+attractiveForce*delta[0]*correctionStrength
            u[1][1] = u[1][1]+attractiveForce*delta[1]*correctionStrength
            u[1][2] = u[1][2]+attractiveForce*delta[2]*correctionStrength
        dispVecLenAverage = 0
        for v in vertexList:

            dispVec = [v[1][0],v[1][1],v[1][2]]
            #dispVecLen = max(i+1,math.sqrt(math.pow(v[1][0],2)+math.pow(v[1][1],2)+math.pow(v[1][2],2)))
            dispVecLen = math.sqrt(math.pow(v[1][0],2)+math.pow(v[1][1],2)+math.pow(v[1][2],2))
            dispVec = [dispVec[0]/dispVecLen,dispVec[1]/dispVecLen,dispVec[2]/dispVecLen]
            dispVecLenAverage += dispVecLen
            v[0][0] = v[0][0] + dispVec[0]*dispVecLen
            v[0][1] = v[0][1] + dispVec[1]*dispVecLen
            v[0][2] = v[0][2] + dispVec[2]*dispVecLen
        dispVecLenAverage = dispVecLenAverage/len(vertexList)
    for element in vertexList:
        cartCoords = element[0]

        x = cartCoords[0]
        y = cartCoords[1]
        z = cartCoords[2]
        length = math.sqrt(math.pow(x,2) + math.pow(y,2) + math.pow(z,2))

        #Find the normal lengths
        xNorm = x/length
        yNorm = y/length
        zNorm = z/length

        theta = math.acos(zNorm)

        phi = math.atan2(yNorm,xNorm)

        coordsDict[element[2]] = [phi,theta]

    return coordsDict

def generateCoords4(adjacencyListNumTimesReferenced, adjacencyList):
    
    adjacencyListInGraph = []

    for entry in adjacencyList:
        if entry[2] == True:
            adjacencyListInGraph.append(entry)


    coordsDict = generateCoords(adjacencyListNumTimesReferenced, adjacencyList)

    for element in coordsDict:

        coordsDict[element] = [2*math.pi*random.random(),math.pi*random.random()]

    surfaceArea = 4*math.pi

    eqAngle = math.sqrt(surfaceArea/len(adjacencyListNumTimesReferenced))

    vertexList = []

    for element in coordsDict:
        phi = coordsDict[element][0]
        theta = coordsDict[element][1]

        x = math.cos(phi)*math.sin(theta)
        y = math.sin(phi)*math.sin(theta)
        z = math.cos(theta)

        vertexList.append([[x,y,z],[0,0,0],element])



    for i in range(25):
        #print(i)
        for v in vertexList: 
            v[1] = [0,0,0]
            for u in vertexList:
                if u[0][0] != v[0][0] or u[0][1] != v[0][1] or u[0][2] != v[0][2]:


                    #calcDisp = [delta vector at v directly away from u, length of arc between v and u]
                    delta, arcLength = calcDisp(u[0],v[0])
                    deltaLength = math.sqrt(math.pow(delta[0],2) + math.pow(delta[1],2) + math.pow(delta[2],2))
                    
                    for i in range(len(delta)):
                        delta[i] = delta[i]/deltaLength

                    repulsiveForceStrength = 1/(2*i)
                    correctionStrength = math.pow(eqAngle,2)/arcLength

                    v[1][0] = v[1][0] + repulsiveForceStrength*delta[0]*correctionStrength
                    v[1][1] = v[1][1] + repulsiveForceStrength*delta[1]*correctionStrength
                    v[1][2] = v[1][2] + repulsiveForceStrength*delta[2]*correctionStrength
        
        for e in adjacencyListInGraph:

            u = e[0]
            v = e[1]

            for element in vertexList:
                if element[2] == u:
                    u = element
                if element[2] == v:
                    v = element

            
            delta, arcLength = calcDisp(u[0],v[0])
            deltaLength = math.sqrt(math.pow(delta[0],2) + math.pow(delta[1],2) + math.pow(delta[2],2))


            correctionStrength = math.pow(arcLength,2)/eqAngle
            attractiveForce = 1/(2*i)

            v[1][0] = v[1][0]-attractiveForce*delta[0]*correctionStrength
            v[1][1] = v[1][1]-attractiveForce*delta[1]*correctionStrength
            v[1][2] = v[1][2]-attractiveForce*delta[2]*correctionStrength

            u[1][0] = u[1][0]+attractiveForce*delta[0]*correctionStrength
            u[1][1] = u[1][1]+attractiveForce*delta[1]*correctionStrength
            u[1][2] = u[1][2]+attractiveForce*delta[2]*correctionStrength
        dispVecLenAverage = 0
        for v in vertexList:

            dispVec = v[1]
            
            x = calcActualDispVec(v[0],v[1])

            for i in range(len(dispVec)):
                dispVec[i] =  x[i]-v[0][i]

            dispVecLen = math.sqrt(math.pow(v[1][0],2)+math.pow(v[1][1],2)+math.pow(v[1][2],2))
            dispVec = [dispVec[0]/dispVecLen,dispVec[1]/dispVecLen,dispVec[2]/dispVecLen]
            dispVecLenAverage += dispVecLen

            v[0][0] = v[0][0] + dispVec[0]*dispVecLen
            v[0][1] = v[0][1] + dispVec[1]*dispVecLen
            v[0][2] = v[0][2] + dispVec[2]*dispVecLen


        dispVecLenAverage = dispVecLenAverage/len(vertexList)
    for element in vertexList:
        cartCoords = element[0]

        x = cartCoords[0]
        y = cartCoords[1]
        z = cartCoords[2]
        length = math.sqrt(math.pow(x,2) + math.pow(y,2) + math.pow(z,2))

        xNorm = x/length
        yNorm = y/length
        zNorm = z/length

        theta = math.acos(zNorm)

        phi = math.atan2(yNorm,xNorm)

        coordsDict[element[2]] = [phi,theta]
    
    return coordsDict


def calcActualDispVec(v_1,v_2):

    #Get the (x,y,z) cooredinates of each point.
    coord_1 = np.array([[v_1[0]],[v_1[1]],[v_1[2]]])
    coord_2 = np.array([[v_2[0]],[v_2[1]],[v_2[2]]])

    #Find the normal vector using the cross product 
    normal_vector = [coord_1[1][0]*coord_2[2][0]-coord_1[2][0]*coord_2[1][0], coord_1[2][0]*coord_2[0][0]-coord_1[0][0]*coord_2[2][0], coord_1[0][0]*coord_2[1][0]-coord_1[1][0]*coord_2[0][0]]

    #Scale the normal vector down to length 1
    length_normal = math.sqrt(math.pow(normal_vector[0],2)+math.pow(normal_vector[1],2)+math.pow(normal_vector[2],2))
    normal_vector_unit = [normal_vector[0]/length_normal,normal_vector[1]/length_normal,normal_vector[2]/length_normal]
    
    #Unit version of the normal vector
    normal_vector_unit = np.array([[normal_vector_unit[0]],
                                    [normal_vector_unit[1]],
                                    [normal_vector_unit[2]]])

    #ax+by+cz = 0
    a = normal_vector_unit[0][0]
    b = normal_vector_unit[1][0]
    c = normal_vector_unit[2][0]


    #Find the necessary angle to rotate the normal vector onto the xz plane. After this, y should be 0 for the normal vector
    if (b == 0 and a == -1):
        angle_1 = math.pi
    elif (b == 0 and a == 1):
        angle_1 = 0    
    elif (a == 0):
        angle_1 = math.pi/2
    else:
        angle_1 = math.atan2(b,a)

    rot_matrix_1 = np.array([[math.cos(-angle_1),-math.sin(-angle_1),0],
                                [math.sin(-angle_1),math.cos(-angle_1),0],
                                [0,0,1]])

    normal_vector_1 = np.dot(rot_matrix_1, normal_vector_unit)

    #After rotating the normal vector onto the xz plane.
    point1_step_1_matrix = np.dot(rot_matrix_1,coord_1)
    point2_step_1_matrix = np.dot(rot_matrix_1,coord_2)

    #Finding out the angle of inclination/declination of the normal vector
    angle_2 = math.asin(c)
    angle_2 = math.pi/2-angle_2

    positiveIndicator = False
    if (normal_vector_1[0][0] >= 0):
        positiveIndicator = True

    if not positiveIndicator:
        rot_matrix_2 = np.array([[math.cos(angle_2),0,math.sin(angle_2)],
                                    [0,1,0],
                                    [-math.sin(angle_2),0,math.cos(angle_2)]])
    else:
        rot_matrix_2 = np.array([[math.cos(-angle_2),0,math.sin(-angle_2)],
                                    [0,1,0],
                                    [-math.sin(-angle_2),0,math.cos(-angle_2)]])


    normal_vector_2 = np.dot(rot_matrix_2, normal_vector_1)
    point1_step_2_matrix = np.dot(rot_matrix_2, point1_step_1_matrix)
    point2_step_2_matrix = np.dot(rot_matrix_2, point2_step_1_matrix)



    angleFirstPoint = math.atan2(point1_step_2_matrix[1],point1_step_2_matrix[0])
    angleSecondPoint = math.atan2(point2_step_2_matrix[1],point2_step_2_matrix[0])

    rot_matrix_3 = np.array([[math.cos(-angleFirstPoint),-math.sin(-angleFirstPoint),0],
                                [math.sin(-angleFirstPoint),math.cos(-angleFirstPoint),0],
                                [0,0,1]])

    point1_step_3_matrix = np.dot(rot_matrix_3, point1_step_1_matrix)
    point2_step_3_matrix = np.dot(rot_matrix_3, point2_step_2_matrix)
    lenTangentVector = math.sqrt(math.pow(coord_2[0][0],2)+math.pow(coord_2[1][0],2)+math.pow(coord_2[2][0],2))
    if point2_step_3_matrix[1] < 0:
        angleFirstPoint = angleFirstPoint-(lenTangentVector/10)
    else:
        angleFirstPoint = angleFirstPoint + lenTangentVector/10

    corrVector = np.array([math.cos(angleFirstPoint),math.sin(angleFirstPoint),0])

    if not positiveIndicator:
        rot_matrix_2_inverse = np.array([[math.cos(-angle_2),0,math.sin(-angle_2)],
                                    [0,1,0],
                                    [-math.sin(-angle_2),0,math.cos(-angle_2)]])
    else:
        rot_matrix_2_inverse = np.array([[math.cos(angle_2),0,math.sin(angle_2)],
                                    [0,1,0],
                                    [-math.sin(angle_2),0,math.cos(angle_2)]])

    rot_matrix_1_inverse = np.array([[math.cos(angle_1),-math.sin(angle_1),0],
                                    [math.sin(angle_1),math.cos(angle_1),0],
                                    [0,0,1]])

    corrVector = np.dot(rot_matrix_2_inverse,corrVector)
    corrVector = np.dot(rot_matrix_1_inverse,corrVector)


    return corrVector

    




def terminalPointsOffSphere(adjacencyListNumTimesReferenced, adjacencyList):

    coordsDict = generateCoordsPrimePrime(adjacencyListNumTimesReferenced, adjacencyList)

    adjacencyList.sort(key=sortKey2)

    adjacencyListNumOfReferences = []

    prevDoi = "999"
    firstTime = True

    for element in adjacencyList:
        if element[2] == True:
            if prevDoi != element[0]:
                if firstTime == False:
                    adjacencyListNumOfReferences.append([prevDoi,counter])
                firstTime = False
                counter = 1
                prevDoi = element[0]
            else:
                counter += 1 
        
    adjacencyListNumOfReferences.append([prevDoi,counter])


    

    adjacencyList.sort(key=sortKey)




    adjacencyListNumOfReferences.sort(key=sortKey,reverse = True)


    offSphereLinesList = []
    offSpherePointsList = []

    for element in adjacencyListNumTimesReferenced:
        name = element[0]
        initTotal = element[1]
        total = element[1]
        for elem in adjacencyListNumOfReferences:
            if elem[0] == name:
                total += elem[1]
        if total == 0:
            coordsDict.pop(element[0])
        if total == 1:
            if initTotal ==  1:
                for triple in adjacencyList:
                    if triple[2] == True:
                        if triple[1] == name:
                            offSphereLinesList.append([triple[0],triple[1],1])
                            offSpherePointsList.append(name)
            else:
                for triple in adjacencyList:
                    if triple[2] == True:
                        if triple[0] == name:
                            offSphereLinesList.append([triple[0],triple[1],0])
                            offSpherePointsList.append(name)


    var = 0
    for elem1 in offSpherePointsList:
        for elem2 in offSpherePointsList:
            for elem in offSphereLinesList:
                if elem[0] == elem1 and elem[1] == elem2:
                    var = var
                elif elem[1] == elem1 and elem[0] == elem2:
                    var = var
                else:
                    if elem1 in coordsDict:
                        coordsDict.pop(elem1)
                    if elem2 in coordsDict:
                        coordsDict.pop(elem2)

    offPointsDict = {}

    for elem in offSphereLinesList:
        if elem[2] == 0:
            if elem[1] in offPointsDict:
                offPointsDict[elem[1]].append(elem[0])
            else:
                offPointsDict[elem[1]] = [elem[0]]
        else:
            if elem[0] in offPointsDict:
                offPointsDict[elem[0]].append(elem[1])
            else:
                offPointsDict[elem[0]] = [elem[1]]

    

    offSphereCoordsDict = {}
    for element in offPointsDict:
        phi, theta = coordsDict[element]

        inv_phi_matrix = np.array([[math.cos(phi),-math.sin(phi),0],
                                  [math.sin(phi),math.cos(phi),0],
                                  [0,0,1]])

        inv_theta_matrix = np.array([[math.cos(theta),0,math.sin(theta)],
                                     [0,1,0],
                                     [-math.sin(theta),0,math.cos(theta)]])

        r = 1.3

        stepAngle = 2*math.pi/len(offPointsDict[element])
        print(stepAngle)

        for i in range(0,len(offPointsDict[element])):

            tempElem = np.array([[r*math.cos(i*stepAngle)*math.sin(math.pi/36)],
                                [r*math.sin(i*stepAngle)*math.sin(math.pi/36)],
                                [r*math.cos(math.pi/36)]])

            offSphereCoordsDict[offPointsDict[element][i]] = [np.dot(inv_phi_matrix,np.dot(inv_theta_matrix,tempElem))[0][0],np.dot(inv_phi_matrix,np.dot(inv_theta_matrix,tempElem))[1][0],np.dot(inv_phi_matrix,np.dot(inv_theta_matrix,tempElem))[2][0]]

    print(offSphereCoordsDict)

    with open('C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\SupportFiles\\OffSpherePoints.vtk', 'w', encoding="utf8") as g:

        radSphere = 0.015
        listLength = len(offSphereCoordsDict)
        n=16

        #Header
        g.write("# vtk DataFile Version 3.0\n")
        g.write("fieldline polygons\n")
        g.write("ASCII\n")
        g.write("DATASET POLYDATA\n")
        g.write("POINTS " + str(listLength*(n*(n-1)+2)) + " float64\n")

        with open('./GeneratedOffSphereCoords.txt', 'w', encoding="utf8") as h:
            for element in offSphereCoordsDict:

                x = offSphereCoordsDict[element][0]
                y = offSphereCoordsDict[element][1]
                z = offSphereCoordsDict[element][2]
                h.write(str(x) + " " + str(y) + " " + str(z) + "\n")
                writePointsForOneSphere(x,y,z,radSphere,g,n)
        h.close()

        g.write("POLYGONS " + str(n*n*listLength) + " " + str(listLength*(4*n+5*(n-2)*n+4*n)) + "\n")

        shift = 0
        for element in offSphereCoordsDict:
            x = offSphereCoordsDict[element][0]
            y = offSphereCoordsDict[element][1]
            z = offSphereCoordsDict[element][2]
            writePolygons(g,shift,n)
            shift += 1


        #Ending
        g.write("POINT_DATA " + str(listLength*(n*(n-1)+2)) + "\n")
        g.write("CELL_DATA " + str(listLength*n*n) + "\n")
        g.write("SCALARS cell_Scalars int 1" + "\n") 
        g.write("LOOKUP_TABLE default" + "\n")

        #White color at the end

        for i in range(listLength*n*n):
            g.write("5\n")

    g.close()

    lineCoordsList = []

    for element in offSphereLinesList:
        if element[2] == 0:
            phi, theta = coordsDict[element[1]]

            x = math.cos(phi)*math.sin(theta)
            y = math.sin(phi)*math.sin(theta)
            z = math.cos(theta)

            lineCoordsList.append([offSphereCoordsDict[element[0]][0],offSphereCoordsDict[element[0]][1],offSphereCoordsDict[element[0]][2],x,y,z])
        else:
            phi, theta = coordsDict[element[0]]

            x = math.cos(phi)*math.sin(theta)
            y = math.sin(phi)*math.sin(theta)
            z = math.cos(theta)

            lineCoordsList.append([x,y,z,offSphereCoordsDict[element[1]][0],offSphereCoordsDict[element[1]][1],offSphereCoordsDict[element[1]][2]])

    numOfSpaces = 64

    with open('./OffSphereLines.vtk', "w", encoding="utf8") as h:
        h.write("# vtk DataFile Version 3.0\n")
        h.write("fieldline polygons\n")
        h.write("ASCII\n")
        h.write("DATASET POLYDATA\n")
        h.write("POINTS " + str(len(lineCoordsList)*(numOfSpaces+1)) + " float64\n")

        for pair in lineCoordsList:

            x_1 = pair[0]
            y_1 = pair[1]
            z_1 = pair[2]
            x_2 = pair[3]
            y_2 = pair[4]
            z_2 = pair[5]        


            emphasizeIndicator = False

            createArc(h,x_1,y_1,z_1,x_2,y_2,z_2,numOfSpaces)


        h.write("LINES " + str(len(lineCoordsList)) + " " + str(len(lineCoordsList)*(numOfSpaces+2)) + "\n")

        counter = 0
        for i in range(len(lineCoordsList)):
            output = str(numOfSpaces+1) + " "
            for i in range(numOfSpaces+1):
                output += str(counter) + " "
                counter = counter+1
            h.write(output + "\n")




        h.write("POINT_DATA " + str((numOfSpaces+1)*len(lineCoordsList)) + "\n")
        h.write("SCALARS cell_Scalars int 1" + "\n") 
        h.write("LOOKUP_TABLE default" + "\n")





        for i in range(len(lineCoordsList)):
            for j in range(math.floor((numOfSpaces+1)/2)):
                h.write("3\n")
            for j in range(numOfSpaces+1-math.floor((numOfSpaces+1)/2)):
                h.write("7\n")


    
    h.close



    return coordsDict

def createArc(h,x_1,y_1,z_1,x_2,y_2,z_2,numOfSpaces):
    shiftx = (x_2-x_1)/numOfSpaces
    shifty = (y_2-y_1)/numOfSpaces
    shiftz = (z_2-z_1)/numOfSpaces

    for i in range(numOfSpaces+1):
        h.write(str(x_1 + shiftx*i) + " " + str(y_1 + shifty*i) + " " + str(z_1 + shiftz*i) + "\n")


def writePolygons(f,shift,n):

    addValue = shift*(n*(n-1)+2)

    for x in range(1,n):
        f.write(str(3) + " " + str(addValue) + " " + str(x+addValue) + " " + str(x+addValue+1) + "\n")
    f.write(str(3) + " " + str(addValue) + " " + str(n+addValue) + " " + str(1+addValue) + "\n")

    for x in range(n-2):
        for y in range(1,n):
            f.write(str(4) + " " + str(n*x+y+addValue) + " " + str(n*x+y + addValue + 1) + " " + str(n*(x+1)+y+addValue + 1) + " " + str(n*(x+1)+y+ addValue) + "\n")
        f.write(str(4) + " " + str(n*(x+1) + addValue) + " " + str(n*x+addValue + 1) + " " + str(n*(x+1)+addValue + 1) + " " + str(n*(x+2)+addValue) + "\n")

    for x in range(n-1):
        f.write(str(3) + " " + str(n*(n-1)+addValue + 1) + " " + str((n-1)*(n-1)+x+addValue + 1) + " " + str((n-1)*(n-1)+addValue + x) + "\n")
    f.write(str(3) + " " + str(n*(n-1)+addValue + 1) + " " + str(n*(n-1)+addValue) + " " + str((n-1)*(n-1)+addValue) + "\n")


            
    
def writePointsForOneSphere(x,y,z,r,f,n):

        xcoord = x
        ycoord = y
        zcoord = z
        #Write the coord of the top point
        f.write(str(xcoord) + " " + str(ycoord) + " " + str(zcoord + r) + "\n")

        #In concentric circles, write the coordinates of all the points in the middle
        for x in range(1,n):
            for y in range(n):
                f.write(str(r*math.cos(2*math.pi*y/n)*math.sin(math.pi*x/n)+xcoord) + " " + str(r*math.sin(2*math.pi*y/n)*math.sin(math.pi*x/n)+ycoord) + " " + str(r*math.cos(math.pi*x/n)+zcoord) + "\n")

        #Write the coord of the bottom point
        f.write(str(xcoord) + " " + str(ycoord) + " " + str(zcoord-r) + "\n")



def calcDisp(firstPoint, secondPoint):
    ind = 0

    #Get the (x,y,z) cooredinates of each point.
    coord_1 = np.array([[firstPoint[0]],[firstPoint[1]],[firstPoint[2]]])
    coord_2 = np.array([[secondPoint[0]],[secondPoint[1]],[secondPoint[2]]])

    #Find the normal vector using the cross product 
    normal_vector = [coord_1[1][0]*coord_2[2][0]-coord_1[2][0]*coord_2[1][0], coord_1[2][0]*coord_2[0][0]-coord_1[0][0]*coord_2[2][0], coord_1[0][0]*coord_2[1][0]-coord_1[1][0]*coord_2[0][0]]

    
    #Scale the normal vector down to length 1
    length_normal = math.sqrt(math.pow(normal_vector[0],2)+math.pow(normal_vector[1],2)+math.pow(normal_vector[2],2))
    normal_vector_unit = [normal_vector[0]/length_normal,normal_vector[1]/length_normal,normal_vector[2]/length_normal]
    
    #Unit version of the normal vector
    normal_vector_unit = np.array([[normal_vector_unit[0]],
                                    [normal_vector_unit[1]],
                                    [normal_vector_unit[2]]])

    #ax+by+cz = 0
    a = normal_vector_unit[0][0]
    b = normal_vector_unit[1][0]
    c = normal_vector_unit[2][0]

    #Find the necessary angle to rotate the normal vector onto the xz plane. After this, y should be 0 for the normal vector
    if (b == 0 and a == -1):
        angle_1 = math.pi
    elif (b == 0 and a == 1):
        angle_1 = 0    
    elif (a == 0):
        angle_1 = math.pi/2
    else:
        angle_1 = math.atan2(b,a)

    rot_matrix_1 = np.array([[math.cos(-angle_1),-math.sin(-angle_1),0],
                                [math.sin(-angle_1),math.cos(-angle_1),0],
                                [0,0,1]])

    normal_vector_1 = np.dot(rot_matrix_1, normal_vector_unit)

    #After rotating the normal vector onto the xz plane.
    point1_step_1_matrix = np.dot(rot_matrix_1,coord_1)
    point2_step_1_matrix = np.dot(rot_matrix_1,coord_2)

    #Finding out the angle of inclination/declination of the normal vector
    angle_2 = math.asin(c)
    angle_2 = math.pi/2-angle_2

    positiveIndicator = False
    if (normal_vector_1[0][0] >= 0):
        positiveIndicator = True

    if not positiveIndicator:
        rot_matrix_2 = np.array([[math.cos(angle_2),0,math.sin(angle_2)],
                                    [0,1,0],
                                    [-math.sin(angle_2),0,math.cos(angle_2)]])
    else:
        rot_matrix_2 = np.array([[math.cos(-angle_2),0,math.sin(-angle_2)],
                                    [0,1,0],
                                    [-math.sin(-angle_2),0,math.cos(-angle_2)]])


    normal_vector_2 = np.dot(rot_matrix_2, normal_vector_1)
    point1_step_2_matrix = np.dot(rot_matrix_2, point1_step_1_matrix)
    point2_step_2_matrix = np.dot(rot_matrix_2, point2_step_1_matrix)


    angleFirstPoint = math.atan2(point1_step_2_matrix[1],point1_step_2_matrix[0])
    angleSecondPoint = math.atan2(point2_step_2_matrix[1],point2_step_2_matrix[0])

    if abs(angleSecondPoint-angleSecondPoint) < math.pi:
        angleDiff = abs(angleSecondPoint-angleFirstPoint)
    else:
        angleDiff = 2*math.pi-abs(angleSecondPoint-angleFirstPoint)

    if (angleFirstPoint >= angleSecondPoint):
        corrVector = np.array([math.sin(angleSecondPoint),math.cos(angleSecondPoint),0])
    else:
        corrVector = np.array([-math.sin(angleSecondPoint),-math.cos(angleSecondPoint),0])

    print(corrVector)

    if not positiveIndicator:
        rot_matrix_2_inverse = np.array([[math.cos(-angle_2),0,math.sin(-angle_2)],
                                    [0,1,0],
                                    [-math.sin(-angle_2),0,math.cos(-angle_2)]])
    else:
        rot_matrix_2_inverse = np.array([[math.cos(angle_2),0,math.sin(angle_2)],
                                    [0,1,0],
                                    [-math.sin(angle_2),0,math.cos(angle_2)]])

    rot_matrix_1_inverse = np.array([[math.cos(angle_1),-math.sin(angle_1),0],
                                    [math.sin(angle_1),math.cos(angle_1),0],
                                    [0,0,1]])

    corrVector = np.dot(rot_matrix_2_inverse,corrVector)
    corrVector = np.dot(rot_matrix_1_inverse,corrVector)


    return corrVector, angleDiff


def isConn(adjacencyListInGraph,u,v):
    for element in adjacencyListInGraph:
        if element[0] == u:
            if element[1] == v:
                return True
    return False



def sortKey(e):
    return e[1]

def sortKey2(e):
    return e[0]

#Adds onto the adjacency list and turns each set of references into a numbered dictionary.
def parseReferences(articleDOI,references, adjacencyList):

    #Trims off the braces from each end of articleDOI
    articleDOI = articleDOI[0:len(articleDOI)]

    #Splits the references by the newline character.
    refList = re.split(r'\n',references.strip())

    #Creates the numbered dictionary for the Cited_References field
    rDict = {}
    counter = 0
    for ref in refList:
        counter += 1
        rDict[str(counter)] = ref
    
    #If the articles actually has a DOI, a pair of the form [article DOI, citation DOI] will appear in the adjacencyList
    if articleDOI != "999":
        for i in range(len(rDict)):
            if rDict[str(i+1)].find("DOI") != -1:
                doipiece = rDict[str(i+1)][rDict[str(i+1)].find("DOI")+4:len(rDict[str(i+1)])-1]
                adjacencyList.append([articleDOI, doipiece])

    return rDict, adjacencyList

#if __name__ == '__main__':
#    parseBibtexEntry()