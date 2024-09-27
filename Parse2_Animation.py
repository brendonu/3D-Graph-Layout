import re
from sys import addaudithook, float_repr_style
import math
import random
import numpy as np
from matplotlib import pyplot as plt
from typing import List

debug = False
attractiveForce = 0
repulsiveForceStrength = 1
attractiveForceStrength = 1

# Parse a single bibtex citation, store each entry in the citation as a key-value pair.
# Store references as a numbered dictionary instead of as one large string.
def parseBibtexEntry():

    #Dictionary to store each entry in the bibtex as a separate key-value pair.
    articlesDict = {}

    #dictionary for single entry
    articleDict = {}

    with open('./gyrorecs.bib', encoding="utf8") as f:
        
        #Indicators for what is being entered/updated right now.
        pubType = ""
        nameIndicator = False
        fieldIndicator = False
        fieldValueIndicator = False

        #Initial values
        stack = []
        adjacencyList = []
        #Current number of brackets
        currVal = 0
        #Number of brackets at the time of the previous letter
        prevVal = 0
        #Name of the article
        articleName = ""
        #Indicator for whether the reader is on the name (first element of articleDict) or on something else
        counter = 0
        #The field to be entered as a key in the articleDict
        field = ""
        #The corresponding value that becomes a value in the articleDict
        fieldValue = ""

        #Loop over each letter in the whole txt or bib file
        for line in f.readlines()[1:-1]:
            for element in line[0:len(line):1]:

                #If new bracket opens, add one to currVal and update prevVal
                if element == "{":
                    stack.append("{")
                    prevVal = currVal
                    currVal = len(stack)
                #If bracked closes, subtract one from currVal and update prevVal
                elif element == "}":
                    stack.pop()
                    prevVal = currVal
                    currVal = len(stack)
                #If neither, just update prevVal
                else:
                    prevVal = currVal
                
                #For the first time we encounter a comma, the stuff before the comma is the article name.
                if (element == "," and prevVal == 1 and currVal == 1 and counter == 0):
                    nameIndicator = False
                    articleName = articleName.strip()
                    counter += 1
                    fieldIndicator = True

                #After the first time encountering a comma, we only obtain commas if we have defined both the field
                #and the field value for a particular field. In this step we add the field:fieldValues as a key-value
                #pair.
                if (element == "," and prevVal == 1 and currVal == 1 and counter == 1):
                    fieldValueIndicator = False
                    fieldValue = fieldValue.strip()
                    fieldValue = fieldValue[0:len(fieldValue)-1]
                    fieldValue = fieldValue.strip()

                    #Separate out the references into another dictionary and add on to the adjacencyList with pairs of nodes.
                    if field == "Cited-References":
                        fieldValue, adjacencyList = parseReferences(articleDict["DOI"],fieldValue,adjacencyList)
                    #Add name field. Also, pre-add the DOI field where "999" is a placeholder for "no DOI yet".
                    if len(articleDict) == 0:
                        articleDict["Name"] = articleName
                        articleDict["DOI"] = "999"
                    else:
                        articleDict[field] = fieldValue
                    articleDict["pubType"] = pubType
                    field = ""
                    fieldValue = ""
                    fieldIndicator = True

                #Identifies the end of a field by an equals sign, and strips/cleans the field
                if (element == "=" and prevVal == 1 and currVal == 1):
                    fieldIndicator = False
                    field = field.strip()
                    field = field[2:len(field)]
                
                #when the name indicator is on, the article name is updated for every new letter.
                if nameIndicator:
                    articleName += element

                #When the field value indictor is on, the field value is updated for every new letter.
                if fieldValueIndicator:
                    fieldValue += element

                #When the field indicator is on, the field string is updated for every new letter.
                if fieldIndicator:
                    field += element
                
                #Detects the start of the "name" field.
                if (prevVal == 0 and currVal == 1 and counter == 0):
                    
                    endChar = line.find("{")
                    pubType = line[1:endChar]

                    #if line[0:13] == "@inproceedings":
                    #    articleIndicator = 0
                    nameIndicator = True

                #Detects the start of every field value entry other than the name field.
                if (prevVal == 1 and currVal == 2):
                    fieldValueIndicator = True
                    

                #Detects when the entire citation for a single article entry is complete. Adds the accumulated
                #articleDict to articlesDict, then resets articleDict. Process repeats for each complete bibtex entry
                #in the file.
                if (prevVal == 1 and currVal == 0):
                    articlesDict[articleDict["Name"]] = articleDict
                    nameIndicator = False
                    fieldIndicator = False
                    fieldValueIndicator = False

                    
                    stack = []
                    currVal = 0
                    prevVal = 0
                    articleName = ""
                    counter = 0
                    field = ""
                    fieldValue = ""
                    articleDict = {}
        f.close()

        #Starts out by assuming that every element in adjacency List has both pairs as articles within the file.
        for element in adjacencyList:
            element.append(True)
            #print(element)

        #List of the doi's of the articles within the file that actually have doi's.
        doiList = []

        #Goes through each element in articlesDict. If that element has a valid DOI, it adds that DOI to doiList.
        try:
            for element in articlesDict:
                if articlesDict[element]["DOI"] != "999":
                    doiString = articlesDict[element]["DOI"]
                    elementDOI = doiString[0:len(doiString)]
                    doiList.append(elementDOI)

        except:
            print("EXCEPTION")
            print(articlesDict[element])
        
        #for element in doiList:
        #    print(element + "\n")


        #Goes through each pair in adjacencyList, and adds a tag that indicates whether the second entry in the pair is one of the articles in the file.
        for pair in adjacencyList:
            answer = pair[1]
            indoiList = False
            
            for element in doiList:
                if element == answer:
                    indoiList = True
                
            if indoiList == False:
                pair[2] = False
    f.close()

    #Takes all the elements in adjacencyList that have both entries as one of the articles in the file, and writes each pair into a CSV file.
    with open('./gyrorecsCSV.csv', 'w', encoding="utf8") as g:
        for element in adjacencyList:
            if element[2] == True:
                g.write(element[0] + ", " + element[1] + "\n")
    g.close()


    adjacencyListNumTimesReferenced = []

    adjacencyList.sort(key=sortKey)

    #with open('C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\SupportFiles\\gyrorecsCSV2.csv', 'w', encoding="utf8") as h:
    #    for element in adjacencyList:
    #        if element[2] == True:
    #            h.write(element[0] + ", " + element[1] + "\n")
    #h.close()


    #Calculates the number of nodes that will come out of each element in the adjacencyList
    adjacencyListNumTimesReferenced = []

    prevDoi = "999"
    firstTime = True

    for element in adjacencyList:
        if element[2] == True:
            if prevDoi != element[1]:
                if firstTime == False:
                    adjacencyListNumTimesReferenced.append([prevDoi,counter])
                firstTime = False
                counter = 1
                prevDoi = element[1]
            else:
                counter += 1 
        
    adjacencyListNumTimesReferenced.append([prevDoi,counter])

    for article in articlesDict:
        doi = articlesDict[article]["DOI"]
        appears = False
        for element in adjacencyListNumTimesReferenced:
            if element[0] == doi or doi == "999":
                    appears = True
        if not appears:
            adjacencyListNumTimesReferenced.append([doi,0])


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

    for article in articlesDict:
        doi = articlesDict[article]["DOI"]
        appears = False
        for element in adjacencyListNumOfReferences:
            if element[1] == doi or doi == "999":
                    appears = True
        if not appears:
            adjacencyListNumOfReferences.append([doi,0])

    

    adjacencyList.sort(key=sortKey)

    #Sorts the number-of-references list from highest number of references to lowest number of references
    adjacencyListNumTimesReferenced.sort(key=sortKey, reverse=True)
    adjacencyListNumOfReferences.sort(key=sortKey, reverse=True)

    generatedSphericalCoords = generateCoords(articlesDict, adjacencyListNumTimesReferenced, adjacencyList)
    if debug:
        print(generatedSphericalCoords)
    
    #for element in adjacencyList:
    #    if element[2] == True:
    #        print(adjacencyList)
    #for element in adjacencyListNumOfReferences:
    #    print(element)
    

    return articlesDict, adjacencyList, adjacencyListNumTimesReferenced, generatedSphericalCoords




def generateCoords(articlesDict, adjacencyListNumTimesReferenced, adjacencyList):
    coordsDict = {}

    referencesMostReferenced = []
    referencesSecondMostReferenced = []

    referencesMostReferencedNumOfReferences = []
    referencesSecondMostReferencedNumOfReferences = []

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
    #extraCounter = 0

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

            #print([inMostList,inSecondMostList]
            if inMostList:
                #print("3")
                inMostListCounter += 1
                #print(inMostListCounter)
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
                    #print("4")
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

def generateCoords3_animation():
    articlesDict, adjacencyList, adjacencyListNumTimesReferenced, generatedSphericalCoords = parseBibtexEntry()
    
    adjacencyListInGraph = []

    for entry in adjacencyList:
        if entry[2] == True:
            adjacencyListInGraph.append(entry)


    coordsDict = generateCoordsMiddle(articlesDict,adjacencyListNumTimesReferenced, adjacencyList)

    createVTKFilesPointsArcs(articlesDict, adjacencyList, adjacencyListNumTimesReferenced, coordsDict, 0)


    #for element in coordsDict:

    #    coordsDict[element] = [2*math.pi*random.random(),math.pi*random.random()]

    surfaceArea = 4*math.pi

    eqAngle = math.sqrt(surfaceArea/len(adjacencyListNumTimesReferenced))

    vertexList = []

    for element in coordsDict:
        phi = float(coordsDict[element][0])
        theta = float(coordsDict[element][1])

        x = math.cos(phi)*math.sin(theta)
        y = math.sin(phi)*math.sin(theta)
        z = math.cos(theta)

        vertexList.append([[x,y,z],[0,0,0],element])


    
    for ctr in range(50):
        for v in vertexList: 
            v[1] = [0,0,0]
            for u in vertexList:
                if u[0][0] != v[0][0] or u[0][1] != v[0][1] or u[0][2] != v[0][2]:

                    #print(u[0][0] != v[0][0])
                    #rint(u)
                    #print(v)
                    #print(u[0][2] != v[0][2])
                    #print(" ")


                    #calcDisp = [delta vector at v directly away from u, length of arc between v and u]
                    delta, arcLength = calcDisp(u[0],v[0])
                    deltaLength = math.sqrt(math.pow(delta[0],2) + math.pow(delta[1],2) + math.pow(delta[2],2))
                    
                    for i in range(len(delta)):
                        delta[i] = delta[i]/deltaLength

                    repulsiveForceStrength = 2
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
            #for element in vertexList:
            #    if element[0][0] == u[0] and element[0][1] == u[1]:
            #        u = element
            #for element in vertexList:
            #    if element[0][0] == v[0] and element[0][1] == v[1]:
            #        V = element
            
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
        #print(dispVecLenAverage)

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

        createVTKFilesPointsArcs(articlesDict, adjacencyList, adjacencyListNumTimesReferenced, coordsDict, ctr+1)

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


    #print(point1_step_2_matrix)

    angleFirstPoint = math.atan2(point1_step_2_matrix[1],point1_step_2_matrix[0])
    angleSecondPoint = math.atan2(point2_step_2_matrix[1],point2_step_2_matrix[0])

    rot_matrix_3 = np.array([[math.cos(-angleFirstPoint),-math.sin(-angleFirstPoint),0],
                                [math.sin(-angleFirstPoint),math.cos(-angleFirstPoint),0],
                                [0,0,1]])

    point1_step_3_matrix = np.dot(rot_matrix_3, point1_step_1_matrix)
    point2_step_3_matrix = np.dot(rot_matrix_3, point2_step_2_matrix)
    lenTangentVector = math.sqrt(math.pow(coord_2[0][0],2)+math.pow(coord_2[1][0],2)+math.pow(coord_2[2][0],2))
    if point2_step_3_matrix[1] < 0:
    #    print(lenTangentVector)
        angleFirstPoint = angleFirstPoint-(lenTangentVector/10)
    else:
    #    print(lenTangentVector)
        angleFirstPoint = angleFirstPoint + lenTangentVector/10

    corrVector = np.array([math.cos(angleFirstPoint),math.sin(angleFirstPoint),0])
    #print(corrVector)

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

    #print(corrVector)

    return corrVector



def calcDisp(firstPoint, secondPoint):

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

debug = False

#edge pairs contain many points. each element of edge_pairs looks like [phi_1, phi_2, theta_1, theta_2]
def createAllArcsOfGraph(edge_pairs,topPoint, ColorStyleIndicator,ListOfPointsToEmphasize,Option,iteration):
    
    emphasizeList = []
    for element in edge_pairs:
        if element[4]:
            emphasizeList.append([edge_pairs[1],edge_pairs[3]])
        element = [edge_pairs[0],edge_pairs[1],edge_pairs[2],edge_pairs[3]]

    #print(emphasizeList)

    #print("ListOfPointsToEmphasize")
    #print(ListOfPointsToEmphasize) 
    

    numOfSpaces = 512
    print(iteration)
    with open('./OneLineVTK3-Iteration' + str(iteration) + '.vtk', "w", encoding="utf8") as f:
        #Header
        f.write("# vtk DataFile Version 3.0\n")
        f.write("fieldline polygons\n")
        f.write("ASCII\n")
        f.write("DATASET POLYDATA\n")
        f.write("POINTS " + str(len(edge_pairs)*(numOfSpaces+1)) + " float64\n")

        for pair in edge_pairs:
            phi_1 = pair[0]
            phi_2 = pair[1]
            theta_1 = pair[2]
            theta_2 = pair[3]        

            emphasizeIndicator = False


            if Option == 0:
                createArc(f,phi_1,phi_2,theta_1,theta_2,numOfSpaces)

            if Option == 1:
                for element in ListOfPointsToEmphasize:
                    if float(element[0].strip()) == phi_2 and float(element[1].strip()) == theta_2:
                        if debug:
                            print("Enterhere")
                        createArc2(f,phi_1, phi_2, theta_1, theta_2, numOfSpaces)
                        emphasizeIndicator = True
                if not emphasizeIndicator:
                    createArc(f, phi_1, phi_2, theta_1, theta_2, numOfSpaces)

        f.write("LINES " + str(len(edge_pairs)) + " " + str(len(edge_pairs)*(numOfSpaces+2)) + "\n")

        counter = 0
        for i in range(len(edge_pairs)):
            output = str(numOfSpaces+1) + " "
            for i in range(numOfSpaces+1):
                output += str(counter) + " "
                counter = counter+1
            f.write(output + "\n")




        f.write("POINT_DATA " + str((numOfSpaces+1)*len(edge_pairs)) + "\n")
        f.write("SCALARS cell_Scalars int 1" + "\n") 
        f.write("LOOKUP_TABLE default" + "\n")




        if ColorStyleIndicator == 0:
            for i in range(len(edge_pairs)*(numOfSpaces+1)):
                f.write("14\n")
        elif ColorStyleIndicator == 1:
            for i in range(len(edge_pairs)):
                for j in range(math.floor((numOfSpaces+1)/2)):
                    f.write("3\n")
                for j in range(numOfSpaces+1-math.floor((numOfSpaces+1)/2)):
                    f.write("7\n")
        elif ColorStyleIndicator == 2:
            for element in edge_pairs:
                if element[1] == topPoint[0] and element[3] == topPoint[1]:
                    f.write("3\n")
                else:
                    f.write("1\n")

        
    f.close()


def createArc(f, phi_1, phi_2, theta_1, theta_2, numOfSpaces):

    #Get the (x,y,z) cooredinates of each point.
    coord_1 = np.array([[math.cos(phi_1)*math.sin(theta_1)], [math.sin(phi_1)*math.sin(theta_1)], [math.cos(theta_1)]])
    coord_2 = np.array([[math.cos(phi_2)*math.sin(theta_2)], [math.sin(phi_2)*math.sin(theta_2)], [math.cos(theta_2)]])


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
    point2_step_2_matrix = np.dot(rot_matrix_1,coord_2)

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
    point2_step_2_matrix = np.dot(rot_matrix_2, point2_step_2_matrix)

    angleFirstPoint = math.atan2(point1_step_2_matrix[1],point1_step_2_matrix[0])
    angleSecondPoint = math.atan2(point2_step_2_matrix[1],point2_step_2_matrix[0])
    #if point1_step_2_matrix[0] == 0:
    #    angleFirstPoint = math.pi/2
    #else:
    #    angleFirstPoint = math.atan(point1_step_2_matrix[1]/point1_step_2_matrix[0])#

    #if point2_step_2_matrix[0] == 0:
    #    angleFirstPoint = math.pi/2
    #else:
    #    angleSecondPoint = math.atan(point2_step_2_matrix[1]/point2_step_2_matrix[0])

    #if point1_step_2_matrix[0] < 0:
    #    angleFirstPoint += math.pi
    #elif point1_step_2_matrix[1] < 0:
    #    angleFirstPoint += 2*math.pi

    #if point2_step_2_matrix[0] < 0:
    #    angleSecondPoint += math.pi
    #elif point2_step_2_matrix[1] < 0:
    #    angleSecondPoint += 2*math.pi

    if abs(angleSecondPoint-angleFirstPoint) < math.pi:
        step = (angleSecondPoint-angleFirstPoint)/numOfSpaces
        rotatedpoints = []
        for i in range(numOfSpaces+1):
            rot_vector = np.array([[math.cos(angleFirstPoint+i*step)],[math.sin(angleFirstPoint+i*step)],[0]])




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
            inv1 = np.dot(rot_matrix_2_inverse,rot_vector)
            inv2 = np.dot(rot_matrix_1_inverse, inv1)

            f.write(str(inv2[0][0]) + " " + str(inv2[1][0]) + " " + str(inv2[2][0]) + "\n")
    else:
        if angleSecondPoint < angleFirstPoint:
            angleSecondPoint += 2*math.pi
            step = (angleSecondPoint-angleFirstPoint)/numOfSpaces
            rotatedpoints = []
            for i in range(numOfSpaces+1):
                rot_vector = np.array([[math.cos(angleFirstPoint+i*step)],[math.sin(angleFirstPoint+i*step)],[0]])

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
                inv1 = np.dot(rot_matrix_2_inverse,rot_vector)
                inv2 = np.dot(rot_matrix_1_inverse, inv1)

                f.write(str(inv2[0][0]) + " " + str(inv2[1][0]) + " " + str(inv2[2][0]) + "\n")
                #f.write(str(inv2[2][0]) + " " + str(inv2[1][0]) + " " + str(inv2[0][0]) + " --- " + str(math.pow(inv2[2][0],2) + math.pow(inv2[1][0],2) + math.pow(inv2[0][0],2)) + "\n")
        else:
            angleFirstPoint += 2*math.pi

            step = (angleSecondPoint-angleFirstPoint)/numOfSpaces
            rotatedpoints = []
            for i in range(numOfSpaces+1):
                rot_vector = np.array([[math.cos(angleFirstPoint+i*step)],[math.sin(angleFirstPoint+i*step)],[0]])

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
                    

                inv1 = np.dot(rot_matrix_2_inverse,rot_vector)

                inv2 = np.dot(rot_matrix_1_inverse, inv1)

                f.write(str(inv2[0][0]) + " " + str(inv2[1][0]) + " " + str(inv2[2][0]) + "\n")






#Emphasized Lines that are not on the sphere itself.
def createArc2(f, phi_1, phi_2, theta_1, theta_2, numOfSpaces):
    height = 1.3

    #Get the (x,y,z) cooredinates of each point.
    coord_1 = np.array([[math.cos(phi_1)*math.sin(theta_1)], [math.sin(phi_1)*math.sin(theta_1)], [math.cos(theta_1)]])
    coord_2 = np.array([[math.cos(phi_2)*math.sin(theta_2)], [math.sin(phi_2)*math.sin(theta_2)], [math.cos(theta_2)]])


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
    point2_step_2_matrix = np.dot(rot_matrix_1,coord_2)

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
    point2_step_2_matrix = np.dot(rot_matrix_2, point2_step_2_matrix)

    angleFirstPoint = math.atan2(point1_step_2_matrix[1],point1_step_2_matrix[0])
    angleSecondPoint = math.atan2(point2_step_2_matrix[1],point2_step_2_matrix[0])
    

    if abs(angleSecondPoint-angleFirstPoint) < math.pi:
        middleAngle = (angleFirstPoint+angleSecondPoint)/2
    else:
        middleAngle = (angleFirstPoint+angleSecondPoint)/2 + math.pi


    rot_matrix_3 = np.array([[math.cos(-middleAngle),-math.sin(-middleAngle),0],
                            [math.sin(-middleAngle),math.cos(-middleAngle),0],
                            [0,0,1]])
    
    point1_step_3_matrix = np.dot(rot_matrix_3,point1_step_2_matrix)
    point2_step_3_matrix = np.dot(rot_matrix_3,point2_step_2_matrix)

    #y^2 = a(height-x). We are calculating a so that the parabola passes thru point1_step_3_matrix, point2_step_3_matrix, and [height,0,0]

    a = math.pow(point1_step_3_matrix[1][0],2)/(height-point1_step_3_matrix[0][0])

    rotatedpoints = []

    inity = point1_step_3_matrix[1][0]
    step = (point2_step_3_matrix[1][0]-point1_step_3_matrix[1][0])/numOfSpaces
    for i in range(numOfSpaces+1):
        ytemp = inity+i*step
        rot_vector = np.array([[height - math.pow(ytemp,2)/a],[ytemp],[0]])
        #print(rot_vector)


        rot_matrix_3_inverse = np.array([[math.cos(middleAngle),-math.sin(middleAngle),0],
                            [math.sin(middleAngle),math.cos(middleAngle),0],
                            [0,0,1]])

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

        inv1 = np.dot(rot_matrix_3_inverse,rot_vector)
        inv2 = np.dot(rot_matrix_2_inverse, inv1)
        inv3 = np.dot(rot_matrix_1_inverse, inv2)

        #print(inv3)
        #print(" ")

        f.write(str(inv3[0][0]) + " " + str(inv3[1][0]) + " " + str(inv3[2][0]) + "\n")



def createVTKFilesPointsArcs(articlesDict, adjacencyList, adjacencyListNumTimesReferenced, generatedSphericalCoords, iteration):

    with open('./TrueAdjacencyList.txt', "w", encoding="utf8") as b:
        for element in adjacencyList:
            if element[2] == True:
                b.write(element[0] + " " + element[1] + "\n")
        
    with open('./GeneratedPoints3_iteration' + str(iteration) + '.txt', "w", encoding="utf8") as a:
        #print(generatedSphericalCoords)        
        for element in generatedSphericalCoords:
            phi = float(generatedSphericalCoords[element][0])
            theta = float(generatedSphericalCoords[element][1])

            x = math.cos(phi)*math.sin(theta)
            y = math.sin(phi)*math.sin(theta)
            z = math.cos(theta)

            a.write(str(x) + " " + str(y) + " " + str(z) + " " + element + "\n")

    emphasizeIndexList = [0]
    emphasizeList = []

    #for element in generatedSphericalCoords:
    #    print(element+" "+ str(generatedSphericalCoords[element]))

    counter = 0
    CoordList = []
    for element in generatedSphericalCoords:
        CoordList.append(generatedSphericalCoords[element])


    createVTKSpheres(CoordList,16,2,iteration)



    for element in generatedSphericalCoords:
        tempList = generatedSphericalCoords[element]
        part1 = str(tempList[0])
        part2 = str(tempList[1])

        generatedSphericalCoords[element] = [part1,part2]
        #print(generatedSphericalCoords[element])

    #print(generatedSphericalCoords)
    
    #for element in adjacencyList:
    #    if element[2] == True:
    #        print(element)
    #generatedSphericalCoords = {}
    #with open('C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\SupportFiles\\GeneratedPoints.txt', encoding="utf8") as f:
    #    counter = 0
    #    for line in f:
    #        elements = line.split(',')

    #        generatedSphericalCoords[elements[0]] = [elements[1],elements[2]]

    #        for number in emphasizeIndexList:
    #            if number == counter:
    #                emphasizeList.append(generatedSphericalCoords[elements[0]])
    #        counter += 1

        #print("EMPHASIZELIST")
        #for element in emphasizeList:
        #    print(element)

    #    f.close()



    counter = 0
    for element in generatedSphericalCoords:
        if  counter == 0:
            topPoint = [generatedSphericalCoords[element][0], generatedSphericalCoords[element][1]]
            counter += 1

    LinesList = []

    #print(adjacencyListNumTimesReferenced[0][0])

    tempCounter = 0
    for pair in adjacencyList:
        if pair[2] == True:
            if pair[0] in generatedSphericalCoords:
                if pair[1] in generatedSphericalCoords:
                    #inCoords = False
                    #inCoords1 = False
                    #inCoords2 = False

                    #for elem in generatedSphericalCoords:
                    #    if elem == pair[0]:
                    #        inCoords1 = True
                    #    if elem == pair[1]:
                    #        inCoords2 = True
                        
                    #if inCoords1 and inCoords2:
                    #    inCoords = True
                    first = pair[0]
                    second = pair[1]

                    firstCoords = [float(generatedSphericalCoords[first][0]), float(generatedSphericalCoords[first][1])]
                    secondCoords = [float(generatedSphericalCoords[second][0]), float(generatedSphericalCoords[second][1])]

                    if len(emphasizeList) != 0:
                        for element in emphasizeList:
                            if secondCoords[0] == float(element[0].strip()) and secondCoords[1] == float(element[1].strip()):
                                tempCounter += 1
                                LinesList.append([firstCoords[0],secondCoords[0],firstCoords[1],secondCoords[1],True])
                            else:
                                LinesList.append([firstCoords[0],secondCoords[0],firstCoords[1],secondCoords[1],False])
                    else:
                        LinesList.append([firstCoords[0],secondCoords[0],firstCoords[1],secondCoords[1],False])

        
    OptionNumber = 0
    #option 0 = everything on plane
    #option 1 = everything connected to points in emphasizeList is above

    createAllArcsOfGraph(LinesList,topPoint,1,emphasizeList,OptionNumber,iteration)


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


def sortKey(e):
    return e[1]

def sortKey2(e):
    return e[0]


def createVTKSpheres(sphericalCoordList,numSides,ColorStyleIndicator,iteration):
    r = 0.015
    listLength = len(sphericalCoordList)
    n=numSides
    with open('./SmallSpherePoints_iteration' + str(iteration) + '.vtk', "w", encoding="utf8") as f:
        with open('./GeneratedPoints3_iteration' + str(iteration) + '.txt', "w", encoding="utf8") as h:

            #Header
            f.write("# vtk DataFile Version 3.0\n")
            f.write("fieldline polygons\n")
            f.write("ASCII\n")
            f.write("DATASET POLYDATA\n")
            f.write("POINTS " + str(listLength*(n*(n-1)+2)) + " float64\n")



            for i in range(listLength):
                phi = sphericalCoordList[i][0]
                theta = sphericalCoordList[i][1]
                writePointsForOneSphere(phi,theta,r,f,n,h)
             
        h.close()
        

        f.write("POLYGONS " + str(n*n*listLength) + " " + str(listLength*(4*n+5*(n-2)*n+4*n)) + "\n")

        shift = 0
        for i in range(listLength):
            phi = sphericalCoordList[i][0]
            theta = sphericalCoordList[i][1]
            writePolygons(f,shift,n)
            shift += 1 

        #Ending
        f.write("POINT_DATA " + str(listLength*(n*(n-1)+2)) + "\n")
        f.write("CELL_DATA " + str(listLength*n*n) + "\n")
        f.write("SCALARS cell_Scalars int 1" + "\n") 
        f.write("LOOKUP_TABLE default" + "\n")

        #White color at the end
        if ColorStyleIndicator == 0:
            for i in range(listLength*n*n):
                f.write("5\n")
        elif ColorStyleIndicator == 1:
            for i in range(n*n*10):
                f.write("9\n")
            for i in range(n*n*10+1,listLength*n*n):
                f.write("5\n")
        elif ColorStyleIndicator == 2:
            for i in range(n*n):
                for j in range(listLength):
                    f.write(str(i) + "\n")

    f.close()


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



def writePointsForOneSphere(phi,theta,r,f,n,h):

        #Coordinates
        xcoord = math.cos(phi)*math.sin(theta)
        ycoord = math.sin(phi)*math.sin(theta)
        zcoord = math.cos(theta)

        h.write(str(xcoord) + " " + str(ycoord) + " " + str(zcoord) +"\n")

        #Write the coord of the top point
        f.write(str(xcoord) + " " + str(ycoord) + " " + str(zcoord + r) + "\n")

        #In concentric circles, write the coordinates of all the points in the middle
        for x in range(1,n):
            for y in range(n):
                f.write(str(r*math.cos(2*math.pi*y/n)*math.sin(math.pi*x/n)+xcoord) + " " + str(r*math.sin(2*math.pi*y/n)*math.sin(math.pi*x/n)+ycoord) + " " + str(r*math.cos(math.pi*x/n)+zcoord) + "\n")

        #Write the coord of the bottom point
        f.write(str(xcoord) + " " + str(ycoord) + " " + str(zcoord-r) + "\n")


#Structured Arrangement of Points
def generateCoordsPrimePrime(articlesDict, adjacencyListNumTimesReferenced, adjacencyList):
    coordsDict = {}

    coordsDict = generateCoords(articlesDict,adjacencyListNumTimesReferenced, adjacencyList)

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
    #print(permlist1)
    #print(type(permlist1))

    counter = 0
    for elem in permlist1:
        column = counter % columns
        row = (counter - column)/columns
        #print(column)
        #print(row)
        #print(coordsDict[elem])
        coordsDict[elem] = [2*math.pi*(column+1)/columns,(math.pi*(row+1))/(columns+1)]
        #print(coordsDict[elem])
        #print()
        counter += 1
        #print(counter)
        #print()

    #print(coordsDict)

    return coordsDict

#Starting from the Middle and Moving Outwards
def generateCoordsMiddle(articlesDict, adjacencyListNumTimesReferenced, adjacencyList):
    coordsDict = {}

    coordsDict = generateCoords(articlesDict,adjacencyListNumTimesReferenced, adjacencyList)

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
        #print(column)
        #print(row)
        #print(coordsDict[elem])
        coordsDict[elem] = [2*math.pi*(column+1)/columns,(math.pi*(row+1))/(columns+1)]
        #print(coordsDict[elem])
        #print()
        counter += 1
        #print(counter)
        #print()

    #print(coordsDict)

    return coordsDict

generateCoords3_animation()


