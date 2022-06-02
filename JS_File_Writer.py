import math
import numpy as np

def generateJSFile():
    with open('C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\WEBGL\\THREEJSCode.js', "w", encoding="utf8") as f:

        f.write("import * as THREE from 'https://unpkg.com/three@0.119.0/build/three.module.js';\n")
        f.write("import { OrbitControls } from 'https://unpkg.com/three@0.119.0/examples/jsm/controls/OrbitControls.js';\n\n")
        f.write("let scene, camera, renderer,controls,objects = [],numObjects = [],nodeNameList = [],adjacencyList = [],citedPapersList = [], citesPapersList = [];\n\n")
        f.write("init();\n")
        f.write("animate();\n\n")

        f.write("function init() {\n")
        f.write("\tvar div = document.createElement(\'div\')\n")
        f.write("\tdiv.id = \'dialog\';\n")
        f.write("\tdiv.title = \'Node Information\';\n")
        f.write("\tdiv.innerHTML = 0;\n")
        f.write("\tdocument.body.appendChild(div);\n\n")

        f.write("\tvar div2 = document.createElement(\'div\')\n")
        f.write("\tdiv2.id = \'dialog2\';\n")
        f.write("\tdiv2.title = 'Node Edges';\n")
        f.write("\tdiv2.innerHTML = 0\n")
        f.write("\tdocument.body.appendChild(div2)\n\n")

        f.write("\tvar container = document.getElementById( \'canvas\' );\n\n")

        f.write("\tscene = new THREE.Scene();\n")
        f.write("\tscene.background = new THREE.Color(0x123456)\n\n")
        f.write("\trenderer = new THREE.WebGLRenderer({ antialias: true });\n")
        f.write("\trenderer.setSize(window.innerWidth,window.innerHeight);\n")
        f.write("\tdocument.body.appendChild( renderer.domElement );\n\n")
        f.write("\tcamera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );\n\n")
        f.write("\tcontrols = new OrbitControls( camera, renderer.domElement );\n")
        #f.write("\tcontrols.listenToKeyEvents( window );\n\n\n")
        f.write("\tcontrols.enableDamping = true;\n")
        f.write("\tcontrols.dampingFactor = 0.05;\n\n")
        f.write("\tcontrols.minDistance = 1;\n")
        f.write("\tcontrols.maxDistance = 15\n\n")
        f.write("\tcontrols.maxPolarAngle = Math.PI\n\n\n\n")
        f.write("\tconst points = []\n")

        pointindicator = False
        with open("C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\SupportFiles\\OneLineVTK3.vtk", encoding="utf8") as g:
            counter = 0
            for line in g:

                counter += 1
                if "LINES" in line:
                    pointindicator = False

                if pointindicator:
                    coordsList = line.split()
                    coordsList[0] = float(coordsList[0])
                    coordsList[1] = float(coordsList[1])
                    coordsList[2] = float(coordsList[2])

                    f.write("\n\tpoints.push(new THREE.Vector3(" + str(coordsList[0]) + "," + str(coordsList[1]) + "," + str(coordsList[2]) + "))")
        
                if "POINTS" in line:
                    pointindicator = True

        f.write("\n\n\tlet geometry = new THREE.BufferGeometry().setFromPoints( points )\n")
        f.write("\tconst material = new THREE.MeshBasicMaterial( {color: 0xffffff,wireframe:true} );\n\n")
        f.write("\tconst mesh = new THREE.Mesh(geometry,material);\n")
        f.write("\tscene.add(mesh)\n\n")


        f.write("\tlet geometryprime = new THREE.SphereGeometry(1,40,40)\n\n")
        f.write("\tconst materialprime = new THREE.MeshBasicMaterial( {color:0xababab } );\n\n")
        f.write("\tconst meshprime = new THREE.Mesh(geometryprime,materialprime)\n")
        f.write("\tscene.add(meshprime)\n\n\n")

        counter = 1
        with open("C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\SupportFiles\\GeneratedPoints3.txt", encoding="utf8") as h:
            for line in h:
                lineList = line.split()
                f.write("\tconst geometry" + str(counter) + " = new THREE.SphereGeometry(0.02);\n")
                f.write("\tconst material" + str(counter) + " = new THREE.MeshBasicMaterial( {color: 0xff0000});\n")
                f.write("\tconst mesh" + str(counter) + " = new THREE.Mesh(geometry" + str(counter) + ",material" + str(counter) + ")\n")
                f.write("\tmesh" + str(counter) + ".position.x = " + lineList[0] + "\n")
                f.write("\tmesh" + str(counter) + ".position.y = " + lineList[1] + "\n")
                f.write("\tmesh" + str(counter) + ".position.z = " + lineList[2] + "\n")
                f.write("\tscene.add(mesh" + str(counter) + ")\n\n")
                f.write("\tnumObjects.push([" + str(counter) + ",mesh" + str(counter) + ", \"" + lineList[3] + "\"])\n")
                f.write("\tobjects.push( mesh" + str(counter) + " )\n\n")
                #Add OPTION LATER
                f.write("\tconst loader" + str(counter) + " = new THREE.FontLoader();\n\n")
                f.write("\tloader" + str(counter) + ".load( 'https://unpkg.com/three@0.119.0/examples/fonts/helvetiker_regular.typeface.json', function ( font ) {\n\n")
                f.write("\t\tconst color" + str(counter) + "_5 = 0xff0000;\n\n")
                f.write("\t\tconst matLite"+ str(counter) + "= new THREE.MeshBasicMaterial( {\n")
                f.write("\t\t\tcolor:color" + str(counter) + "_5,\n")
                f.write("\t\t\tside: THREE.DoubleSide\n")
                f.write("\t\t} );\n\n")
                f.write("\t\tconst geometry" + str(counter) + "_5 = new THREE.ShapeGeometry( shapes" + str(counter) + " );\n\n")
                f.write("\t\tgeometry" + str(counter) + "_5.computeBoundingBox()\n\n")
                f.write("\t\tconst text = new THREE.Mesh( geometry" + str(counter) + "_5, matLite" + str(counter) + " );\n")

                r=math.sqrt(math.pow(float(lineList[0]),2) + math.pow(float(lineList[1]),2) + math.pow(float(lineList[2]),2))
                theta = math.acos(float(lineList[2])/r)
                phi = math.atan2(float(lineList[1]),float(lineList[0]))

                mat3 = np.array([[math.cos(-phi),-math.sin(-phi),0],
                                 [math.sin(-phi),math.cos(-phi),0],
                                 [0,0,1]])

                mat2 = np.array([[math.cos(theta),0,math.sin(theta)],
                                 [0,1,0],
                                 [-math.sin(theta),0,math.cos(theta)]])
                
                mat1 = np.array([[math.cos(phi),-math.sin(phi),0],
                                 [math.sin(phi),math.cos(phi),0],
                                 [0,0,1]])

                mat_overall = np.dot(mat1,np.dot(mat2,mat3))

                beta = math.atan2(-1*mat_overall[2][0],math.sqrt(math.pow(mat_overall[0][0],2)+math.pow(mat_overall[1][0],2)))
                alpha = math.atan2(mat_overall[2][1]/math.cos(beta),mat_overall[2][2]/math.cos(beta))
                gamma = math.atan2(mat_overall[1][0]/math.cos(beta),mat_overall[0][0]/math.cos(beta))

                f.write("\t\ttext.rotation.z = " + str(phi) + ";\n")


                f.write("\t\ttext.position.x = " + lineList[0] + "*1.08;\n")
                f.write("\t\ttext.position.y = " + lineList[1] + "*1.08;\n")
                f.write("\t\ttext.position.z = " + lineList[2] + "*1.08;\n")

                
                f.write("\t\tif (text.position.z < 0) {\n")

                f.write("\t\t}\n")
                

                f.write("\t\tscene.add( text )\n\n\n")
                f.write("\t} );\n")

                adjList = ""
                citedList = ""
                citesList = ""
                with open("C:\\Users\\aguha\\Documents\\1-PPPL-Research\\1-PPPL-Research\\SupportFiles\\TrueAdjacencyList.txt", encoding="utf8") as b:
                    targetNode = lineList[3]
                    print(targetNode)
                    for line in b:
                        targetSplit = line.split(' ')
                        targetSplit1 = targetSplit[1]
                        targetSplit1 = targetSplit1[0:len(targetSplit1)-1]
                        if targetSplit[0] == targetNode:
                            adjList = adjList + "[\"" + targetSplit[0] + "\", \"" + targetSplit1 + "\"], "
                            citedList = citedList + "\"" + targetSplit1 + "\", "
                        if targetSplit1 == targetNode:
                            adjList = adjList + "[\"" + targetSplit[0] + "\", \"" + targetSplit1 + "\"], "
                            citesList = citesList + "\"" + targetSplit[0] + "\", "

                        
                
                b.close()
                

                f.write("\tadjacencyList.push([" + adjList[0:len(adjList)-2] + "])\n\n")
                f.write("\tcitedPapersList.push([" + citedList[0:len(citedList)-2] + "])\n\n")
                f.write("\tcitesPapersList.push([" + citesList[0:len(citesList)-2] + "])\n\n")
                counter += 1



        f.write("\tvar raycaster = new THREE.Raycaster();\n")
        f.write("\tvar mouse = new THREE.Vector2();\n\n\n\n")
        f.write("\tdocument.addEventListener( \'mousedown\',function( event ) {\n\n")
        f.write("\tvar rect = renderer.domElement.getBoundingClientRect();\n")
        f.write("\tmouse.x = ( ( event.clientX - rect.left ) / ( rect.width - rect.left ) ) * 2 -1;\n")
        f.write("\tmouse.y = - ( ( event.clientY - rect.top ) / ( rect.bottom - rect.top) ) * 2 + 1;\n\n")
        f.write("\t\traycaster.setFromCamera( mouse, camera ) ;\n\n")
        f.write("\t\tvar intersects = raycaster.intersectObjects ( scene.children );\n\n")
        f.write("\t\tconst col_red = new THREE.Color( 0xff0000 );\n")
        f.write("\t\tconst col_green = new THREE.Color(0x00ff00 );\n")
        f.write("\t\tconst col_blue = new THREE.Color(0x0000ff);\n")
        f.write("\t\tconst col_orange = new THREE.Color(0xffa500);\n")
        f.write("\t\t\tfor ( let i = 0; i < intersects.length; i ++ ) {\n")
        f.write("\t\t\tvar counter = 0;\n")
        f.write("\t\t\t\tif (intersects[i].object.geometry.type == \"SphereGeometry\") {\n")
        f.write("\t\t\t\t\tif (intersects[i].object.geometry.radius != 1) {\n")
        f.write("\t\t\t\t\t\tif (intersects[i].object.material.color.equals(col_red) || intersects[i].object.material.color.equals(col_blue) || intersects[i].object.material.color.equals(col_orange)) {\n")
        f.write("\t\t\t\t\t\tintersects[i].object.material.color.set( col_green )\n")
        f.write("\t\t\t\t\t\t\tfor (let j = 0; j < scene.children.length; j ++ ) {\n")
        f.write("\t\t\t\t\t\t\t\tif (scene.children[j].material.color.equals( col_green )) {\n")
        f.write("\t\t\t\t\t\t\t\tif (scene.children[j] != intersects[i].object) {\n")
        f.write("\t\t\t\t\t\t\t\t\tscene.children[j].material.color.set( col_red )\n")
        f.write("\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t}\n\n\n")
        f.write("\t\t\t\t\t\tfor (let k = 0; k < numObjects.length; k++) {\n")
        f.write("\t\t\t\t\t\t\tvar listNumObjects = numObjects[k]\n")
        f.write("\t\t\t\t\t\t\tif (listNumObjects[1] == intersects[i].object) {\n")
        f.write("\t\t\t\t\t\t\t\tdiv.innerHTML = \"DOI\" + listNumObjects[0].toString() + \" = \" + listNumObjects[2]\n")
        
        f.write("\t\t\t\t\t\t\t\tvar niceLongString = \"\"\n")
        f.write("\t\t\t\t\t\t\t\tvar adj = adjacencyList[k]\n")
        f.write("\t\t\t\t\t\t\t\tvar citedList = citedPapersList[k]\n")
        f.write("\t\t\t\t\t\t\t\tvar citesList = citesPapersList[k]\n\n")
        f.write("\t\t\t\t\t\t\t\tfor (let t = 0; t < adj.length; t++) {\n")
        f.write("\t\t\t\t\t\t\t\t\tvar elem = adj[t]\n")
        f.write("\t\t\t\t\t\t\t\t\tniceLongString = niceLongString + \"[\" + elem[0] + \",\" + elem[1] + \"]\\n\"\n")
        f.write("\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\tdiv2.innerHTML = niceLongString\n\n\n")
        
        f.write("\t\t\t\t\t\t\t\tvar inCitedListList = [];\n")
        f.write("\t\t\t\t\t\t\t\tvar inCitesListList = [];\n")
        f.write("\t\t\t\t\t\t\t\tfor (let n = 0;n < numObjects.length; n++) {\n")
        f.write("\t\t\t\t\t\t\t\t\tvar nodeName = numObjects[n]\n")
        f.write("\t\t\t\t\t\t\t\t\tvar tempBool1 = false;\n")
        f.write("\t\t\t\t\t\t\t\t\tvar tempBool2 = false;\n")
        f.write("\t\t\t\t\t\t\t\t\tfor (let p = 0; p < citedList.length; p++) {\n")
        f.write("\t\t\t\t\t\t\t\t\t\tif (nodeName[2] == citedList[p]) {\n")
        f.write("\t\t\t\t\t\t\t\t\t\t\ttempBool1 = true;\n")
        f.write("\t\t\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\t\tfor (let q = 0; q < citesList.length; q++) {\n")
        f.write("\t\t\t\t\t\t\t\t\t\tif (nodeName[2] == citesList[q]) {\n")
        f.write("\t\t\t\t\t\t\t\t\t\t\ttempBool2 = true;\n")
        f.write("\t\t\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\t\tinCitedListList.push(tempBool1)\n")
        f.write("\t\t\t\t\t\t\t\t\tinCitesListList.push(tempBool2)\n")
        f.write("\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\tfor (let n = 0; n < numObjects.length; n++) {\n")
        f.write("\t\t\t\t\t\t\t\t\tvar nodeName = numObjects[n]\n")
        f.write("\t\t\t\t\t\t\t\t\tif (inCitedListList[n] == true) {\n")
        f.write("\t\t\t\t\t\t\t\t\t\tnodeName[1].material.color.set(col_blue)\n")
        f.write("\t\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\t\telse if (nodeName[2] == listNumObjects[2] ) {\n")
        f.write("\t\t\t\t\t\t\t\t\t\tnodeName[1].material.color.set(col_green)\n")
        f.write("\t\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\t\telse {\n")
        f.write("\t\t\t\t\t\t\t\t\t\tnodeName[1].material.color.set(col_red)\n")
        f.write("\t\t\t\t\t\t\t\t\t}\n\n")
        f.write("\t\t\t\t\t\t\t\t\tif (inCitesListList[n] == true) {\n")
        f.write("\t\t\t\t\t\t\t\t\t\tnodeName[1].material.color.set(col_orange)\n")
        f.write("\t\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\t\telse if (nodeName[2] == listNumObjects[2] ) {\n")
        f.write("\t\t\t\t\t\t\t\t\t\tnodeName[1].material.color.set(col_green)\n")
        f.write("\t\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\t\telse if (!nodeName[1].material.color.equals(col_blue)) {\n")
        f.write("\t\t\t\t\t\t\t\t\t\tnodeName[1].material.color.set(col_red)\n")
        f.write("\t\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t\t}\n")
        f.write("\t\t\t\t\t}\n")

        f.write("\t\t\t\t\telse if (intersects[i].object.material.color.equals(col_green)) {\n")
        f.write("\t\t\t\t\t\tintersects[i].object.material.color.set(col_red)\n")
        f.write("\t\t\t\t\t}\n")
        f.write("\t\t\t\t}\n")
        f.write("\t\t\t}\n")
        f.write("\t\t}\n")
        f.write("\t},false );\n")


        f.write("\tcamera.position.z = 2\n\n\n\n")
        f.write("\twindow.addEventListener( 'resize', onWindowResize);\n\n")
        f.write("}\n\n")

        f.write("function onWindowResize() {\n\n")
        f.write("\tcamera.aspect = window.innerWidth / window.innerHeight;\n")
        f.write("camera.updateProjectionMatrix();\n\n\n")
        f.write("renderer.setSize( window.innerWidth, window.innerHeight );\n\n")

        f.write("}")

        f.write("\n\nfunction animate() {\n\n")
        f.write("\trequestAnimationFrame( animate );\n\n")
        f.write("\tcontrols.update();\n\n")
        f.write("renderer.render(scene,camera);\n\n")
        f.write("}")
    f.close()


