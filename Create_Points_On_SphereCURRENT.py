from Parse2 import parseBibtexEntry
import math

debug = False

adjacencyList, numreferenced = parseBibtexEntry()[0], parseBibtexEntry()[1]


#counter = 0
#for pair in adjacencyList:
#   if pair[2]:
#        print(pair)
#        counter = counter+1
#print(counter)

#print(" \n SPACE \n ")

#for pair in numreferenced:
#    print(pair)

def PhiThetaValuesCalculator(numreferenced):

    #Dictionary where the key is the DOI of the article and the value is a pair of the form [phi,theta]
    phithetaDict = {}

    #The most commonly referenced DOI goes at the top of the sphere
    phithetaDict[numreferenced[0]] = [0,0]

    #The second-most commonly referenced DOI goes at the bottom of the sphere
    phithetaDict[numreferenced[1]] = [math.pi,0] 

    return phithetaDict

def createVTKSpheres(sphericalCoordList,numSides,ColorStyleIndicator):
    r = 0.015
    listLength = len(sphericalCoordList)
    n=numSides
    with open('./SmallSpherePoints.vtk', "w", encoding="utf8") as f:
        with open('./GeneratedPoints2.txt', "w", encoding="utf8") as h:

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
                f.write("3\n")
            for i in range(n*n+1,listLength*n*n):
                f.write("5\n")
        
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
    
if __name__ == '__main__':
    #print(len(Parser.parseBibtexEntry()))

    adjacencyList, adjacencyListNumTimesReferenced, generatedSphericalCoords = parseBibtexEntry()

    with open('./GeneratedPoints.txt', "w", encoding="utf8") as f:
        CoordList = []
        for element in generatedSphericalCoords:
            CoordList.append(generatedSphericalCoords[element])
            f.write(element + ", " + str(generatedSphericalCoords[element][0]) + ", " + str(generatedSphericalCoords[element][1]) + "\n")
    

    #print("Elements of generatedSphericalCoords")
    #for element in generatedSphericalCoords:
    #    print(element)

    #print("Elements of adjacencyListNumTimesReferenced")
    #for element in adjacencyListNumTimesReferenced:
    #    print(element)
    

    #for element in CoordList:
    #    print(CoordList)

    #CoordList.append([9.748910536139755,0.7853981633974483])
    #CoordList.append([0.0,0.2617993877991494])
    
    #print(len(CoordList))

    #for element in CoordList:
    #    print(element)
    #CoordList = [[0,0],[0,math.pi],[math.pi/2,math.pi/2]]
    #CoordList = [[0,0]]

    # 0 = all the same color
    # 1 = Every point is blue except for the 10 most referenced points
    createVTKSpheres(CoordList,16,1)
