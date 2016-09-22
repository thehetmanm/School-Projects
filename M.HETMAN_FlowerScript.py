import maya.cmds as cmds
import math as m
import random as r

ZT = 0.000000001

if "GUIWindow" in globals():
    if cmds.window( GUIWindow, exists = True ):     #Check if UI Window is open
        cmds.deleteUI( GUIWindow, window = True)    #Delete UI Window if one is open already

############################################################################### Math Functions #####################################################
    
################ Calculate Dot Product
def dotProduct (Vec1, Vec2):
    
    K = (Vec1[0])*(Vec2[0]) + (Vec1[1])*(Vec2[1]) + (Vec1[2])*(Vec2[2])
    
    return K
    
################ Calculate Angle Between Two Vectors    
def getAngle(vecA, vecB):
    
    magA = getMagnitude(vecA[0],vecA[1],vecA[2])
    magB = getMagnitude(vecB[0],vecB[1],vecB[2])
    
    dot = dotProduct(vecA, vecB)
    
    if (abs(magA*magB) < ZT):
        return False
    
    x = dot/(magA*magB)
    
    if (x > 1):
        x = 1
    elif (x < -1):
        x = -1
    
    angle = m.acos(x)
    return angle
    
def matrixMult(tMatrix, vtx):
    #tMatrix is incoming Matrix, vtx is incoming vertex point
    blankVect = [0.0,0.0,0.0,0.0] #Blank Vector
    vtxVect = [vtx[0],vtx[1],vtx[2],1] #Vertex Vector
    blankVect[0] = (tMatrix[0]*vtxVect[0]) + (tMatrix[4]*vtxVect[1]) + (tMatrix[8]*vtxVect[2]) + (tMatrix[12]*vtxVect[3])
    blankVect[1] = (tMatrix[1]*vtxVect[0]) + (tMatrix[5]*vtxVect[1]) + (tMatrix[9]*vtxVect[2]) + (tMatrix[13]*vtxVect[3])
    blankVect[2] = (tMatrix[2]*vtxVect[0]) + (tMatrix[6]*vtxVect[1]) + (tMatrix[10]*vtxVect[2]) + (tMatrix[14]*vtxVect[3])
    returnedVect = [blankVect[0],blankVect[1], blankVect[2]] #Returned Vector
    return returnedVect

################ Get Vector From 2 Points    
def getVector(Vert1, Vert2):
    
    vector = [Vert2[0]-Vert1[0], Vert2[1]-Vert1[1], Vert2[2]-Vert1[2]]
    return vector
    
    
################ Calculate Magnitude of Vector    
def getMagnitude(x,y,z):
    
    mag = m.sqrt(((x)**2)+((y)**2)+((z)**2))
    
    return mag
    
############################################################################### Component Creation Functions #####################################################

def getFlowerAttr():
    
    pAmount     = cmds.intSliderGrp('pAmount', query = True, value = True)
    throwAwayPetal = createPetal()
    petalTransformMatrix = cmds.xform(throwAwayPetal, query = True, matrix = True, worldSpace = True)
    
    vert1 = cmds.getAttr(throwAwayPetal+".vt[29]")[0]
    vert2 = cmds.getAttr(throwAwayPetal+".vt[25]")[0]
    
    newVert1 = matrixMult(petalTransformMatrix, vert1)
    newVert2 = matrixMult(petalTransformMatrix, vert2)
    baseWidthVec = getVector(newVert1, newVert2)
    
    #Get Magnitude of the width of the petal
    bwVecMag = getMagnitude(baseWidthVec[0], baseWidthVec[1], baseWidthVec[2])
    
    cmds.delete(throwAwayPetal)
    innerAngle = (360.0 / pAmount)
    halfAngle = innerAngle/2
    flowerRad = (bwVecMag/2)/(m.sin(halfAngle*(m.pi/180)))
    
    return [innerAngle,halfAngle,flowerRad]

def createPetal():
    
    # Create Petal Material
    rgbP = cmds.colorSliderGrp('primaryColor', query = True, rgbValue = True)
    rgbS = cmds.colorSliderGrp('secondaryColor', query = True, rgbValue = True)
    petalMaterial = cmds.shadingNode('blinn', asShader = True, n = "petalMaterial")
    rampMaterial = cmds.shadingNode('ramp', asShader = True, n = "rampMaterial")
    cmds.setAttr(rampMaterial+".colorEntryList[0].color", rgbP[0], rgbP[1], rgbP[2], type = 'double3')
    cmds.setAttr(rampMaterial+".colorEntryList[0].position", 1)
    cmds.setAttr(rampMaterial+".colorEntryList[1].color", rgbS[0], rgbS[1], rgbS[2], type = 'double3')
    cmds.setAttr(rampMaterial+".colorEntryList[1].position", 0)
    cmds.connectAttr(rampMaterial+".outColor", petalMaterial+".color")
    petalSet = cmds.sets(petalMaterial, empty = True, r = True, noSurfaceShader = True)
    cmds.connectAttr(petalMaterial+".color", petalSet+".surfaceShader")
    
    #Ensure Soft Select is Off
    cmds.softSelect(sse =0)
    
    #Retrieve Variables from GUI
    pLength     = cmds.intSliderGrp('pLength', query = True, value = True)
    pTWidth     = cmds.intSliderGrp('pTWidth', query = True, value = True)
    pBWidth     = cmds.intSliderGrp('pBWidth', query = True, value = True)
    pWWidth     = cmds.intSliderGrp('pWWidth', query = True, value = True)
    pWWidthPos  = cmds.intSliderGrp('pWWidthPos', query = True, value = True)
    pTBCurve    = cmds.intSliderGrp('pTBCurve', query = True, value = True)
    pSSCurve    = cmds.intSliderGrp('pSSCurve', query = True, value = True)
    pAngle      = cmds.intSliderGrp('pAngle', query = True, value = True)
    
    #Create Base Petal
    petalBase = cmds.polyCube(n="Petal", w = 1, d = pLength, h = 0.1, sx = 4, sz = 4)[0]
    
    #Form Basic Shape 
    #Apply specified Length and Widest Width
    cmds.select(petalBase+".vtx[2]", petalBase+".vtx[7]", r = True)
    cmds.move(pLength, moveZ = True)
    
    cmds.select(petalBase+".vtx[1]", petalBase+".vtx[3]", petalBase+".vtx[6]", petalBase+".vtx[8]",r = True)
    cmds.move((pLength*0.75), moveZ = True, a = True)
    
    cmds.select(petalBase+".vtx[25]", petalBase+".vtx[30]",r = True)
    cmds.move(-(0.35), moveX = True, a = True)
    
    cmds.select( petalBase+".vtx[29]", petalBase+".vtx[34]",r = True)
    cmds.move((0.35), moveX = True, a = True)
    
    cmds.select(petalBase+".vtx[4]", petalBase+".vtx[9]", r = True)
    cmds.move((0.40), moveX = True, a = True)    
    
    cmds.select(petalBase+".vtx[0]", petalBase+".vtx[5]" ,r = True)
    cmds.move(-(0.40), moveX = True, a = True)
    
    cmds.select(petalBase+".vtx[14]", petalBase+".vtx[49]", petalBase+".vtx[24]", petalBase+".vtx[39]",r = True)
    cmds.move((0.48), moveX = True, a = True)
         
    cmds.select(petalBase+".vtx[10]", petalBase+".vtx[45]",petalBase+".vtx[20]", petalBase+".vtx[35]", r = True)
    cmds.move(-(0.48), moveX = True, a = True)
    
    cmds.select(petalBase, r = True)
    cmds.move(pLength*0.5, moveZ = True, a = True)
    
    #Apply Changes to Vertices Along X Axis
    if(pWWidth > 1):
       cmds.softSelect(sse = 1, ssd = 1.0) 
       cmds.select(petalBase+".vtx[15]", petalBase+".vtx[19]", petalBase+".vtx[40]", petalBase+".vtx[44]",r = True)
       cmds.scale(pWWidth*0.8, scaleX = True, a = True)
       cmds.softSelect(sse =0, ssd = 1.0)
        
    if(pBWidth > 1):
        cmds.softSelect(sse = 1, ssd = (pWWidth/3.0) + 1.0)
        cmds.select(petalBase+".vtx[25]", petalBase+".vtx[30]", petalBase+".vtx[29]", petalBase+".vtx[34]",r = True)
        cmds.scale(pBWidth*0.5, scaleX = True, a = True)
        cmds.softSelect(sse =0, ssd = 1.0)
        
    if(pTWidth > 1):
        cmds.softSelect(sse = 1, ssd = (pWWidth/3.0 + 1.0))
        cmds.select(petalBase+".vtx[1]", petalBase+".vtx[3]", petalBase+".vtx[6]", petalBase+".vtx[8]",r = True)
        cmds.scale(pTWidth*0.5, scaleX = True, a = True)
        cmds.softSelect(sse =0, ssd = 1.0)
    
    #Apply Changes to Vertices Along Z Axis   
    cmds.softSelect(sse = 1, ssd = pLength*0.66) 
    cmds.select(petalBase+".vtx[15:19]", petalBase+".vtx[40:44]", r = True)
    cmds.move(pWWidthPos * (pLength*0.045), moveZ = True, r = True)
    cmds.select(petalBase+".vtx[25:34]", r = True)
    cmds.move(0,moveZ = True, a = True)
    cmds.softSelect(sse =0, ssd = 1.0)   
    cmds.select(clear = True)
    
    bendSS = cmds.nonLinear(petalBase, type = 'bend', curvature = pSSCurve*2.0*pLength)
    cmds.select(bendSS[1], r = True)
    cmds.rotate(90, z = True, a = True)
    
    bendTB = cmds.nonLinear(petalBase, type = 'bend', curvature = pTBCurve*2.0)
    cmds.select(bendTB[1], r = True)
    cmds.rotate(90, z = True, a = True)
    cmds.rotate(90, x = True, a = True)
    
    cmds.select(petalBase)
    cmds.delete(ch = True)
    
    petalTransformMatrix = cmds.xform(petalBase, query = True, matrix = True, worldSpace = True)
    
    vert1 = cmds.getAttr(petalBase+".vt[27]")[0]
    
    newVert1 = matrixMult(petalTransformMatrix, vert1)
    
    vert2 = cmds.getAttr(petalBase+".vt[32]")[0]
    
    newVert2 = matrixMult(petalTransformMatrix, vert2)
    
    
    cP = (newVert1[1]+newVert2[1])/2
    
    cmds.move(newVert1[0], cP, newVert1[2], petalBase+".scalePivot",petalBase+".rotatePivot", absolute=True)
    cmds.select(petalBase, r = True)
    
    cmds.move(-newVert1[0], moveX = True, r = True)
    cmds.move(-cP, moveY = True, r = True)
    cmds.move(-newVert1[2], moveZ = True, r = True)
    
    #rotate petal to account for input angle, and angle created by applying bend to petal
    cmds.rotate(-(pAngle+(pTBCurve*2)), x = True, r = True)
    cmds.hyperShade(petalBase, assign = petalMaterial)
    return petalBase

################ Create Basic petal
def createBasicPetal():
    #Create Base Petal
    petalBase = cmds.polyCube(n="Petal", w = 1, d = 1, h = 0.1, sx = 4, sz = 4)[0]
    
    #Form Basic Shape 
    #Apply specified Length and Widest Width
    cmds.select(petalBase+".vtx[2]", petalBase+".vtx[7]", r = True)
    cmds.move(1, moveZ = True)
    
    cmds.select(petalBase+".vtx[1]", petalBase+".vtx[3]", petalBase+".vtx[6]", petalBase+".vtx[8]",r = True)
    cmds.move(0.75, moveZ = True, a = True)
    
    cmds.select(petalBase+".vtx[25]", petalBase+".vtx[30]",r = True)
    cmds.move(-(0.35), moveX = True, a = True)
    
    cmds.select( petalBase+".vtx[29]", petalBase+".vtx[34]",r = True)
    cmds.move((0.35), moveX = True, a = True)
    
    cmds.select(petalBase+".vtx[4]", petalBase+".vtx[9]", r = True)
    cmds.move((0.40), moveX = True, a = True)    
    
    cmds.select(petalBase+".vtx[0]", petalBase+".vtx[5]" ,r = True)
    cmds.move(-(0.40), moveX = True, a = True)
    
    cmds.select(petalBase+".vtx[14]", petalBase+".vtx[49]", petalBase+".vtx[24]", petalBase+".vtx[39]",r = True)
    cmds.move((0.48), moveX = True, a = True)
         
    cmds.select(petalBase+".vtx[10]", petalBase+".vtx[45]",petalBase+".vtx[20]", petalBase+".vtx[35]", r = True)
    cmds.move(-(0.48), moveX = True, a = True)
    
    cmds.select(petalBase, r = True)
    cmds.move(0.5, moveZ = True, a = True)
    
    petalTransformMatrix = cmds.xform(petalBase, query = True, matrix = True, worldSpace = True)
    
    vert1 = cmds.getAttr(petalBase+".vt[27]")[0]
    
    newVert1 = matrixMult(petalTransformMatrix, vert1)
    
    vert2 = cmds.getAttr(petalBase+".vt[32]")[0]
    
    newVert2 = matrixMult(petalTransformMatrix, vert2)
    
    
    cP = (newVert1[1]+newVert2[1])/2
    #Move pivot point to correct position
    cmds.move(newVert1[0], cP, newVert1[2], petalBase+".scalePivot",petalBase+".rotatePivot", absolute=True)
    cmds.select(petalBase, r = True)
    
    cmds.move(-newVert1[0], moveX = True, r = True)
    cmds.move(-cP, moveY = True, r = True)
    cmds.move(-newVert1[2], moveZ = True, r = True)
    
    #rotate petal to account for input angle, and angle created by applying bend to petal
    cmds.rotate(-12, x = True, r = True)
    
    return petalBase      

############# Create Pistil and Stamen     
def createPistilAndStamen(flowerRad):
    stamenArray = []
    pAmount     = cmds.intSliderGrp('pAmount', query = True, value = True)
    
    #Create pistil shape
    pistil = cmds.polySphere(r = flowerRad/3.0)[0]
    cmds.move(flowerRad/3.0, moveY = True, r = True)
    cmds.softSelect(sse = 1, ssd = flowerRad/3.0)
    cmds.select(pistil+".e[200:219]", r = True)
    cmds.scale(0.35, z = True, r = True)
    cmds.scale(0.35, x = True, r = True)
    cmds.softSelect(sse = 0, ssd = 1)
    cmds.select(pistil, r = True)
    cmds.move(0,0,0, pistil+".scalePivot",pistil+".rotatePivot", absolute=True)
    cmds.scale(2, y = True, r = True)
    
    #Create Original Stamen
    orgStamenStalk = cmds.polyCylinder(r = 0.05, h = flowerRad, sy = 30)[0]
    cmds.move(flowerRad/2.0, moveY = True, r = True)
    orgStamenEnd = cmds.polySphere(r = 0.07)[0]
    cmds.move(flowerRad, moveY = True, r = True)
    cmds.scale(2.5, y = True, r = True)
    cmds.rotate(-45, z = True, r = True)
    flareD = cmds.nonLinear(orgStamenStalk, type = 'flare')
    cmds.nonLinear(flareD[0], edit = True, startFlareX = 1.1, startFlareZ = 1.1, endFlareX = 0.8, endFlareZ = 0.8)
    cmds.select(orgStamenStalk, r = True)
    cmds.delete(ch=True)
    
    cmds.select(orgStamenEnd, r = True)
    cmds.select(orgStamenStalk, add = True)
    cmds.parent()
    
    #Create final Stamen
    for i in range(pAmount):
        cmds.select(orgStamenStalk, r = True)
        newStamenStalk = cmds.duplicate()[0]
        bendCurve = r.uniform(10.0,20.0)
        bend = cmds.nonLinear(newStamenStalk, type = 'bend', curvature = -bendCurve)
        cmds.select(newStamenStalk, r = True)
        cmds.delete(ch=True)
        cmds.rotate(bendCurve, z = True, r = True, p = [0,0,0])
        cmds.move(flowerRad, moveX = True, r = True)
        cmds.rotate(i*(360.0/pAmount), y = True, r = True, p = [0,0,0])
        stamenArray.append(newStamenStalk)
        
    cmds.select(orgStamenStalk, r = True)
    cmds.delete()
    
    cmds.select(clear = True)
    
    for stalk in stamenArray:
        cmds.select(stalk, add = True)
    cmds.select(pistil, add = True)
    cmds.parent()
    return pistil
    
############# Create Sepal    
def createSepal(radius,pOrders, yValue):
    sepalPetalArray = []
    pAmount     = cmds.intSliderGrp('pAmount', query = True, value = True)
    sepalSphere = cmds.polySphere(r = radius+0.26)[0]
    cmds.select(sepalSphere, r = True)
    if pOrders > 1:
        cmds.scale(1+(pOrders)/5.0, x = True, a = True)
        cmds.scale(1+(pOrders)/5.0,z = True, a = True)
    cmds.scale(0.5, y = True, a = True)
    
    #Delete edges and vertices of sphere to create proper shape
    cmds.select(sepalSphere+".e[200:379]", r = True)
    cmds.delete()
    
    cmds.select(sepalSphere+".vtx[200:379]", r = True)
    cmds.delete()
    
    # move shape to origin
    cmds.select(sepalSphere+".vtx[201]", r = True)
    cmds.move(0 , y = True, a = True)
    
    #Harden Edge
    cmds.select(sepalSphere+".e[180:199]", r = True)
    cmds.polySoftEdge(a = 0)
    
    #Move shape to appropriate spot
    cmds.select(sepalSphere, r = True)
    cmds.move((yValue)+(0.05), y = True, r = True)
    
    #Find vertex on sepal sphere
    sepalSphereTransformMatrix = cmds.xform(sepalSphere, query = True, matrix = True, worldSpace = True)
    ssVert1 = cmds.getAttr(sepalSphere+".vt[200]")[0]
    newSSVert1 = matrixMult(sepalSphereTransformMatrix, ssVert1)
    
    #create sepal leaves
    
    throwAwayPetal = createBasicPetal()
    petalTransformMatrix = cmds.xform(throwAwayPetal, query = True, matrix = True, worldSpace = True)
    
    vert1 = cmds.getAttr(throwAwayPetal+".vt[24]")[0]
    vert2 = cmds.getAttr(throwAwayPetal+".vt[20]")[0]
    
    newVert1 = matrixMult(petalTransformMatrix, vert1)
    newVert2 = matrixMult(petalTransformMatrix, vert2)
    baseWidthVec = getVector(newVert1, newVert2)
    
    #Get Magnitude of the width of the petal
    bwVecMag = getMagnitude(baseWidthVec[0], baseWidthVec[1], baseWidthVec[2])
    
    cmds.delete(throwAwayPetal)
    
    innerAngle = (360.0 / 5)
    halfAngle = innerAngle/2
    flowerRad = (bwVecMag/2)/(m.sin(halfAngle*(m.pi/180)))
    
    petalDistance = (m.sin((180 - halfAngle - 90)*(m.pi/180))* flowerRad)
    
    cmds.select(clear = True)
    
    #Create and rotate petal shape to make sepal flowers
    for i in range(5):
        petal = createBasicPetal()
      
        cmds.select(petal, r = True)
        #cmds.move(petalDistance, moveZ =True, r = True)
        cmds.rotate((i*innerAngle), y= True, a = True, p = (0, 0, 0))
        
        sepalPetalArray.append(petal)
    
    cmds.select(clear = True)
        
    for petals in sepalPetalArray:
        cmds.select(petals, add = True)
        
    #Combine and move sepal leaves to correct position 
    sepalLeaves = cmds.polyCBoolOp( op=1, o = True)[0]
    sepalLeavesTransformMatrix = cmds.xform(sepalLeaves, query = True, matrix = True, worldSpace = True)
    slVert1 = cmds.getAttr(sepalLeaves+".vt[44]")[0]
    newSLVert1 = matrixMult(sepalLeavesTransformMatrix, slVert1)
    cmds.move(newSLVert1[0], newSLVert1[1], newSLVert1[2], sepalLeaves+".scalePivot",sepalLeaves+".rotatePivot", absolute=True)
    
    cmds.select(sepalLeaves, r = True)
    cmds.move(newSSVert1[0],newSSVert1[1],newSSVert1[2], a = True)
    cmds.move(-(pAmount/100.0), y = True, r = True)
    if pOrders > 1:
        cmds.scale(1+(pOrders)/5.0, x = True, a = True)
        cmds.scale(1+(pOrders)/5.0,z = True, a = True)
        
    cmds.select(sepalSphere, add = True)
    #Merge sepal shapes together
    sepalShape = cmds.polyUnite(ch = False)[0]
    cmds.move(0,(yValue)+(0.05),0,sepalShape+".scalePivot",sepalShape+".rotatePivot", absolute=True)
    return sepalShape


############# Create Normal Flower      
def createFlower():
    petalArray = []
    petalRingArray = []
    flowerVertexYArray = []
    
    petalOrders = cmds.intSliderGrp('orders', query = True, value = True)
    addPS = cmds.checkBox('addPS', q = True, v = True)
    pAmount     = cmds.intSliderGrp('pAmount', query = True, value = True)
    
    flowerAttr = getFlowerAttr()
    innerAngle = flowerAttr[0]
    halfAngle = flowerAttr[1]
    flowerRad = flowerAttr[2]
    
    petalDistance = (m.sin((180 - halfAngle - 90)*(m.pi/180))* flowerRad)
    
    
    cmds.select(clear = True)
    #Create Petal Rings
    for j in range(petalOrders):
        for i in range(pAmount):
            petal = createPetal()
          
            cmds.select(petal, r = True)
            cmds.move(petalDistance, moveZ =True, r = True)
            cmds.rotate((i*innerAngle), y= True, a = True, p = (0, 0, 0))
            
            
            petalArray.append(petal)
            
        for petal in petalArray: 
            cmds.select(petal, add = True)
        
        petalRing = cmds.polyUnite(ch = False)[0]
        
        if (j+1)%2 == 0:
            cmds.select(petalRing, r = True)
            cmds.rotate((innerAngle/2), y = True, a = True, p = (0,0,0))
        
        if j+1>0:
            cmds.scale(1+(j+1)/5.0, x = True, a = True)
            cmds.scale(1+(j+1)/5.0,z = True, a = True)
            
        cmds.move(-0.05*(j), y = True, r = True)
        petalRingArray.append(petalRing)
        petalArray = []
     
    #Create Flower Center
    middleFlower = cmds.polySphere(r = flowerRad*1.5)[0]
    cmds.select(middleFlower, r = True)
    if (pAmount % 2 == 0):
        cmds.rotate(90+halfAngle, y = True, a = True)
    else:
        cmds.rotate(90, y = True, a = True)
    
    cmds.scale(0.5, y = True, a = True)
    
    sepal = createSepal(flowerRad, petalOrders,(-0.05*petalOrders))
    
    cmds.select(sepal, r = True)
    
    for petalRing in petalRingArray: 
                cmds.select(petalRing, add = True)
    cmds.select(middleFlower, add = True)  
     
    cmds.parent()
    
    #Find vertex with lowest Y value, translate object up in the Y direction by that magnitude.
    
    vertexCountSepal = cmds.polyEvaluate(sepal, vertex=True)
    
    SepalTransformMatrix = cmds.xform(sepal, query = True, matrix = True, worldSpace = True)
    for vert in range(0, vertexCountSepal):
        
        vertex = cmds.getAttr(sepal + ".vt[" + str(vert) + "]")
        newVertex = matrixMult(SepalTransformMatrix, list(vertex[0]))
        flowerVertexYArray.append(newVertex[1])
        
    lowestY = min(flowerVertexYArray)
    cmds.select(middleFlower, r = True)
    cmds.move(-lowestY, y = True, r = True)
    
    if(addPS):
        pistil = createPistilAndStamen(flowerRad)
        cmds.select(pistil, r = True)
        cmds.move(-lowestY*1.5, y = True, r = True)
        cmds.select(middleFlower, add = True)
        cmds.parent()
        
    return middleFlower

############### Create Stem Function
def createStem():
    leafArray = []
    #Check user choices
    pAmount     = cmds.intSliderGrp('pAmount', query = True, value = True)
    addThorns = cmds.checkBox('addThorns', q = True, v = True)
    addLeaves = cmds.checkBox('addLeaves', q = True, v = True)
    
    #Create stem base
    stemBase = cmds.polyCylinder(r = 0.15, h = (6), sx = 10, sy = (60))[0]
    cmds.move(-2.95, y = True, r = True)
    cmds.move(0,0,0, stemBase+".scalePivot",stemBase+".rotatePivot", absolute=True)
    
    
    #if thorns selected
    if addThorns:
        faceCount = cmds.polyEvaluate(stemBase, face=True)
        numThorns = r.randint(30,60)
        i = 0
        
        cmds.select(clear = True)
        
        for j in range(numThorns):
            i += r.randint(15,30)
            if i < (faceCount - 3):
                cmds.select(stemBase+".f["+str(i)+"]", add = True)    
        cmds.polyExtrudeFacet(ltz = 0.1, off = 0.046)
    
    #if leaves selected    
    if addLeaves:
        leaf = createBasicPetal()
        cmds.select(leaf+".vtx[0:24]", r = True)
        cmds.select(leaf+".vtx[35:49]", add = True)
        cmds.move(0.3, moveZ = True, r = True)
        cmds.select(leaf+".vtx[25:34]", r = True)
        cmds.scale(0.5, 1, 1, r = True)
        cmds.select(leaf, r = True)
        cmds.scale(0.5,0.5,0.5, r = True)
        
        #place random amount of leaves at random positions along the stem
        for i in range(r.randint(3,10)):
            newLeaf = cmds.duplicate(leaf, inputConnections = True)[0]
            cmds.select(newLeaf, r = True)
            cmds.move(-(r.uniform(0.5, 5.5)), moveY = True, a = True)
            cmds.rotate((r.uniform(1.0, 360.0)), y = True, r = True)
            cmds.rotate((r.uniform(1.0, 45.0)), z = True, r = True)
            cmds.rotate((r.uniform(-20.0, 20.0)), x = True, r = True)
            leafArray.append(newLeaf)
        cmds.delete(leaf) 
        cmds.select(clear=True)
        for leaf in leafArray:
            cmds.select(leaf, add = True)                               
        cmds.select(stemBase, add = True)
        cmds.parent()   

    #Scale stem to fit with flower
    cmds.select(stemBase, r = True)
    cmds.scale((pAmount/3.0), x = True)    
    cmds.scale((pAmount/3.0), y = True)  
    cmds.scale((pAmount/3.0), z = True)  
    
    
    
    return stemBase
        

        
def createTubeFlowerShape():
    petalArray = []
    flowerVertexYArray = []
    pAmount     = cmds.intSliderGrp('pAmount', query = True, value = True)
    tLength     = cmds.intSliderGrp('tLength', query = True, value = True)
    tBWidth     = cmds.intSliderGrp('tBWidth', query = True, value = True)
    #Get Dimensions of petal and flower
    flowerAttr = getFlowerAttr()
    innerAngle = flowerAttr[0]
    halfAngle = flowerAttr[1]
    flowerRad = flowerAttr[2]
    petalDistance = (m.sin((180 - halfAngle - 90)*(m.pi/180))* flowerRad)
    
    #Create petal ring
    for i in range(pAmount):
        petal = createPetal()
      
        cmds.select(petal, r = True)
        cmds.move(petalDistance, moveZ =True, r = True)
        cmds.rotate((i*innerAngle), y= True, a = True, p = (0, 0, 0))
        
        
        petalArray.append(petal)
    #Create and rotate flower's tube    
    tube = cmds.polyPipe(r = flowerRad+0.1, sa = pAmount, t = 0.1, h = tLength)[0]
    cmds.select(tube, r = True)
    if (pAmount % 2 == 0):
        cmds.rotate(90+halfAngle, y = True, a = True)
    else:
        cmds.rotate(90, y = True, a = True)
    
    cmds.move(-(tLength/4.0), y = True, a = True)
    
    cmds.select(tube+".f["+str(pAmount*3)+":"+str(pAmount*4)+"]", r = True)
    cmds.scale((tBWidth/5.0), x = True, r = True)
    cmds.scale((tBWidth/5.0), z = True, r = True)
    sepal = createSepal(flowerRad+0.1,1,-((tLength/2.0)-0.05))
    cmds.scale((tBWidth/5.0), x = True, r = True)
    cmds.scale((tBWidth/5.0), y = True, r = True)
    cmds.scale((tBWidth/5.0), z = True, r = True)
    
    cmds.select(tube, r = True)
   
    for petal in petalArray:
        cmds.select(petal, add = True)
        
    tubeFlower = cmds.polyCBoolOp(op=1, o = True)[0]
    cmds.select(sepal, r = True)
    cmds.select(tubeFlower, add = True)
    
    cmds.parent()
    
    #Find vertex with lowest Y value, translate object up in the Y direction by that magnitude.
    vertexCountSepal = cmds.polyEvaluate(sepal, vertex=True)
    
    SepalTransformMatrix = cmds.xform(sepal, query = True, matrix = True, worldSpace = True)
    for vert in range(0, vertexCountSepal):
        
        vertex = cmds.getAttr(sepal + ".vt[" + str(vert) + "]")
        newVertex = matrixMult(SepalTransformMatrix, list(vertex[0]))
        flowerVertexYArray.append(newVertex[1])
        
    lowestY = min(flowerVertexYArray)
    cmds.select(tubeFlower, r = True)
    cmds.move(-lowestY, y = True, r = True)
    
    returnedPackage = (tubeFlower, (flowerRad+0.1)*(tBWidth/5.0))
    return returnedPackage


############################################################################### High Level Functions #################################################################
    
############# High Level Function to Create Normal Flower    
def createNormalFlower():
    #Retreive Normal Flower Components and Combine
    flowerTop = createFlower()
    flowerStem = createStem()
    
    normalFlower = cmds.polyUnite(flowerTop, flowerStem)[0]
    cmds.delete(all = True, ch = True)
    return normalFlower
    
############## High Level Function to Create Tube Flower
def createTubeFlower():
    #Retreive Tube Flower Components and Combine
    package = createTubeFlowerShape()
    flowerTop = package[0]
    flowerStem = createStem()
    tubeFlower = cmds.polyUnite(flowerTop, flowerStem)[0]
    cmds.delete(all = True, ch = True)
    return tubeFlower
    

############# High Level Function to Create Spike Flower
def createSpikeFlower():
    #Create Spike Flowers using the Tube Flower Shape
    package = createTubeFlowerShape()
    flowerArrayGroup = []
    pLength = cmds.intSliderGrp('pLength', query = True, value = True)
    tLength = cmds.intSliderGrp('tLength', query = True, value = True)
    flower = package[0]
    radius = (package[1]*2.0) + pLength
    numRows = cmds.intSliderGrp('sfRows', query = True, value = True)
    rowDensity = cmds.intSliderGrp('sfDensity', query = True, value = True)
    stemBase = cmds.polyCylinder(r = radius, h = radius*40)
    cmds.move(-((radius*40)/2), moveY = True, r = True)
    cmds.select(flower, r = True)
    cmds.move(0,0,0,flower+".scalePivot",flower+".rotatePivot", absolute=True)
    cmds.rotate(-78, x = True, r = True,)
    cmds.move(-radius, z = True, r = True)
    cmds.makeIdentity(a = True, t = 1, r = 1, s = 1, n = 0, pn = 1)
    
    #Create Number of Flower Rows Specified By User
    for j in range(numRows):
        flowerArray = []
        spacing = (((radius*4)- (rowDensity/10))*j) 
        for i in range(4):
            newFlower = cmds.duplicate(flower)[0]
            cmds.select(newFlower, r = True)
            cmds.rotate(i*90.0, y = True, a = True, p = [0,0,0])
            flowerArray.append(newFlower)
            flowerArrayGroup.append(newFlower)
            print newFlower
            
            for flower in flowerArray:
                cmds.select(flower, r = True)
                cmds.move(-spacing, moveY = True, a = True)
    
                
    cmds.select(stemBase, r = True)
     
    for flower in flowerArrayGroup:          
       cmds.select(flower, add = True)
       #print flower
        
    spikeFlower = cmds.polyUnite()[0]
    cmds.delete(all = True, ch = True)
    return spikeFlower
    
def createArrangement():
    
    flowerArray = []
    
    fAmount     = cmds.intSliderGrp('fAmount', query = True, value = True)
    fChoice     = cmds.radioButtonGrp('fChoice', query = True, sl = True)
    fArrang     = cmds.radioButtonGrp('fArrangement', query = True, sl = True)
    
    flowerAttr = getFlowerAttr()
    innerAngle = flowerAttr[0]
    halfAngle = flowerAttr[1]
    flowerRad = flowerAttr[2]
    
    #If Random Arrangment Chosen
    if fArrang == 1:
        positionArray = []
        
        if fChoice == 1:
            for i in range (fAmount):
                flowerArray.append(createNormalFlower())
        if fChoice == 2:
            for i in range (fAmount):
                flowerArray.append(createTubeFlower())
                
        if fChoice == 3:
            for i in range (fAmount):
                flowerArray.append(createSpikeFlower())
    
        for flower in flowerArray:
            isValid = True
            position = [0,0]
            while isValid:
                isValid = False
                
                for pos in positionArray:
                    position = [(r.randint(0,50)),(r.randint(0,50))]
                    if position[0] > pos[0]-(flowerRad*2.0) and position[0] < pos[0]+(flowerRad*2.0) and position[1] > pos[1]-(flowerRad*2.0) and position[1] < pos[1]+(flowerRad*2.0):
                        isValid = True
                        break
                        
            positionArray.append(position)
            cmds.select(flower, r = True)
            cmds.move(position[0],0,position[1], a = True)
    
    #If Linear Arrangement Chosen        
    if fArrang == 2:
        positionArray = []
        counter = 0
        iAmount = 0
        if (fAmount % 4) == 0:
            iAmount = (fAmount-(fAmount % 4))/4
            
        if (fAmount % 4) != 0:
            iAmount = ((fAmount-(fAmount % 4))/4)+1
            
        if fChoice == 1:
            for i in range(iAmount):
                for j in range(4):
                    if counter < fAmount:
                        flower = createNormalFlower()
                        cmds.select(flower, r = True)
                        cmds.move((i*flowerRad*10.0), 0 , (j*flowerRad*10.0), a = True)
                        flowerArray.append(flower)
                        counter+=1
        
        if fChoice == 2:
            for i in range((fAmount-(fAmount % 4))/4):
                print i
                for j in range(4):
                    if counter < fAmount:
                        flower = createTubeFlower()
                        cmds.select(flower, r = True)
                        cmds.move((i*flowerRad*10.0), 0 , (j*flowerRad*10.0), a = True)
                        flowerArray.append(flower)
                        counter+=1
                        
        if fChoice == 3:
            for i in range((fAmount-(fAmount % 4))/4):
                print i
                for j in range(4):
                    if counter < fAmount:
                        flower = createTubeFlower()
                        cmds.select(flower, r = True)
                        cmds.move((i*flowerRad*10.0), 0 , (j*flowerRad*10.0), a = True)
                        flowerArray.append(flower)
                        counter+=1
                        
                
    # If Fractal Arrangement option chosen                            
    if fArrang == 3:
        vertexArray = kochCurve()
        amount = len(vertexArray)
        if fChoice == 1:
            for i in range (amount):
                flower = createNormalFlower()
                cmds.select(flower, r = True)
                cmds.move(vertexArray[i-1][0],0,vertexArray[i-1][2], a = True)
        if fChoice == 2:
            for i in range (amount):
                flower = createTubeFlower()
                cmds.select(flower, r = True)
                cmds.move(vertexArray[i-1][0],0,vertexArray[i-1][2], a = True)
        
    
    cmds.delete(all = True, ch = True)

def kochCurve():
    
    #Find dimensions of petals and flower geometry
    pLength     = cmds.intSliderGrp('pLength', query = True, value = True)
    pAmount     = cmds.intSliderGrp('pAmount', query = True, value = True)
    fAmount     = cmds.intSliderGrp('fAmount', query = True, value = True)
    baseArray = []
    kochVertexArray = []
    flowerAttr = getFlowerAttr()
    innerAngle = flowerAttr[0]
    halfAngle = flowerAttr[1]
    flowerRad = flowerAttr[2]
    
    flowerDiam = ((2*flowerRad)+(2*pLength))
    
    #Create Pyramid to make base of Koch Curve
    base = cmds.polyPyramid(w = (flowerDiam*fAmount), ns = 3)[0]
    cmds.select(base+".f[1:3]", r = True)
    cmds.delete()
    cmds.select(base, r = True)
    cmds.delete(ch=True)
    
    edgeCount = cmds.polyEvaluate(base, edge=True)
    
    #Add a vertex in the middle of each edge
    for i in range(edgeCount):
        cmds.select(base, r = True)
        cmds.polySplit( ip = [(i,0.5)] )
    
    baseArray.append(base)   
    
    #Create a smaller triangle for each order of the Koch Curve
    for j in range(1,4):
        prevBase = baseArray[j-1]
        baseTransformMatrix = cmds.xform(prevBase, query = True, matrix = True, worldSpace = True)
        prevBaseVert = cmds.pointPosition(prevBase+".vtx[4]", world = True)
        cmds.select(prevBase, r = True)
        
        newBase = cmds.duplicate()[0]
        newBaseVert = cmds.pointPosition(newBase+".vtx[3]", world = True)
        translateVector = getVector(newBaseVert, prevBaseVert)
        cmds.move(newBaseVert[0], newBaseVert[1], newBaseVert[2], newBase+".scalePivot",newBase+".rotatePivot", absolute=True)

        cmds.move(translateVector[0],translateVector[1],translateVector[2], r = True)
        cmds.rotate(-60, y = True, r = True)
        cmds.scale(0.5,0.5,0.5, r = True)
        
        baseArray.append(newBase)
    
    #Starting from the highest order or the Koch Curve, Duplicate the order's triangle, and rotate with the center of the next lowest order triangle's center.   
    for n in range(4,1,-1):
        print n
        currentBase = baseArray[n-1]
        nextBase = baseArray[n-2]
        nextBaseV1 = cmds.pointPosition(nextBase+".vtx[0]", world = True)
        nextBaseV2 = cmds.pointPosition(nextBase+".vtx[1]", world = True)
        nextBaseV3 = cmds.pointPosition(nextBase+".vtx[2]", world = True)
        nextBaseCenter = [((nextBaseV1[0]+nextBaseV2[0]+nextBaseV3[0])/3),(nextBaseV1[1]), ((nextBaseV1[2]+nextBaseV2[2]+nextBaseV3[2])/3)]
        #Delete vertices which will not be used for flower placement
        cmds.select(currentBase+".vtx[3:5]", r = True)
        cmds.delete()
        
        dupeBase = []
        if n != 2:
            cmds.select(currentBase, r = True)
            dupeBase.append(cmds.duplicate(rc = True)[0])
            cmds.select(dupeBase[0], r=True)
            cmds.rotate(120, y = True, r = True, p = [(nextBaseCenter[0]),(nextBaseCenter[1]),(nextBaseCenter[2])])
        if n == 2:
            for i in range(1,3):
                cmds.select(currentBase, r = True)
                temp = cmds.duplicate(rc = True)[0]
                cmds.select(temp, r=True)
                cmds.rotate(i*120, y = True, r = True, p = [(nextBaseCenter[0]),(nextBaseCenter[1]),(nextBaseCenter[2])])
                dupeBase.append(temp)
                
        for i in dupeBase:
            baseArray.append(i)
        #Parent the two highest order triangles with the next lowest order triangle    
        cmds.select(currentBase, r = True)
        cmds.select(dupeBase, add = True)
        cmds.select(nextBase, add = True)
        cmds.parent()
    
    cmds.select(clear = True)
    #Combine the triangles
    for triangle in baseArray:
        cmds.select(triangle, add = True)
    kochCurve = cmds.polyUnite()[0]
    
    #Get Vertices and pass them to flower arrangment function
    cmds.select(kochCurve, r = True)
    cmds.scale(flowerDiam*5, flowerDiam*5, flowerDiam*5, r = True)
    vertexCountKC = cmds.polyEvaluate(kochCurve, vertex=True)
    
    for vert in range(vertexCountKC):
        kochVertexArray.append(cmds.pointPosition(kochCurve+".vtx["+str(vert)+"]", world = True))
        print vert
    
    cmds.delete(kochCurve)
    return kochVertexArray

    
#GUI Specifications
GUIWindow = cmds.window(title="Floral Mesh Generator", menuBar=True)

cmds.menu(label = "Basic Options")
cmds.menuItem (label = "New Scene", command = ('cmds.file(new=True, force=True)'))
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'))

cmds.columnLayout()

#Section for square blocks without holes
cmds.frameLayout(collapsable=True, label="General Attributes")
cmds.columnLayout()
cmds.colorSliderGrp('primaryColor', label = "Primary Colour", hsv = (120, 1, 1))
cmds.colorSliderGrp('secondaryColor', label = "Secondary Colour", hsv = (120, 1, 1))
cmds.intSliderGrp('pLength', label = "Petal Length", field = True, min = 1, max = 10, value = 1)
cmds.intSliderGrp('pTWidth', label = "Petal Tip Width", field = True, min = 1, max = 5, value = 1)
cmds.intSliderGrp('pBWidth', label = "Petal Base Width", field = True, min = 1, max = 5, value = 1)
cmds.intSliderGrp('pWWidth', label = "Petal Widest Width", field = True, min = 1, max = 3, value = 1)
cmds.intSliderGrp('pWWidthPos', label = "Widest Width Position", field = True, min = -10, max = 10, value = 0)
cmds.intSliderGrp('pTBCurve', label = "Petal Tip to Base Curve", field = True, min = 0, max = 20, value = 0)
cmds.intSliderGrp('pSSCurve', label = "Petal Sides Curve", field = True, min = 0, max = 20, value = 0)
cmds.intSliderGrp('pAngle', label = "Angle of Petal", field = True, min = 0, max = 45, value = 0)
cmds.intSliderGrp('pAmount', label = "Petal Quantity", field = True, min = 3, max = 10, value = 3)
cmds.checkBox('addPS', label = "Include Pistil and Stamen")
cmds.checkBox('addThorns', label = "Add Thorns")
cmds.checkBox('addLeaves', label = "Add Leaves")
cmds.setParent('..')
cmds.setParent('..')

# Regular Flower Options
cmds.frameLayout(collapsable=True, label="Regular Flower")
cmds.columnLayout()
cmds.intSliderGrp('orders', label = "Amount of Orders", field = True, min = 1, max = 5, value = 1)
cmds.button(label = "Create Flower", command="createNormalFlower()" )
cmds.setParent('..')
cmds.setParent('..')

#Tube Flower Options
cmds.frameLayout(collapsable=True, label="Tube Flower")
cmds.columnLayout()
cmds.intSliderGrp('tLength', label = "Tube Length", field = True, min = 5, max = 10, value = 5)
cmds.intSliderGrp('tBWidth', label = "Tube Bottom Width", field = True, min = 1, max = 10, value = 5)
cmds.button(label = "Create Tube Flower", command="createTubeFlower()" )
cmds.setParent('..')
cmds.setParent('..')

# Spike Flower Options
cmds.frameLayout(collapsable=True, label="Spike Flower")
cmds.columnLayout()
cmds.intSliderGrp('sfRows', label = "Flower Rows", field = True, min = 3, max = 10, value = 3)
cmds.intSliderGrp('sfDensity', label = "Flower Density", field = True, min = 3, max = 10, value = 3)
cmds.button(label = "Create Flower", command="createSpikeFlower()" )
cmds.setParent('..')
cmds.setParent('..')

# Flower Arrangment Options
cmds.frameLayout(collapsable=True, label="Flower Arrangements")
cmds.columnLayout()
cmds.intSliderGrp('fAmount', label = "Flower Amount", field = True, min = 1, max = 20, value = 1)
cmds.radioButtonGrp( 'fChoice', label='Select A Flower', labelArray3=['Normal', 'Tube', 'Spike'], numberOfRadioButtons=3, select = 1 )
cmds.radioButtonGrp( 'fArrangement', label='Select An Arrangement', labelArray3=['Random', 'Lines', 'Fractal'], numberOfRadioButtons=3, select = 1 )
cmds.button(label = "Create", command="createArrangement()" )
cmds.setParent('..')
cmds.setParent('..')


#Show window when script is run
cmds.showWindow(GUIWindow)

