import maya.cmds as cmds

################ Function that creates listed materials when called
def createMaterials():
    
    blackMaterial = cmds.shadingNode('blinn', asShader = True, n = "blackMaterial")
    cmds.setAttr(blackMaterial+".color", 27/255.0, 42/255.0, 52/255.0, type = 'double3')
    blackSet = cmds.sets(blackMaterial, empty = True, r = True, noSurfaceShader = True)
    cmds.connectAttr(blackMaterial+".color", blackSet+".surfaceShader")
    
    matteBlackMaterial = cmds.shadingNode('lambert', asShader = True, n = "matteBlackMaterial")
    cmds.setAttr(matteBlackMaterial+".color", 27/255.0, 42/255.0, 52/255.0, type = 'double3')
    matteBlackSet = cmds.sets(matteBlackMaterial, empty = True, r = True, noSurfaceShader = True)
    cmds.connectAttr(matteBlackMaterial+".color", matteBlackSet+".surfaceShader")
    
    whiteMaterial = cmds.shadingNode('blinn', asShader = True, n = "whiteMaterial")
    cmds.setAttr(whiteMaterial+".color", 242/255.0, 243/255.0, 242/255.0, type = 'double3')
    whiteSet = cmds.sets(whiteMaterial, empty = True, r = True, noSurfaceShader = True)
    cmds.connectAttr(whiteMaterial+".color", whiteSet+".surfaceShader")
    
    greyMaterial = cmds.shadingNode('blinn', asShader = True, n = "greyMaterial")
    cmds.setAttr(greyMaterial+".color", 161/255.0, 165/255.0, 162/255.0, type = 'double3')
    greySet = cmds.sets(greyMaterial, empty = True, r = True, noSurfaceShader = True)
    cmds.connectAttr(greyMaterial+".color", greySet+".surfaceShader")
    
    darkGreyMaterial = cmds.shadingNode('blinn', asShader = True, n = "darkGreyMaterial")
    cmds.setAttr(darkGreyMaterial+".color", 109/255.0, 110/255.0, 108/255.0, type = 'double3')
    darkGreySet = cmds.sets(darkGreyMaterial, empty = True, r = True , noSurfaceShader = True)
    cmds.connectAttr(darkGreyMaterial+".color", darkGreySet+".surfaceShader")
    
    redMaterial = cmds.shadingNode('blinn', asShader = True, n = "redMaterial")
    cmds.setAttr(redMaterial+".color", 196/255.0, 40/255.0, 27/255.0, type = 'double3')
    redSet = cmds.sets(redMaterial, empty = True, r = True , noSurfaceShader = True)
    cmds.connectAttr(redMaterial+".color", redSet+".surfaceShader")
    
    darkRedMaterial = cmds.shadingNode('blinn', asShader = True, n = "darkRedMaterial")
    cmds.setAttr(darkRedMaterial+".color", 123/255.0, 46/255.0, 47/255.0, type = 'double3')
    darkRedSet = cmds.sets(darkRedMaterial, empty = True, r = True , noSurfaceShader = True)
    cmds.connectAttr(darkRedMaterial+".color", darkRedSet+".surfaceShader")
    
    yellowMaterial = cmds.shadingNode('blinn', asShader = True, n = "yellowMaterial")
    cmds.setAttr(yellowMaterial+".color", 245/255.0, 205/255.0, 47/255.0, type = 'double3')
    yellowSet = cmds.sets(yellowMaterial, empty = True, r = True , noSurfaceShader = True)
    cmds.connectAttr(yellowMaterial+".color", yellowSet+".surfaceShader")
    
    blueMaterial = cmds.shadingNode('blinn', asShader = True, n = "blueMaterial")
    cmds.setAttr(blueMaterial+".color", 13/255.0, 105/255.0, 171/255.0, type = 'double3')
    blueSet = cmds.sets(blueMaterial, empty = True, r = True , noSurfaceShader = True)
    cmds.connectAttr(blueMaterial+".color", blueSet+".surfaceShader")
    
    greenMaterial = cmds.shadingNode('blinn', asShader = True, n = "greenMaterial")
    cmds.setAttr(greenMaterial+".color", 75/255.0, 151/255.0, 74/255.0, type = 'double3')
    greenSet = cmds.sets(greenMaterial, empty = True, r = True , noSurfaceShader = True)
    cmds.connectAttr(greenMaterial+".color", greenSet+".surfaceShader")

################ Function to create normal square blocks
def createSqBlocks():
    
    #Array to hold bumbShapes
    pipeBumpArray = []
    
    #Get Block Dimensions from GUI
    blockDepthSq = cmds.intSliderGrp('blockDepthSq', query = True, value = True)
    blockWidthSq = cmds.intSliderGrp('blockWidthSq', query = True, value = True)
    blockHeight = cmds.radioButtonGrp('blockHeight', query = True, sl = True)
    
    #Convert to lego sizes
    SqBlock_SizeX = blockWidthSq * 0.8
    SqBlock_SizeZ = blockDepthSq * 0.8
    
    #Set block height according to radio button choice
    if blockHeight == 1:
        SqBlock_SizeY = 0.32
            
    if blockHeight == 2:    
        SqBlock_SizeY = 0.96
    
    cmds.select(clear = True)
    
    #Create Cube Base
    pCube = cmds.polyCube (h = SqBlock_SizeY, w = SqBlock_SizeX, d = SqBlock_SizeZ, sz = blockDepthSq, sy = 2, sx = blockWidthSq )[0]
    
    #move block Above Origin
    cmds.move((SqBlock_SizeY/2.0), moveY = True)
    
    #create bump shapes and add it to array
    for i in range(blockWidthSq):
        for j in range(blockDepthSq):
            pipeBumpArray.append(cmds.polyCylinder(r=0.24, h = 0.18)[0])
            cmds.move((SqBlock_SizeY + 0.10), moveY = True, a = True)
            cmds.move((( i * 0.8) - (SqBlock_SizeX/2.0) + 0.4), moveX = True, a = True)
            cmds.move((( j * 0.8) - (SqBlock_SizeZ/2.0) + 0.4), moveZ = True, a = True)
    
    cmds.select(pCube, r=True)
    
    #Select All Bumps in Array        
    for pipe in pipeBumpArray:
        cmds.select(pipe, add = True)        
    
    #Create Final Shape
    cmds.polyUnite(ch=False)
    cmds.delete(ch=True)
    
    #Set material of object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True))

################ Create Square Blocks with Holes    
def createSqBlocksHoles():
    
    #Create array to hold boolean shapes
    booleanShapeArray = []
    
    #Create array to hold bump shapes
    pipeBumpArray = []
    
    #Get Block Dimensions from GUI
    blockDepthSqH = cmds.intSliderGrp('blockDepthSqH', query = True, value = True)
    
    
    cmds.select(clear = True);
    
    #Convert to lego sizes
    SqBlockHoles_SizeX = 0.8
    SqBlockHoles_SizeZ = blockDepthSqH * 0.8
    SqBlockHoles_SizeY = 0.96
    
     #Create Cube Base
    pCube = cmds.polyCube (h = SqBlockHoles_SizeY, w = SqBlockHoles_SizeX, d = SqBlockHoles_SizeZ, sz =blockDepthSqH, sy = 2 )[0]
    
    #move block Above Origin
    cmds.move((SqBlockHoles_SizeY/2.0), moveY = True)
    
    
    #Create objects to perform boolean difference and store them in array
    for i in range (1,blockDepthSqH):
        
        booleanShapeArray.append(cmds.polyCylinder(r =0.24, h = SqBlockHoles_SizeX)[0])
        cmds.rotate(90, z = True, a = True)
        cmds.move(0.58, moveY = True, a = True)
        cmds.move((( i * 0.8) - (SqBlockHoles_SizeZ/2.0)), moveZ = True)
        
        booleanShapeArray.append(cmds.polyCylinder(r = 0.31, h = 0.10)[0])
        cmds.rotate(90, z = True, a = True)
        cmds.move(0.58, moveY = True, a = True)
        cmds.move((( i * 0.8) - (SqBlockHoles_SizeZ/2.0)), moveZ = True, a = True)
        cmds.move((SqBlockHoles_SizeX/2.0)-0.05, moveX = True, a = True)
        
        booleanShapeArray.append(cmds.polyCylinder(r = 0.31, h = 0.10)[0])
        cmds.rotate(90, z = True, a = True)
        cmds.move(0.58, moveY = True, a = True)
        cmds.move((( i * 0.8) - (SqBlockHoles_SizeZ/2.0)), moveZ = True, a = True)
        cmds.move((-1.0)*(SqBlockHoles_SizeX/2.0)+0.05, moveX = True, a = True)
        
        
    #Select all items to perform boolean difference
    cmds.select(pCube)    
    
    #Iterate through boolean shape array and select objects
    for booleanShape in (booleanShapeArray):
        cmds.select( booleanShape, add=True)
        
    #Perform Boolean Difference
    diff = cmds.polyCBoolOp(op=2, o = True)[0]
    
    #Create bumps and store them in array
    for i in range(1):
        for j in range(blockDepthSqH):
            pipeBumpArray.append(cmds.polyPipe(r=0.24, h = 0.36, t=0.05)[0])
            cmds.move((SqBlockHoles_SizeY + 0.10), moveY = True, a = True)
            cmds.move((( i * 0.8) - (SqBlockHoles_SizeX/2.0) + 0.4), moveX = True, a = True)
            cmds.move((( j * 0.8) - (SqBlockHoles_SizeZ/2.0) + 0.4), moveZ = True, a = True)
    
    #Select Main Shape
    cmds.select(diff)
    
    #Iterate through pipeBumpArray and select pipes        
    for pipe in pipeBumpArray:
        cmds.select(pipe, add = True)        
    
    #create final shape
    cmds.polyUnite(ch=False)
    cmds.delete(ch=True)
    
    #Set material of object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True))
    
    
################ Creat Rounded Block With No Angles using info from GUI   
def createRoundedBlocksNoAngle():    
    #Get Block Dimensions from GUI
    blockDepthR = cmds.intSliderGrp('blockDepthR', query = True, value = True)
    
    #Call function to create beam with the beam's size, and specifying that the beam will not have a cross shape
    a = generalBeamCreation(blockDepthR, False)
    
    #Set material of object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True)) 


################ General Function for Creating Beam Shapes, information containing size of beam and if the beam should include a cross shape at the end are passed to this function
def generalBeamCreation(beamDepth, includeCross):
    #Create array for containing shapes used for boolean operations
    booleanShapeArray = []
    
    #Set variables used for beam creation
    beamDepth = beamDepth
    includeCross = includeCross
    beam_SizeX = 0.8
    beam_SizeZ = (beamDepth - 1) * 0.8
    beam_SizeY = 0.7
    
    #Create Cube Base
    pCube = cmds.polyCube (h = beam_SizeY, w = beam_SizeX, d = beam_SizeZ)[0]
    #move block Above Origin
    cmds.move((beam_SizeY/2.0), moveY = True)
    
    #Create and move cylinders which are used to give beam rounded ends
    pCyl1 = cmds.polyCylinder(r =beam_SizeY/2.0, h = beam_SizeX, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move((-1*(beam_SizeZ/2.0)), moveZ = True)
    
    pCyl2 = cmds.polyCylinder(r =beam_SizeY/2.0, h = beam_SizeX, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move((beam_SizeZ/2.0), moveZ = True)
    
    #Select Cube and 2 Cylinders and perform a union boolean operation to create base shape of beam
    cmds.select(pCube,pCyl1, pCyl2, r = True)
    roundedBlock = cmds.polyCBoolOp( op=1, o = True)[0] 
    
    #Delete History 
    cmds.delete(ch=True)
    
    #If the beam will not include a cross
    if(includeCross == False):
        #Create cylinder shapes which will be used to give holes to base beam shape, then add them to boolean shape array
        for i in range(beamDepth):
            booleanShapeArray.append(cmds.polyCylinder(n = 'p1'+str(i), r =0.24, h = beam_SizeX)[0])
            cmds.rotate(90, z = True, a = True)
            cmds.move((beam_SizeY/2), moveY = True, a = True)
            cmds.move((( i * 0.8) - (beam_SizeZ/2.0)), moveZ = True)
            
            booleanShapeArray.append(cmds.polyCylinder(n = 'p2'+str(i), r = 0.31, h = 0.10)[0])
            cmds.rotate(90, z = True, a = True)
            cmds.move((beam_SizeY/2), moveY = True, a = True)
            cmds.move((( i * 0.8) - (beam_SizeZ/2.0)), moveZ = True)
            cmds.move((beam_SizeX/2.0)-0.05, moveX = True, a = True)
            
            booleanShapeArray.append(cmds.polyCylinder(n = 'p3'+str(i),r = 0.31, h = 0.10)[0])
            cmds.rotate(90, z = True, a = True)
            cmds.move((beam_SizeY/2), moveY = True, a = True)
            cmds.move((( i * 0.8) - (beam_SizeZ/2.0)), moveZ = True)
            cmds.move((-1.0*(beam_SizeX/2.0))+0.05, moveX = True, a = True)
        
        #Create indent shapes for beam detail, then add them to boolean shape array
        for j in range(beamDepth-1):
            a = cmds.polyCube(n = 'c1'+str(j), h = 0.62, d = 0.3, w = 0.10, sy=3)[0]
            cmds.move((beam_SizeY/2.0), moveY = True, a = True)
            cmds.move((( j  * 0.8) - (beam_SizeZ/2.0)+0.4), moveZ = True)
            cmds.move((beam_SizeX/2.0)-0.05, moveX = True, a  = True)
            
            cmds.select( a+".vtx[10:13]")
            cmds.polyMoveVertex(tz=0.12)
            cmds.select(a+".vtx[2:5]")
            cmds.polyMoveVertex(tz=-0.12 )
            booleanShapeArray.append(a)
            
            b = cmds.polyCube(n = 'c2'+str(j), h = 0.62, d = 0.3, w = 0.10, sy=3)[0]
            cmds.move((beam_SizeY/2.0), moveY = True, a = True)
            cmds.move((( j  * 0.8) - (beam_SizeZ/2.0)+0.4), moveZ = True)
            cmds.move((-1.0*(beam_SizeX/2.0))+0.05, moveX = True, a = True)
            
            cmds.select( b + ".vtx[10:13]")
            cmds.polyMoveVertex(tz=0.12 )
            cmds.select( b + ".vtx[2:5]")
            cmds.polyMoveVertex(tz=-0.12 )
            booleanShapeArray.append(b)
        
        #Select the base shape
        cmds.select(roundedBlock, r = True)
        
        #Select all shapes in the boolean shape array
        for shape in booleanShapeArray:
            cmds.select(shape, add = True)
    
    # If the beam will include the cross        
    if(includeCross == True):
        #Create cylinder shapes which will be used to give holes to base beam shape, then add them to boolean shape array
        for i in range(beamDepth -1):
            booleanShapeArray.append(cmds.polyCylinder(n = 'p1'+str(i), r =0.24, h = beam_SizeX)[0])
            cmds.rotate(90, z = True, a = True)
            cmds.move((beam_SizeY/2), moveY = True, a = True)
            cmds.move((( i * 0.8) - (beam_SizeZ/2.0)), moveZ = True)
            
            booleanShapeArray.append(cmds.polyCylinder(n = 'p2'+str(i), r = 0.31, h = 0.10)[0])
            cmds.rotate(90, z = True, a = True)
            cmds.move((beam_SizeY/2), moveY = True, a = True)
            cmds.move((( i * 0.8) - (beam_SizeZ/2.0)), moveZ = True)
            cmds.move((beam_SizeX/2.0)-0.05, moveX = True, a = True)
            
            booleanShapeArray.append(cmds.polyCylinder(n = 'p3'+str(i),r = 0.31, h = 0.10)[0])
            cmds.rotate(90, z = True, a = True)
            cmds.move((beam_SizeY/2), moveY = True, a = True)
            cmds.move((( i * 0.8) - (beam_SizeZ/2.0)), moveZ = True)
            cmds.move((-1.0*(beam_SizeX/2.0))+0.05, moveX = True, a = True)
        
        #Create indent shapes for beam detail, then add them to boolean shape array
        for j in range(beamDepth-2):
            a = cmds.polyCube(n = 'c1'+str(j), h = 0.62, d = 0.3, w = 0.10, sy=3)[0]
            cmds.move((beam_SizeY/2), moveY = True, a = True)
            cmds.move((( j  * 0.8) - (beam_SizeZ/2.0)+0.4), moveZ = True)
            cmds.move((beam_SizeX/2.0)-0.05, moveX = True, a  = True)
            
            cmds.select(a + ".vtx[10:13]")
            cmds.polyMoveVertex(tz=0.12)
            cmds.select( a + ".vtx[2:5]")
            cmds.polyMoveVertex(tz=-0.12 )
            
            booleanShapeArray.append(a)
            
            b = cmds.polyCube(n = 'c2'+str(j), h = 0.62, d = 0.3, w = 0.10, sy=3)[0]
            cmds.move((beam_SizeY/2), moveY = True, a = True)
            cmds.move((( j  * 0.8) - (beam_SizeZ/2.0)+0.4), moveZ = True)
            cmds.move((-1.0*(beam_SizeX/2.0))+0.05, moveX = True, a = True)
            
            cmds.select( b +".vtx[10:13]")
            cmds.polyMoveVertex(tz=0.12 )
            cmds.select( b + ".vtx[2:5]")
            cmds.polyMoveVertex(tz=-0.12 )
            
            booleanShapeArray.append(b)
        
        #Create Cross Boolean Shape
        crossBA = cmds.polyCube (n="crossBA", h = 0.46, w = beam_SizeX*2, d = 0.46/3.0, sy=3)[0]
        cmds.move((beam_SizeY/2), moveY = True, a = True)
        cmds.move((( (beamDepth-1) * 0.8) - (beam_SizeZ/2.0)), moveZ = True)
        cmds.polyExtrudeFacet( crossBA+'.f[1]' , tz = 0.46/3.0) 
        cmds.polyExtrudeFacet( crossBA+'.f[5]' , tz = -2*(0.46/3.0)) 
        
        cmds.select(crossBA+'.e[0:43]', r = True)
        cmds.select(crossBA+'.e[1]', d = True)
        cmds.select(crossBA+'.e[2]', d = True)
        cmds.select(crossBA+'.e[5]', d = True)
        cmds.select(crossBA+'.e[6]', d = True)
        cmds.polyBevel(oaf = True, at = 180, ch=False)
        
        #Add shape to boolean shape array
        booleanShapeArray.append(crossBA)
        
        #Create funky indent shape that goes through whole width of beam
        crossFunkyBA = cmds.polyCube(n = 'crossFunkyBA', h = 0.62, d = 0.3, w = beam_SizeX, sy=3)[0]
        cmds.move((beam_SizeY/2), moveY = True, a = True)
        cmds.move((( (beamDepth-2)  * 0.8) - (beam_SizeZ/2.0)+0.4), moveZ = True)
        cmds.select( crossFunkyBA+".vtx[10:13]")
        cmds.polyMoveVertex(tz=0.12 )
        cmds.select( crossFunkyBA+".vtx[2:5]")
        cmds.polyMoveVertex(tz=-0.12 )
        
        #Add shape to boolean shape array
        booleanShapeArray.append(crossFunkyBA)
        
        #Select base shape    
        cmds.select(roundedBlock, r = True)
        
        #Select all shapes in boolean shape array
        for shape in booleanShapeArray: 
             cmds.select(shape, add = True)
    
    #Perform boolean difference operation     
    beam = cmds.polyCBoolOp(op=2, o = True)[0]  
    
    #Delete history
    cmds.delete(ch=True)
    
    #return Beam
    return(beam)

################ Create rounded beam with an angle between two sections    
def createRoundedBlocksWithAngle(): 
    
    #Get Block Dimensions from GUI for Beam Before Angle
    blockDepthRBA = cmds.intSliderGrp('blockDepthRBA', query = True, value = True)
    
    #Get Block Dimensions from GUI for Beam After Angle
    blockDepthRAA = cmds.intSliderGrp('blockDepthRAA', query = True, value = True)
    
    #Check if use wants beams to have a cross hole
    includeCrossRBA = cmds.checkBox('includeCrossRBA', query = True, value = True)
    includeCrossRAA = cmds.checkBox('includeCrossRAA', query = True, value = True)
    
    #Get Desired Angle
    bendAngleRA = cmds.radioButtonGrp('bendAngleRA', query = True, sl = True)
    
    cmds.select(clear = True);
    
    #Convert dimentions to lego size
    RBlockBAWithAngle_SizeZ = (blockDepthRBA - 1) * 0.8
    RBlockAAWithAngle_SizeZ = (blockDepthRAA - 1) * 0.8
    
    #Set constant height
    RBlockWithAngle_SizeY = 0.7
    
    #Create beams
    BeamBA = generalBeamCreation(blockDepthRBA, includeCrossRBA)
    BeamAA = generalBeamCreation(blockDepthRAA, includeCrossRAA)
    
    #Move pivot of BeamAA to one end of the beam
    cmds.move(0, (RBlockWithAngle_SizeY/2), (-1*(RBlockAAWithAngle_SizeZ/2.0)), BeamAA+".scalePivot",BeamAA+".rotatePivot", absolute=True)           
    #Move pivot position of BeamAA to the end of BeamBA
    cmds.move( (RBlockAAWithAngle_SizeZ/2.0)-(RBlockBAWithAngle_SizeZ/2.0), moveZ = True)
    
    #Rotate beamAA to an angle depending on the users choise of angle
    if (bendAngleRA == 1):
        cmds.rotate(53.1-180, x = True, a = True)
    if (bendAngleRA == 2):
        cmds.rotate(-90, x = True, a = True)
        
    #Add BeamBA to selection
    cmds.select(BeamBA, add = True)
    
    #Combine two beams
    cmds.polyUnite(ch = False)
    cmds.delete(ch=True) 
    
    #Set material of object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True))    


################ Create Multi-Beam Shape
def createMultBeam():
    
    #Create array for booleans shapes of special middle beam (Second beam)
    SBBooleanArray = []
    
    #Get Block Dimensions from GUI for First Beam
    blockDepthFBeam = cmds.intSliderGrp('blockDepthFB', query = True, value = True)
    
    #Get Block Dimensions from GUI for Second Beam
    blockDepthSBeam = cmds.intSliderGrp('blockDepthSB', query = True, value = True)
    
    #Get Block Dimensions from GUI for Third Beam
    blockDepthTBeam = cmds.intSliderGrp('blockDepthTB', query = True, value = True)
    
    #Check if use wants beams to have a cross hole
    includeCrossFBeam = cmds.checkBox('includeCrossFB', query = True, value = True)
    includeCrossTBeam = cmds.checkBox('includeCrossTB', query = True, value = True)
    

    cmds.select(clear = True);
    
    #Convert to Lego Dimensions
    FBeam_SizeZ = (blockDepthFBeam - 1) * 0.8
    SBeam_SizeZ = ((blockDepthSBeam+0.83) - 1) * 0.8
    TBeam_SizeZ = (blockDepthTBeam - 1) * 0.8
    
    beam_SizeY = 0.7
    beam_SizeX = 0.8
    
    #Create Cube Base
    pCube = cmds.polyCube (h = beam_SizeY, w = beam_SizeX, d = SBeam_SizeZ)[0]
    #Move block Above Origin
    cmds.move((beam_SizeY/2.0), moveY = True)
    
    #Create Cylinders for Rounded Ends
    pCyl1 = cmds.polyCylinder(r =beam_SizeY/2.0, h = beam_SizeX, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move((-1*(SBeam_SizeZ/2.0)), moveZ = True)
    
    pCyl2 = cmds.polyCylinder(r =beam_SizeY/2.0, h = beam_SizeX, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move((SBeam_SizeZ/2.0), moveZ = True)
    
    #Select shapes and perform boolean union
    cmds.select(pCube,pCyl1, pCyl2, r = True)
    roundedBlockSBeam = cmds.polyCBoolOp( op=1, o = True)[0] 
     
    cmds.delete(ch=True)
    
    #Create Hole Booleans, then add them to boolean array
    SBBooleanArray.append(cmds.polyCylinder( r =0.24, h = beam_SizeX)[0])
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2), moveY = True, a = True)
    cmds.move((-(SBeam_SizeZ/2.0)), moveZ = True)
    
    SBBooleanArray.append(cmds.polyCylinder(r = 0.31, h = 0.10)[0])
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2), moveY = True, a = True)
    cmds.move((-(SBeam_SizeZ/2.0)), moveZ = True)
    cmds.move((beam_SizeX/2.0)-0.05, moveX = True, a = True)
    
    SBBooleanArray.append(cmds.polyCylinder(r = 0.31, h = 0.10)[0])
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2), moveY = True, a = True)
    cmds.move((-(SBeam_SizeZ/2.0)), moveZ = True)
    cmds.move((-1.0*(beam_SizeX/2.0))+0.05, moveX = True, a = True)
    
    SBBooleanArray.append(cmds.polyCylinder(r =0.24, h = beam_SizeX)[0])
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2), moveY = True, a = True)
    cmds.move((SBeam_SizeZ/2.0), moveZ = True)
    
    SBBooleanArray.append(cmds.polyCylinder( r = 0.31, h = 0.10)[0])
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2), moveY = True, a = True)
    cmds.move((SBeam_SizeZ/2.0), moveZ = True)
    cmds.move((beam_SizeX/2.0)-0.05, moveX = True, a = True)
    
    SBBooleanArray.append(cmds.polyCylinder(r = 0.31, h = 0.10)[0])
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2), moveY = True, a = True)
    cmds.move((SBeam_SizeZ/2.0), moveZ = True)
    cmds.move((-1.0*(beam_SizeX/2.0))+0.05, moveX = True, a = True)

    
    #Create Funky Shape Booleans, then add them to boolean array
    fs1 = cmds.polyCube( h = 0.62, d = 0.3, w = 0.10, sy=3)[0]
    cmds.move((beam_SizeY/2.0), moveY = True, a = True)
    cmds.move(( (SBeam_SizeZ/2.0)-0.425), moveZ = True)
    cmds.move((beam_SizeX/2.0)-0.05, moveX = True, a  = True)
    
    cmds.select( fs1+".vtx[10:13]")
    cmds.polyMoveVertex(tz=0.12)
    cmds.select(fs1+".vtx[2:5]")
    cmds.polyMoveVertex(tz=-0.12 )
    SBBooleanArray.append(fs1)
    
    fs2 = cmds.polyCube( h = 0.62, d = 0.3, w = 0.10, sy=3)[0]
    cmds.move((beam_SizeY/2.0), moveY = True, a = True)
    cmds.move(((SBeam_SizeZ/2.0)-0.425), moveZ = True)
    cmds.move((-1.0*(beam_SizeX/2.0))+0.05, moveX = True, a = True)
    
    cmds.select( fs2 + ".vtx[10:13]")
    cmds.polyMoveVertex(tz=0.12 )
    cmds.select( fs2 + ".vtx[2:5]")
    cmds.polyMoveVertex(tz=-0.12 )
    SBBooleanArray.append(fs2)
    
    fs3 = cmds.polyCube( h = 0.62, d = 0.3, w = 0.10, sy=3)[0]
    cmds.move((beam_SizeY/2.0), moveY = True, a = True)
    cmds.move((-(SBeam_SizeZ/2.0)+0.425), moveZ = True)
    cmds.move((beam_SizeX/2.0)-0.05, moveX = True, a  = True)
    
    cmds.select( fs3 + ".vtx[10:13]")
    cmds.polyMoveVertex(tz=0.12)
    cmds.select(fs3 + ".vtx[2:5]")
    cmds.polyMoveVertex(tz=-0.12 )
    SBBooleanArray.append(fs3)
    
    fs4 = cmds.polyCube( h = 0.62, d = 0.3, w = 0.10, sy=3)[0]
    cmds.move((beam_SizeY/2.0), moveY = True, a = True)
    cmds.move((-(SBeam_SizeZ/2.0)+0.425), moveZ = True)
    cmds.move((-1.0*(beam_SizeX/2.0))+0.05, moveX = True, a = True)
    
    cmds.select( fs4 + ".vtx[10:13]")
    cmds.polyMoveVertex(tz=0.12 )
    cmds.select( fs4 + ".vtx[2:5]")
    cmds.polyMoveVertex(tz=-0.12 )
    SBBooleanArray.append(fs4)
    
    
#Create Middle Shape Booleans
    #Create Cube Base for main hole
    p1Cube = cmds.polyCube (h = 0.48, w = beam_SizeX, d = SBeam_SizeZ - 1.6)[0]
    #move block Above Origin
    cmds.move((beam_SizeY/2.0), moveY = True)
    
    #Create Cylinders for Rounded Ends
    p1Cyl1 = cmds.polyCylinder(r =0.24, h = beam_SizeX, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move((-1*((SBeam_SizeZ-1.6)/2.0)), moveZ = True)
    
    p1Cyl2 = cmds.polyCylinder(r =0.24, h = beam_SizeX, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move(((SBeam_SizeZ-1.6)/2.0), moveZ = True)
    
    #Select shapes and perform boolean union, then add the result to the Second Beam boolean array
    cmds.select(p1Cube,p1Cyl1, p1Cyl2, r = True)
    SBBooleanArray.append(cmds.polyCBoolOp( op=1, o = True)[0]) 
    cmds.delete(ch=True)  
    
    #Create Cube Base for imprint 1
    p2Cube = cmds.polyCube (h = 0.61, w = 0.10, d = SBeam_SizeZ - 1.6)[0]
    #move block Above Origin
    cmds.move((beam_SizeY/2.0), moveY = True)
    
    #Create Cylinders for Rounded Ends
    p2Cyl1 = cmds.polyCylinder(r =0.31, h = 0.10, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move((-1*((SBeam_SizeZ - 1.6)/2.0)), moveZ = True)
    
    p2Cyl2 = cmds.polyCylinder(r =0.31, h = 0.10, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move(((SBeam_SizeZ - 1.6)/2.0), moveZ = True)
    
    #Select shapes and perform boolean union, then add the result to the Second Beam boolean array
    cmds.select(p2Cube,p2Cyl1, p2Cyl2, r = True)
    SBBooleanArray.append(cmds.polyCBoolOp( op=1, o = True)[0]) 
    cmds.move((-1.0*(beam_SizeX/2.0))+0.05, moveX = True, a = True)
    cmds.delete(ch=True)  
   
    #Create Cube Base for imprint 2
    p3Cube = cmds.polyCube (h = 0.61, w = 0.10, d = SBeam_SizeZ - 1.6)[0]
    
    #move block Above Origin
    cmds.move((beam_SizeY/2.0), moveY = True)
    
    #Create Cylinders for Rounded Ends
    p3Cyl1 = cmds.polyCylinder(r =0.31, h = 0.10, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move((-1*((SBeam_SizeZ - 1.6)/2.0)), moveZ = True)
    
    p3Cyl2 = cmds.polyCylinder(r =0.31, h = 0.10, sz=1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.move((beam_SizeY/2.0), moveY = True)
    cmds.move(((SBeam_SizeZ - 1.6)/2.0), moveZ = True)
    
    #Select shapes and perform boolean union, then add the result to the Second Beam boolean array
    cmds.select(p3Cube,p3Cyl1, p3Cyl2, r = True)
    SBBooleanArray.append(cmds.polyCBoolOp( op=1, o = True)[0]) 
    cmds.move(((beam_SizeX/2.0))-0.05, moveX = True, a = True)
    cmds.delete(ch=True)  
    
    #Select middle beam base shape
    cmds.select(roundedBlockSBeam, r =True)
    
    #Select all shapes in boolean shape array
    for shape in SBBooleanArray:
        cmds.select(shape, add = True)
    
    #Perform boolean difference on select objects    
    BeamSB = cmds.polyCBoolOp(op=2, o = True)[0]  
    
    #Create first beam and third beam
    BeamFB = generalBeamCreation(blockDepthFBeam, includeCrossFBeam)
    BeamTB = generalBeamCreation(blockDepthTBeam, includeCrossTBeam)

    #Select third beam    
    cmds.select(BeamTB, r = True)
    
    #Move thrid beam to correct position
    cmds.move(((SBeam_SizeZ+TBeam_SizeZ)/2), moveZ = True, r = True)
    
    #Rotate third beam around correct pivot point by 45 degrees
    cmds.rotate(-45, x = True, a = True, p = (0, (beam_SizeY/2), ((SBeam_SizeZ)/2)))
    
    #Select Third and Second beam and Combine them
    cmds.select(BeamTB, BeamSB, r = True)
    BeamsSBTB = cmds.polyUnite(ch=False)[0]
    
    #Select combined Third and Second beam and move it to correct positoin
    cmds.select(BeamsSBTB, r = True)
    cmds.move(((FBeam_SizeZ+SBeam_SizeZ)/2), moveZ = True, r = True)
    #Rotate combined beam around correct pivot point by 45 degrees
    cmds.rotate(-45, x= True, a = True, p = (0, (beam_SizeY/2), ((FBeam_SizeZ)/2)))
    
    #Scale First Beam so that cross shape is facing correct direction
    cmds.scale(-1, BeamFB, z = True)
    
    #Select all beam components
    cmds.select(BeamsSBTB, BeamFB, r = True)
    
    #Combine beam components
    cmds.polyUnite(ch=False)
    
    #Set material of object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True))
    
################ Create Tire and Hub
def createTireAndHub():
    
    #Get Tire Dimensions from GUI
    tireRad = cmds.intSliderGrp('tireRad', query = True, value = True)
    tireWidth = cmds.intSliderGrp('tireWidth', query = True, value = True)
    
    #Get Hub Radius from GUI
    hubRad = cmds.intSliderGrp('hubRad', query = True, value = True)
    
    #Convert values to lego dimensions
    tireShape_Rad = ((tireRad * 1.05) *2.67)*0.75
    tireShape_Width = ((tireWidth * 1.2) * 2.67)*0.75
    
    #Make sure hub is not bigger than tire
    if hubRad <= tireRad:
        hubShape_Rad = hubRad * 1.6 * 0.75
    if hubRad > tireRad:
        hubShape_Rad = tireRad * 1.6 * 0.75
        cmds.warning("Hub Radius changed to fit inside tire")
    
    #Set hub width to equal tire width    
    hubShape_Width = tireShape_Width
    
    #Set tire thickness
    tireShape_Thickness = (tireShape_Rad - hubShape_Rad)
    
    cmds.select(clear = True);
    
    #Create basic tire shape
    tirePipe = cmds.polyPipe( h = tireShape_Width, r = tireShape_Rad,sh = 3, t = tireShape_Thickness, sa = 40)[0]
    
    #Move edge loops on pipe to desired position
    cmds.select(tirePipe+".e[200:239]")  
    cmds.select( tirePipe+".e[240:279]", add = True)
    cmds.polyMoveEdge(sy = 0.5)
    
    cmds.select(clear=True)
    
    #Select alternating tire faces for treads
    for i in range(160,200):
        if (i%2 == 0):
            cmds.select( tirePipe+".f["+str(i)+"]", add = True) 
    for j in range(240,280):
        if (j%2 == 1):
            cmds.select( tirePipe+".f["+str(j)+"]", add = True)  
    
    #Selecting middle facet ring        
    cmds.select( tirePipe+".f[200:239]", add = True) 
    
    #Extrude faces outward by a value related to the tire's width
    cmds.polyExtrudeFacet(lt = [0,0,tireShape_Width/4.0])  
    
    #Select tire shape and move it above origin
    cmds.select(tirePipe)
    cmds.move((tireShape_Width/4), moveY = True, a = True)
    
    #Set material of object to predetermined material
    cmds.hyperShade(assign = "matteBlackMaterial") 
    
    #Create shapes to make up hub base shape
    hubOuterPipe = cmds.polyPipe( h = hubShape_Width, r = hubShape_Rad,sh = 3, t = 0.1, sa = 40)[0]
    hubMainCylinder = cmds.polyCylinder(h = (hubShape_Width/2.0)*0.66, r = hubShape_Rad - 0.1, sz=1, sx = 40)[0]
    
    #Create cylinders to be used for boolean shapes
    c1 = cmds.polyCylinder(r =0.25, h = (hubShape_Width/2.0)*0.66)[0]
    
    #Create a pair of boolean shapes
    c2 = cmds.polyCylinder(r =0.25, h = (hubShape_Width/2.0)*0.66)[0]
    cmds.move((hubShape_Rad/2.0), moveX =True, a = True)
    
    c3 = cmds.polyCylinder(r =0.25, h = (hubShape_Width/2.0)*0.66)[0]
    cmds.move(-(hubShape_Rad/2.0), moveX =True, a = True)
    
    #Select and combine pair of boolean shapes, and then rotate them into correct position
    cmds.select(c2, add = True)
    cp1 = cmds.polyUnite(ch=False)[0]
    cmds.delete(ch = True)
    
    cp2 = cmds.duplicate()[0]
    cmds.rotate(60, y = True, a=True)
    
    cp3 = cmds.duplicate()[0]
    cmds.rotate(120, y = True, a=True)
    
    cmds.select(hubMainCylinder)
    cmds.select(c1, add = True)
    cmds.select(cp1, add = True)
    cmds.select(cp2, add = True)
    cmds.select(cp3, add = True)
    
    #Perform boolean operation, difference, and set it to variable
    holeyCylinder = cmds.polyCBoolOp(op=2, o = True)[0] 
    
    #Create pipes to be used for hub geometry
    p1 = cmds.polyPipe(h = (hubShape_Width*0.66)+0.25, r = 0.35, t = 0.1, sa = 20)[0]
    
    #Create a pair of pipe shapes
    p2 = cmds.polyPipe(h = (hubShape_Width*0.66)+0.25, r = 0.35, t = 0.1, sa = 20)[0]
    cmds.move((hubShape_Rad/2.0), moveX =True, a = True)
    
    p3 = cmds.polyPipe( h = (hubShape_Width*0.66)+0.25, r = 0.35, t = 0.1, sa = 20)[0]
    cmds.move(-(hubShape_Rad/2.0), moveX =True, a = True)
    
    #Select and combine pair of pipe shapes, and then rotate them into correct position
    cmds.select(p2, add = True)
    pp1 = cmds.polyUnite(ch=False)[0]
    cmds.delete(ch = True)
    
    pp2 = cmds.duplicate()[0]
    cmds.rotate(60, y = True, a=True)
    
    pp3 = cmds.duplicate()[0]
    cmds.rotate(120, y = True, a=True)
    
    cmds.select(holeyCylinder, r =True)
    cmds.select(hubOuterPipe, add = True)
    cmds.select(p1, add=True)
    cmds.select(pp1, add = True)
    cmds.select(pp2, add = True)
    cmds.select(pp3, add = True)
    
    # Combine pipes, and other hub shapes
    hub = cmds.polyUnite(ch=False)[0]
    cmds.delete(ch=True)
    
    #Move shape above origin
    cmds.move(hubShape_Width/4.0, moveY = True, a = True)
    
    #Set material of object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True))
    
    #Put tire and hub in a group node
    cmds.group(tirePipe, hub)

################ Create cross axel shape    
def createAxel():
    
    #Retrieve dimensions of axel from GUI
    axelLength = cmds.intSliderGrp('axelLength', query = True, value = True)
    
    #Set to lego dimensions
    axel_SizeX = axelLength * 0.8
    
    #Create cube based on dimensions
    axelShape = cmds.polyCube ( h = 0.46, w = axel_SizeX, d = 0.46/3.0, sy=3)[0]
    
    #Move object above origin
    cmds.move((0.48/2), moveY = True, a = True)
    
    #Extrude 2 faces to create cross shape
    cmds.polyExtrudeFacet( axelShape+'.f[1]' , tz = 0.46/3.0) 
    cmds.polyExtrudeFacet( axelShape+'.f[5]' , tz = -1*(0.46/3.0))
    
    #Bevel edges of axel to round out shape, corners of cross are not selected
    cmds.select(axelShape+'.e[0:43]', r = True)
    cmds.select(axelShape+'.e[1]', d = True)
    cmds.select(axelShape+'.e[2]', d = True)
    cmds.select(axelShape+'.e[5]', d = True)
    cmds.select(axelShape+'.e[6]', d = True)
    cmds.polyBevel(oaf = True, at = 180, ch=False)
    
    #If the axel length is 2, add details
    if axelLength == 2:
        #Create pipes used for boolean operation
        p1 = cmds.polyPipe(r=0.32, t = 0.16, h = 0.2, sa = 16)[0]
        cmds.rotate(90, x = True, a = True)
        cmds.rotate(90, y = True, a = True)
        cmds.move((0.4), moveX = True, a = True)
        cmds.move((0.48/2), moveY = True, a = True)
        
        p2 = cmds.polyPipe(r=0.32, t = 0.16, h = 0.2, sa = 16)[0]
        cmds.rotate(90, x = True, a = True)
        cmds.rotate(90, y = True, a = True)
        cmds.move(-(0.4), moveX = True, a = True)
        cmds.move((0.48/2), moveY = True, a = True)
        
        cmds.select(axelShape, r = True)
        cmds.select(p1, add = True)
        cmds.select(p2, add = True)
        
        #Perform boolean difference
        axelShape = (cmds.polyCBoolOp(op=2, o = True))[0]
    
    cmds.select(axelShape, r = True)    
    #Set material of object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True))

################ Create Axel Extention Shape     
def createExtension():
    
    #Get length of axel from GUI
    extLength = cmds.intSliderGrp('extLength', query = True, value = True)
    
    #Convert to lego dimensions
    extLength_H = extLength * 0.8
    
    #Create cylinder used as base shape of extension
    a = cmds.polyCylinder(r=0.325, h = extLength_H, sx = 8, sy = 15, sz =1)[0]
    cmds.select(clear = True)
    
    #Select every other face column of the cylinder
    for i in range(15):
        cmds.select(a+".f["+str((i*8)+7)+"]", add = True)
        cmds.select(a+".f["+str((i*8)+1)+"]", add = True)
        cmds.select(a+".f["+str((i*8)+3)+"]", add = True)
        cmds.select(a+".f["+str((i*8)+5)+"]", add = True)

    #Extrude faces to create extension shape    
    cmds.polyExtrudeFacet(lt = [0,0,0.05])
    
    #Select faces and peform extrude to create peice details
    cmds.select(a+".f[93]", a+".f[61]", a+".f[29]", a+".f[95]", a+".f[63]", a+".f[31]", a+".f[89]", a+".f[57]", a+".f[25]", a+".f[91]", a+".f[59]", a+".f[27]", r = True)    
    cmds.polyExtrudeFacet(lt = [0,0,0.04])    
    
    #Bevel shape to make edges less sharp
    cmds.select(a, r = True)
    cmds.polyBevel(oaf = True, at = 180, ch=False) 
    
    #Rotate shape so that it is in proper position for boolean operation
    cmds.rotate((45/2), y = True, a = True)
    
    #Create axel shape for boolean operation
    axelShape = cmds.polyCube ( h = 0.46, w = 10, d = 0.46/3.0, sy=3)[0]
    cmds.move((0.48/2), moveY = True, a = True)
    cmds.polyExtrudeFacet( axelShape+'.f[1]' , tz = 0.46/3.0) 
    cmds.polyExtrudeFacet( axelShape+'.f[5]' , tz = -1*(0.46/3.0))
    cmds.select(axelShape+'.e[0:43]', r = True)
    cmds.select(axelShape+'.e[1]', d = True)
    cmds.select(axelShape+'.e[2]', d = True)
    cmds.select(axelShape+'.e[5]', d = True)
    cmds.select(axelShape+'.e[6]', d = True)
    cmds.polyBevel(oaf = True, at = 180)
    
    #Position axel shape for boolean operation
    cmds.select(axelShape, r = True)
    cmds.rotate(90, z = True, a = True)
    
    cmds.select(a, r = True)
    cmds.select(axelShape, add = True)
    
    #Perform boolean difference operation
    cmds.polyCBoolOp(op=2, o = True, ch=False)
    cmds.delete(ch = True)
    
    #Set Material of Object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True))
    
    #Move object above origin
    cmds.move(0.8, moveY = True, a = True)

################ Create Single Connector Shape
def createSConnector():
    
    #Create bottom shape of connector, then move it above origin
    b = cmds.polyCylinder(r=0.355, h = 0.1, sx = 8, sz =1)[0]    
    cmds.move(0.1/2.0, moveY = True, a = True)
    
    #Select faces and extrube faces to create details, then bevel to soften edges
    cmds.select(b+".f[4]", b+".f[0]", b+".f[6]", b+".f[2]", r = True)
    cmds.polyExtrudeFacet(lt = [0,0,0.05])
    cmds.select(b, r = True)
    cmds.polyBevel(oaf = True, at = 180, ch=False) 
    
    #Create main cylinder shape of connector, then move it above origin
    m = cmds.polyCylinder(r = 0.31, h = 0.8, sz = 1)[0]
    cmds.move(0.8/2.0, moveY = True, a = True)
    
    #Create top cylinder shape of connector, then move it above main cylinder shape
    t = cmds.polyCylinder(r=0.36, h = 0.1, sz =1)[0] 
    cmds.move(0.8-0.05, moveY = True, a = True)
    
    #Select objects and perform union boolean operation
    cmds.select(b,m,t, r = True)
    c = cmds.polyCBoolOp(op=1, o = True, ch=False)[0]
    
    #Rotate shape to perpare for boolean difference
    cmds.rotate(45/2.0, y = True, a = True)
    
    #Create axel shape to be used for boolean difference operation
    axelShape = cmds.polyCube ( h = 0.46, w = 10, d = 0.46/3.0, sy=3)[0]
    cmds.move((0.48/2), moveY = True, a = True)
    cmds.polyExtrudeFacet( axelShape+'.f[1]' , tz = 0.46/3.0) 
    cmds.polyExtrudeFacet( axelShape+'.f[5]' , tz = -1*(0.46/3.0))
    cmds.select(axelShape+'.e[0:43]', r = True)
    cmds.select(axelShape+'.e[1]', d = True)
    cmds.select(axelShape+'.e[2]', d = True)
    cmds.select(axelShape+'.e[5]', d = True)
    cmds.select(axelShape+'.e[6]', d = True)
    cmds.polyBevel(oaf = True, at = 180)
    
    #Position axel shape to perpare for boolean difference operation
    cmds.select(axelShape, r = True)
    cmds.rotate(90, z = True, a = True)
    
    #select shapes
    cmds.select(c, r = True)
    cmds.select(axelShape, add = True)
    
    #Perform difference boolean operation
    cmds.polyCBoolOp(op=2, o = True, ch=False)
    cmds.delete(ch = True)
    
    #Set Material of Object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True))


################ Create Angle Connector Shape
def createAConnectorShape():
    
    #Create base shape for round part of connector
    fC = cmds.polyCylinder(r = 0.35, h = 0.8, sz = 1)[0]
    
    #Create boolean shape
    b1=(cmds.polyCylinder( r =0.24, h = 0.8)[0])
    
    b2 = (cmds.polyCylinder(r = 0.31, h = 0.10)[0])
    cmds.move(0.35, moveY = True, a = True)
    
    b3 =(cmds.polyCylinder(r = 0.31, h = 0.10)[0])
    cmds.move(-0.35, moveY = True, a = True)
    
    #Create and position shape that axel will be inserted into
    a = cmds.polyCylinder(r=0.325, h = 1.29, sx = 8, sy = 15, sz =1)[0]
    cmds.rotate(90, z = True, a = True)
    cmds.rotate((45/2)+45, y = True, a = True)
    cmds.select(clear = True)
    
    #Select every other column of faces of shape
    for i in range(15):
        cmds.select(a+".f["+str((i*8)+7)+"]", add = True)
        cmds.select(a+".f["+str((i*8)+1)+"]", add = True)
        cmds.select(a+".f["+str((i*8)+3)+"]", add = True)
        cmds.select(a+".f["+str((i*8)+5)+"]", add = True)

    #Extrude faces    
    cmds.polyExtrudeFacet(lt = [0,0,0.05])
    
    #Bevel shape to soften edges
    cmds.select(a, r = True)
    cmds.polyBevel(oaf = True, at = 180)
    cmds.move(1.29/2, moveX = True, a = True)
    
    #Create axel shape to be used for boolean difference
    axelShape = cmds.polyCube ( h = 0.46, w = 10, d = 0.46/3.0, sy=3)[0]
    cmds.polyExtrudeFacet( axelShape+'.f[1]' , tz = 0.46/3.0) 
    cmds.polyExtrudeFacet( axelShape+'.f[5]' , tz = -1*(0.46/3.0))
    cmds.select(axelShape+'.e[0:43]', r = True)
    cmds.select(axelShape+'.e[1]', d = True)
    cmds.select(axelShape+'.e[2]', d = True)
    cmds.select(axelShape+'.e[5]', d = True)
    cmds.select(axelShape+'.e[6]', d = True)
    cmds.polyBevel(oaf = True, at = 180)
    
    #Perform boolean difference to create long component of shape
    cmds.select(a, r = True)
    cmds.select(axelShape, add = True)
    tube  = cmds.polyCBoolOp(op = 2, o = True, ch = False)[0]
    
    #Perform boolean union on components
    cmds.select(tube, fC, r = True)
    piece =  cmds.polyCBoolOp(op = 1, o = True, ch = False)[0]
    
    #Select main peice of connector, and boolean shapes, and perform boolean difference
    cmds.select(piece, r = True)
    cmds.select(b1, b2, b3, add = True)
    wholePiece =  cmds.polyCBoolOp(op = 2, o = True, ch = False)[0]
    
    #Set Material of Object
    cmds.hyperShade(assign = cmds.optionMenu('colourChoice', query = True, value = True))
    
    #Recturn connector piece
    return wholePiece

################ Manage Angle Connector Shape Creation    
def createAConnector():   
    
    #Get angle between two connector components from GUI
    cAngle = cmds.intSliderGrp('cAngle', query = True, value = True)
    
    #Check if user wants to create a single angle connector
    isSingle = cmds.checkBox('single', query = True, value = True)
    
    #Create first angle connector shape
    piece1 = createAConnectorShape()
    
    #If user does not want to create a single angle connector
    if (isSingle == False):
        #Create second angle connector shape
        piece2 = createAConnectorShape()
        cmds.select(piece2, r = True)
        
        #Rotate peice 2 to specified angle
        cmds.rotate(cAngle, y = True, a = True, p = (0, 0,0))
        cmds.select(piece1, add = True)
        
        #Perform boolean union on the two angle connector peices
        cmds.polyCBoolOp(op = 1, o = True, ch = False)
        
    
    
#Check if UI has already been created    
if "GUIWindow" in globals():
    if cmds.window( GUIWindow, exists = True ):     #Check if UI Window is open
        cmds.deleteUI( GUIWindow, window = True )    #Delete UI Window if one is open already

#if not, create materials
else:
    createMaterials()

#GUI Specifications
GUIWindow = cmds.window(title="Too Technical GUI", menuBar=True, width = 420, height = 600)

cmds.menu(label = "Basic Options")
#When a new scene is created, recreate materials
cmds.menuItem (label = "New Scene", command = ('cmds.file(new=True, force=True), createMaterials()'))
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'))
#Use to create materials
cmds.menuItem(label="Create Materials", command=('createMaterials()'))

cmds.columnLayout()

#Section for Colour Choice
cmds.frameLayout(collapsable=True, label="Colour")
cmds.optionMenu('colourChoice', label = "Choose Colour", width = 420)
cmds.menuItem (label = "blackMaterial")
cmds.menuItem (label = "whiteMaterial")
cmds.menuItem (label = "greyMaterial")
cmds.menuItem (label = "darkGreyMaterial")
cmds.menuItem (label = "redMaterial")
cmds.menuItem (label = "darkRedMaterial")
cmds.menuItem (label = "yellowMaterial")
cmds.menuItem (label = "blueMaterial")
cmds.menuItem (label = "greenMaterial")
cmds.setParent('..')
cmds.setParent('..')

#Create scrollbar for GUI, Colour Choice section is not affected
cmds.scrollLayout(verticalScrollBarThickness=16)

#Section for square blocks without holes
cmds.frameLayout(collapsable=True, label="Square Blocks without Holes")
cmds.columnLayout()
cmds.intSliderGrp('blockDepthSq', label = "Block Depth", field = True, min = 2, max = 20, value = 2)
cmds.intSliderGrp('blockWidthSq', label = "Block Width", field = True, min = 2, max = 20, value = 2)
cmds.radioButtonGrp( 'blockHeight', label='Bend Height', labelArray2=['Flat', 'Normal'], numberOfRadioButtons=2, select = 1 )
cmds.button(label = "Create Block", command="createSqBlocks()" )
cmds.setParent('..')
cmds.setParent('..')

#Section for square blocks with holes
cmds.frameLayout(collapsable=True, label="Square Blocks with Holes")
cmds.columnLayout()
cmds.intSliderGrp('blockDepthSqH', label = "Block Depth", field = True, min = 2, max = 20, value = 2)
cmds.button(label = "Create Block", command = 'createSqBlocksHoles()')
cmds.setParent('..')
cmds.setParent('..')

#Section for round beams with holes
cmds.frameLayout(collapsable=True, label="Rounded Blocks with Holes")
cmds.columnLayout()
cmds.intSliderGrp('blockDepthR', label = "Block Length", field = True, min = 2, max = 20, value = 2)
cmds.button(label = "Create Block", command = 'createRoundedBlocksNoAngle()')
cmds.setParent('..')
cmds.setParent('..')

#Section for round beams with holes and an angle between them
cmds.frameLayout(collapsable=True, label="Rounded Blocks with Holes and Angle")
cmds.columnLayout()
cmds.iconTextStaticLabel( st='textOnly', l='Dimensions of Beam Before Angle' )
cmds.intSliderGrp('blockDepthRBA', label = "Block Depth", field = True, min = 2, max = 20, value = 2)
cmds.checkBox('includeCrossRBA', label='Include Cross Hole', value = False )

cmds.iconTextStaticLabel( st='textOnly', l='Dimensions of Beam After Angle' )
cmds.intSliderGrp('blockDepthRAA', label = "Block Depth", field = True, min = 2, max = 20, value = 2)
cmds.checkBox('includeCrossRAA', label='Include Cross Hole', value = False )

cmds.radioButtonGrp( 'bendAngleRA', label='Bend Angle', labelArray2=['53.1', '90'], numberOfRadioButtons=2, select = 1 )
cmds.button(label = "Create Block", command = "createRoundedBlocksWithAngle()")
cmds.setParent('..')
cmds.setParent('..')

#Section for Tire and Hub
cmds.frameLayout(collapsable=True, label="Tire and Hub")
cmds.columnLayout()
cmds.intSliderGrp('tireRad', label = "Tire Radius", field = True, min = 1, max = 8, value = 1)
cmds.intSliderGrp('tireWidth', label = "Tire Width", field = True, min = 1, max = 8, value = 1)
cmds.intSliderGrp('hubRad', label = "Hub Radius", field = True, min = 1, max = 8, value = 1)
cmds.button(label = "Create Tire and Hub", command = "createTireAndHub()")
cmds.setParent('..')
cmds.setParent('..')

#Section for multi-angle beam
cmds.frameLayout(collapsable = True, label = "Multi-Angle Beam")
cmds.columnLayout()
cmds.iconTextStaticLabel( st='textOnly', l='Dimensions of First Beam' )
cmds.intSliderGrp('blockDepthFB', label = "Block Depth", field = True, min = 2, max = 20, value = 7)
cmds.checkBox('includeCrossFB', label='Include Cross Hole', value = False )

cmds.iconTextStaticLabel( st='textOnly', l='Dimensions of Second Beam' )
cmds.intSliderGrp('blockDepthSB', label = "Block Depth", field = True, min = 3, max = 10, value = 3)

cmds.iconTextStaticLabel( st='textOnly', l='Dimensions of Third Beam' )
cmds.intSliderGrp('blockDepthTB', label = "Block Depth", field = True, min = 2, max = 20, value = 3)
cmds.checkBox('includeCrossTB', label='Include Cross Hole', value = False )
cmds.button (label = "Create Multi-Angle Beam", command = "createMultBeam()");
cmds.setParent('..')
cmds.setParent('..')

#Section for Axel
cmds.frameLayout(collapsable = True, label = "Axel")
cmds.columnLayout()
cmds.intSliderGrp('axelLength', label = "Axel Length", field = True, min = 2, max = 20, value = 1)
cmds.button (label = "Create Axel", command = "createAxel()");
cmds.intSliderGrp('extLength', label = "Extension Length", field = True, min = 1, max = 20, value = 2)
cmds.button (label = "Create Extension", command = "createExtension()");
cmds.setParent('..')
cmds.setParent('..')

#Section for Toggle and Connectors
cmds.frameLayout(collapsable = True, label = "Toggle + Connector")
cmds.columnLayout()
cmds.button (label = "Create Single Connector", command = "createSConnector()");
cmds.intSliderGrp('cAngle', label = "Connector Angle", field = True, min = 90, max = 180, value = 90)
cmds.checkBox('single', label='Make Single Connector', value = False )
cmds.button (label = "Create Angle Connector", command = "createAConnector()");
cmds.setParent('..')

#Show window when script is run
cmds.showWindow(GUIWindow)

