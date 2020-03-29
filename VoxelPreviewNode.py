import sys

# Imports to use the Maya Python API
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# Import the Python wrappers for MEL commands
import maya.cmds as cmds

# Import MEL commands
import maya.mel as mel

# Useful functions for declaring attributes as inputs or outputs.
def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)
def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)

# Define the name of the node
kPluginNodeTypeName = "voxelPreviewNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
voxelPreviewNodeID = OpenMaya.MTypeId(0x8205)

# Node definition
class voxelPreviewNode(OpenMayaMPx.MPxNode):
    # Declare the input and output class variables
    inXOffset = OpenMaya.MObject()
    inYOffset = OpenMaya.MObject()
    inZOffset = OpenMaya.MObject()
    inVoxelSize = OpenMaya.MObject()
    inXKnifeCount = OpenMaya.MObject()
    inYKnifeCount = OpenMaya.MObject()
    inZKnifeCount = OpenMaya.MObject()

    outFrame = OpenMaya.MObject()

    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self, plug, data):
        if plug == voxelPreviewNode.outFrame:
            xo = data.inputValue(voxelPreviewNode.inXOffset).asFloat()
            yo = data.inputValue(voxelPreviewNode.inYOffset).asFloat()
            zo = data.inputValue(voxelPreviewNode.inZOffset).asFloat()
            voxelSize = data.inputValue(voxelPreviewNode.inVoxelSize).asFloat()
            xKnifeCount = data.inputValue(voxelPreviewNode.inXKnifeCount).asInt()
            yKnifeCount = data.inputValue(voxelPreviewNode.inYKnifeCount).asInt()
            zKnifeCount = data.inputValue(voxelPreviewNode.inZKnifeCount).asInt()
            knifeSize = 16.0
            knifeHalf = knifeSize / 2

            # Create a mesh data container, which will store our voxelizer frame
            meshDataFn = OpenMaya.MFnMeshData()
            newOutputMeshData = meshDataFn.create()

            # Compute the frame
            numFaces = xKnifeCount + yKnifeCount + zKnifeCount
            numVertices = 4 * numFaces
            numFaceConnects = numVertices

            points = OpenMaya.MFloatPointArray()
            points.setLength(numVertices)
            faceConnects = OpenMaya.MIntArray()
            faceConnects.setLength(numFaceConnects)
            faceCounts = OpenMaya.MIntArray()
            faceCounts.setLength(numFaces)


            pointIndex = 0
            faceCountIndex = 0

            # Compute knife frame in YZ plane
            base = -voxelSize * (xKnifeCount - 1) / 2.0
            position_0 = [base, -knifeHalf, -knifeHalf]
            position_1 = [base, -knifeHalf, knifeHalf]
            position_2 = [base, knifeHalf, knifeHalf]
            position_3 = [base, knifeHalf, -knifeHalf]

            for i in range(xKnifeCount):
                vtx_0 = OpenMaya.MFloatPoint(position_0[0] + voxelSize * i + xo, position_0[1] + yo, position_0[2] + zo)
                vtx_1 = OpenMaya.MFloatPoint(position_1[0] + voxelSize * i + xo, position_1[1] + yo, position_1[2] + zo)
                vtx_2 = OpenMaya.MFloatPoint(position_2[0] + voxelSize * i + xo, position_2[1] + yo, position_2[2] + zo)
                vtx_3 = OpenMaya.MFloatPoint(position_3[0] + voxelSize * i + xo, position_3[1] + yo, position_3[2] + zo)

                points.set(vtx_0, pointIndex)
                points.set(vtx_1, pointIndex + 1)
                points.set(vtx_2, pointIndex + 2)
                points.set(vtx_3, pointIndex + 3)

                faceConnects.set(pointIndex, pointIndex)
                faceConnects.set(pointIndex + 1, pointIndex + 1)
                faceConnects.set(pointIndex + 2, pointIndex + 2)
                faceConnects.set(pointIndex + 3, pointIndex + 3)

                faceCounts.set(4, faceCountIndex)

                pointIndex += 4
                faceCountIndex += 1

            # Compute knife frame in XZ plane
            base = -voxelSize * (yKnifeCount - 1) / 2.0
            position_0 = [-knifeHalf, base, -knifeHalf]
            position_1 = [knifeHalf, base, -knifeHalf]
            position_2 = [knifeHalf, base, knifeHalf]
            position_3 = [-knifeHalf, base, knifeHalf]

            for i in range(yKnifeCount):
                vtx_0 = OpenMaya.MFloatPoint(position_0[0] + xo, position_0[1] + voxelSize * i + yo, position_0[2] + zo)
                vtx_1 = OpenMaya.MFloatPoint(position_1[0] + xo, position_1[1] + voxelSize * i + yo, position_1[2] + zo)
                vtx_2 = OpenMaya.MFloatPoint(position_2[0] + xo, position_2[1] + voxelSize * i + yo, position_2[2] + zo)
                vtx_3 = OpenMaya.MFloatPoint(position_3[0] + xo, position_3[1] + voxelSize * i + yo, position_3[2] + zo)

                points.set(vtx_0, pointIndex)
                points.set(vtx_1, pointIndex + 1)
                points.set(vtx_2, pointIndex + 2)
                points.set(vtx_3, pointIndex + 3)

                faceConnects.set(pointIndex, pointIndex)
                faceConnects.set(pointIndex + 1, pointIndex + 1)
                faceConnects.set(pointIndex + 2, pointIndex + 2)
                faceConnects.set(pointIndex + 3, pointIndex + 3)

                faceCounts.set(4, faceCountIndex)

                pointIndex += 4
                faceCountIndex += 1

            # Compute knife frame in XY plane
            base = -voxelSize * (zKnifeCount - 1) / 2.0
            position_0 = [-knifeHalf, -knifeHalf, base]
            position_1 = [-knifeHalf, knifeHalf, base]
            position_2 = [knifeHalf, knifeHalf, base]
            position_3 = [knifeHalf, -knifeHalf, base]

            for i in range(zKnifeCount):
                vtx_0 = OpenMaya.MFloatPoint(position_0[0] + xo, position_0[1] + yo, position_0[2] + voxelSize * i + zo)
                vtx_1 = OpenMaya.MFloatPoint(position_1[0] + xo, position_1[1] + yo, position_1[2] + voxelSize * i + zo)
                vtx_2 = OpenMaya.MFloatPoint(position_2[0] + xo, position_2[1] + yo, position_2[2] + voxelSize * i + zo)
                vtx_3 = OpenMaya.MFloatPoint(position_3[0] + xo, position_3[1] + yo, position_3[2] + voxelSize * i + zo)

                points.set(vtx_0, pointIndex)
                points.set(vtx_1, pointIndex + 1)
                points.set(vtx_2, pointIndex + 2)
                points.set(vtx_3, pointIndex + 3)

                faceConnects.set(pointIndex, pointIndex)
                faceConnects.set(pointIndex + 1, pointIndex + 1)
                faceConnects.set(pointIndex + 2, pointIndex + 2)
                faceConnects.set(pointIndex + 3, pointIndex + 3)

                faceCounts.set(4, faceCountIndex)

                pointIndex += 4
                faceCountIndex += 1

            meshFS = OpenMaya.MFnMesh()
            meshFS.create(numVertices, numFaces, points, faceCounts, faceConnects, newOutputMeshData)

            # Set the output data
            outputMeshHandle = data.outputValue(voxelPreviewNode.outFrame)
            outputMeshHandle.setMObject(newOutputMeshData)

            data.setClean(plug)
        else:
            return OpenMaya.kUnknownParameter


# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # initialize the input and output attributes. Be sure to use the
    # MAKE_INPUT and MAKE_OUTPUT functions.

    voxelPreviewNode.inXOffset = nAttr.create("offsetX", "osX", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    voxelPreviewNode.inYOffset = nAttr.create("offsetY", "osY", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    voxelPreviewNode.inZOffset = nAttr.create("offsetZ", "osZ", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    voxelPreviewNode.inVoxelSize = nAttr.create("voxelSize", "vsz", OpenMaya.MFnNumericData.kFloat, 0.5)
    MAKE_INPUT(nAttr)
    voxelPreviewNode.inXKnifeCount = nAttr.create("knifeCountX", "kcX", OpenMaya.MFnNumericData.kInt, 1)
    MAKE_INPUT(nAttr)
    voxelPreviewNode.inYKnifeCount = nAttr.create("knifeCountY", "kcY", OpenMaya.MFnNumericData.kInt, 1)
    MAKE_INPUT(nAttr)
    voxelPreviewNode.inZKnifeCount = nAttr.create("knifeCountZ", "kcZ", OpenMaya.MFnNumericData.kInt, 1)
    MAKE_INPUT(nAttr)
    voxelPreviewNode.outFrame = tAttr.create("knifeFrame", "kf", OpenMaya.MFnData.kMesh)
    MAKE_OUTPUT(tAttr)

    try:
        # Add the attributes to the node and set up the attributeAffects (addAttribute, and attributeAffects)
        voxelPreviewNode.addAttribute(voxelPreviewNode.inXOffset)
        voxelPreviewNode.addAttribute(voxelPreviewNode.inYOffset)
        voxelPreviewNode.addAttribute(voxelPreviewNode.inZOffset)
        voxelPreviewNode.addAttribute(voxelPreviewNode.inVoxelSize)
        voxelPreviewNode.addAttribute(voxelPreviewNode.inXKnifeCount)
        voxelPreviewNode.addAttribute(voxelPreviewNode.inYKnifeCount)
        voxelPreviewNode.addAttribute(voxelPreviewNode.inZKnifeCount)
        voxelPreviewNode.addAttribute(voxelPreviewNode.outFrame)

        voxelPreviewNode.attributeAffects(voxelPreviewNode.inXOffset, voxelPreviewNode.outFrame)
        voxelPreviewNode.attributeAffects(voxelPreviewNode.inYOffset, voxelPreviewNode.outFrame)
        voxelPreviewNode.attributeAffects(voxelPreviewNode.inZOffset, voxelPreviewNode.outFrame)
        voxelPreviewNode.attributeAffects(voxelPreviewNode.inVoxelSize, voxelPreviewNode.outFrame)
        voxelPreviewNode.attributeAffects(voxelPreviewNode.inXKnifeCount, voxelPreviewNode.outFrame)
        voxelPreviewNode.attributeAffects(voxelPreviewNode.inYKnifeCount, voxelPreviewNode.outFrame)
        voxelPreviewNode.attributeAffects(voxelPreviewNode.inZKnifeCount, voxelPreviewNode.outFrame)

        print "voxelPreviewNode Initialized!\n"

    except:
        sys.stderr.write(("Failed to create attributes of %s node\n", kPluginNodeTypeName))

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(voxelPreviewNode())

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(kPluginNodeTypeName, voxelPreviewNodeID, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write("Failed to register node: %s\n" % kPluginNodeTypeName)

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(voxelPreviewNodeID)
    except:
        sys.stderr.write("Failed to unregister node: %s\n" % kPluginNodeTypeName)
