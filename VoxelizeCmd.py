import sys

# Imports to use the Maya Python API
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

# Import the Python wrappers for MEL commands
import maya.cmds as cmds

# Import MEL commands
import maya.mel as mel

# The name of the command.
kPluginCmdName = 'voxelize'


##########################################################
# Plug-in
##########################################################
class voxelizeCmd(OpenMayaMPx.MPxCommand):

    def __init__(self):
        """ Constructor. """
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, args):
        """ Command execution. """

        voxelSize = 1.0
        knifeCount = [1, 1, 1]
        offset = [0.0, 0.0, 0.0]
        gapSize = 0.1

        # Parse the argument first
        argData = OpenMaya.MArgParser(self.syntax(), args)
        if argData.isFlagSet("ox"):
            offset[0] = argData.flagArgumentDouble("ox", 0)
            mel.eval("print " + str(offset[0]))
        if argData.isFlagSet("oy"):
            offset[1] = argData.flagArgumentDouble("oy", 0)
        if argData.isFlagSet("oz"):
            offset[2] = argData.flagArgumentDouble("oz", 0)
        if argData.isFlagSet("kx"):
            knifeCount[0] = argData.flagArgumentInt("kx", 0)
        if argData.isFlagSet("ky"):
            knifeCount[1] = argData.flagArgumentInt("ky", 0)
        if argData.isFlagSet("kz"):
            knifeCount[2] = argData.flagArgumentInt("kz", 0)
        if argData.isFlagSet("vz"):
            voxelSize = argData.flagArgumentDouble("vz", 0)

        # Use the currently selected object as the source
        source = cmds.ls(sl=True)
        objName = self.voxelize(source, voxelSize, gapSize, knifeCount, offset)
        self.energy(objName=objName)

    def voxelize(self, source, voxelSize, gapSize, knifeCount, offset):
        """ Voxelize the first object in source. """
        if len(source) < 1:
            return ""
        objName = source[0]
        boundingBox = cmds.exactWorldBoundingBox(source[0])
        #translation = [(boundingBox[i] + boundingBox[i + 3]) / 2.0 for i in range(3)]
        knifeSize = max([boundingBox[i + 3] * 2 - boundingBox[i] * 2 for i in range(3)])
        knifeSize = max(knifeSize, voxelSize * (1 + max(knifeCount)))

        # Build knife frame and cut the source object
        base = [-voxelSize * (knifeCount[i] - 1) / 2.0 for i in range(3)]

        knifeX = cmds.polyCube(n='knife1', w=gapSize, h=knifeSize, d=knifeSize)
        cmds.move(base[0], 0, 0, knifeX[0])
        cmds.move(offset[0], offset[1], offset[2], knifeX[0], relative=True)
        knifeY = cmds.polyCube(n='knife2', w=knifeSize, h=gapSize, d=knifeSize)
        cmds.move(0, base[1], 0, knifeY[0])
        cmds.move(offset[0], offset[1], offset[2], knifeY[0], relative=True)
        knifeZ = cmds.polyCube(n='knife3', w=knifeSize, h=knifeSize, d=gapSize)
        cmds.move(0, 0, base[2], knifeZ[0])
        cmds.move(offset[0], offset[1], offset[2], knifeZ[0], relative=True)

        for i in range(1, knifeCount[0]):
            knife = cmds.duplicate(knifeX[0])
            cmds.move(voxelSize * i, 0, 0, knife[0], relative=True)
            source = cmds.polyBoolOp(source[0], knife[0], op=2)

        for i in range(1, knifeCount[1]):
            knife = cmds.duplicate(knifeY[0])
            cmds.move(0, voxelSize * i, 0, knife[0], relative=True)
            source = cmds.polyBoolOp(source[0], knife[0], op=2)

        for i in range(1, knifeCount[2]):
            knife = cmds.duplicate(knifeZ[0])
            cmds.move(0, 0, voxelSize * i, knife[0], relative=True)
            source = cmds.polyBoolOp(source[0], knife[0], op=2)

        source = cmds.polyBoolOp(source[0], knifeX[0], op=2)
        source = cmds.polyBoolOp(source[0], knifeY[0], op=2)
        source = cmds.polyBoolOp(source[0], knifeZ[0], op=2)

        cmds.delete(source[0], ch=True)
        objName = cmds.rename(source[0], objName)
        cmds.xform(objName, cpc=True)

        return objName

    def energy(self, objName):
        """ Calculate the energy of this voxelization"""
        source = cmds.polySeparate(objName)
        # cmds.xform(source, cpc=True)

        selection = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(selection)
        iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMesh)

        while not iterSel.isDone():
            dagPath = OpenMaya.MDagPath()
            iterSel.getDagPath(dagPath)
            currentInMeshMFnMesh = OpenMaya.MFnMesh(dagPath)

            # Create empty point array
            inMeshMPointArray = OpenMaya.MPointArray()
            currentInMeshMFnMesh.getPoints(inMeshMPointArray, OpenMaya.MSpace.kWorld)
            for i in range(inMeshMPointArray.length()):
                self.output(inMeshMPointArray[i])
            mel.eval("print \"\\r\\n\";")
            iterSel.next()

    def output(self, vec):
        mel.eval('print <<' + str(vec[0]) + ',' + str(vec[1]) + ',' + str(vec[2]) + '>>;')
        mel.eval("print \"\\r\\n\";")


##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    """ Create an instance of our command. """
    return OpenMayaMPx.asMPxPtr(voxelizeCmd())


def syntaxCreator():
    """ Defines the argument and flag syntax for this command. """
    syntax = OpenMaya.MSyntax()

    # [in] shortName the string representing the short (< 4 character) version of the flag
    # [in] longName the string representing the int (> 3 character) version of the flag
    syntax.addFlag("ox", "offsetX", OpenMaya.MSyntax.kDouble)
    syntax.addFlag("oy", "offsetY", OpenMaya.MSyntax.kDouble)
    syntax.addFlag("oz", "offsetZ", OpenMaya.MSyntax.kDouble)
    syntax.addFlag("kx", "knifeCtX", OpenMaya.MSyntax.kLong)
    syntax.addFlag("ky", "knifeCtY", OpenMaya.MSyntax.kLong)
    syntax.addFlag("kz", "knifeCtZ", OpenMaya.MSyntax.kLong)
    syntax.addFlag("vz", "voxelSize", OpenMaya.MSyntax.kDouble)

    return syntax


def initializePlugin(mobject):
    """ Initialize the plug-in when Maya loads it. """
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "cg@penn", "1.0", "2020")
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator, syntaxCreator)
    except:
        sys.stderr.write('Failed to register command: ' + kPluginCmdName)
    cmds.unloadPlugin(mplugin.loadPath() + '/VoxelPreviewNode.py')
    cmds.loadPlugin(mplugin.loadPath() + '/VoxelPreviewNode.py')
    mel.eval('source "' + mplugin.loadPath() + '/VoxelizeMenu.mel";')


def uninitializePlugin(mobject):
    """ Uninitialize the plug-in when Maya un-loads it. """
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: ' + kPluginCmdName)
    mel.eval("global string $myMenuMain; if (`menu -exists $myMenuMain`) deleteUI $myMenuMain;")
    cmds.unloadPlugin(mplugin.loadPath() + '/VoxelPreviewNode.py')