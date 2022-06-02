import math
from Parse2 import parseBibtexEntry
from Create_Points_On_SphereCURRENT import createVTKSpheres
from typing import List
import numpy as np

debug = False

#edge pairs contain many points. each element of edge_pairs looks like [phi_1, phi_2, theta_1, theta_2]
def createAllArcsOfGraph(edge_pairs,topPoint, ColorStyleIndicator,ListOfPointsToEmphasize,Option):
    
    emphasizeList = []
    for element in edge_pairs:
        if element[4]:
            emphasizeList.append([edge_pairs[1],edge_pairs[3]])
        element = [edge_pairs[0],edge_pairs[1],edge_pairs[2],edge_pairs[3]]
    

    numOfSpaces = 512

    with open('C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\SupportFiles\\OneLineVTK3.vtk', "w", encoding="utf8") as f:
        #Header
        f.write("# vtk DataFile Version 3.0\n")
        f.write("fieldline polygons\n")
        f.write("ASCII\n")
        f.write("DATASET POLYDATA\n")
        for i in range(100):
            print(len(edge_pairs)*(numOfSpaces+1))
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



def createVTKFilesPointsArcs():
    articlesDict, adjacencyList, adjacencyListNumTimesReferenced, generatedSphericalCoords = parseBibtexEntry()
    print("done")
    #print(generatedSphericalCoords)

    with open('C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\SupportFiles\\TrueAdjacencyList.txt', "w", encoding="utf8") as b:
        for element in adjacencyList:
            if element[2] == True:
                b.write(element[0] + " " + element[1] + "\n")

    with open('C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\SupportFiles\\GeneratedPoints3.txt', "w", encoding="utf8") as a:
        #print(generatedSphericalCoords)
        for element in generatedSphericalCoords:
            phi = generatedSphericalCoords[element][0]
            theta = generatedSphericalCoords[element][1]
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

    
    #print(emphasizeList)
    createVTKSpheres(CoordList,16,1)

    for element in generatedSphericalCoords:
        tempList = generatedSphericalCoords[element]
        part1 = str(tempList[0])
        part2 = str(tempList[1])

        generatedSphericalCoords[element] = [part1,part2]




    counter = 0
    for element in generatedSphericalCoords:
        if  counter == 0:
            topPoint = [generatedSphericalCoords[element][0], generatedSphericalCoords[element][1]]
            counter += 1

    LinesList = []


    tempCounter = 0
    for pair in adjacencyList:
        if pair[2] == True:
            if pair[0] in generatedSphericalCoords:
                if pair[1] in generatedSphericalCoords:

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

    print("LinesList")
    print(LinesList)
    OptionNumber = 0
    #option 0 = everything on plane
    #option 1 = everything connected to points in emphasizeList is above

    createAllArcsOfGraph(LinesList,topPoint,1,emphasizeList,OptionNumber)

if __name__ == '__main__':
    createVTKFilesPointsArcs()