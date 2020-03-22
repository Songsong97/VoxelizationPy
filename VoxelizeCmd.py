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

# [in] shortName the string representing the short (< 4 character) version of the flag
# [in] longName the string representing the int (> 3 character) version of the flag
kNameFlagShort = "-nf"
kNameFlagLong = "-name"
kIdFlagShort = "-i"
kIdFlagLong = "-myIdFlag"


##########################################################
# Plug-in
##########################################################
class voxelizeCmd(OpenMayaMPx.MPxCommand):

    def __init__(self):
        """ Constructor. """
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, args):
        """ Command execution. """

        voxelSize = 1
        gapSize = 0.1
        knifeCount = [2, 2, 2]

        # Use the currently selected object as the source
        source = cmds.ls(sl=True)
        objName = self.voxelize(source=source, voxelSize=voxelSize, gapSize=gapSize, knifeCount=knifeCount)
        self.energy(objName=objName)

    def voxelize(self, source, voxelSize, gapSize, knifeCount):
        """ Voxelize the first object in source. """
        if len(source) < 1:
            return ""
        objName = source[0]
        boundingBox = cmds.exactWorldBoundingBox(source[0])
        translation = [(boundingBox[i] + boundingBox[i + 3]) / 2.0 for i in range(3)]
        knifeSize = max([boundingBox[i + 3] * 2 - boundingBox[i] * 2 for i in range(3)])
        knifeSize = max(knifeSize, voxelSize * (1 + max(knifeCount)))

        # Build knife frame and cut the source object
        base = [-voxelSize * (knifeCount[i] - 1) / 2.0 for i in range(3)]

        knifeX = cmds.polyCube(n='knife1', w=gapSize, h=knifeSize, d=knifeSize)
        cmds.move(base[0], 0, 0, knifeX[0])
        knifeY = cmds.polyCube(n='knife2', w=knifeSize, h=gapSize, d=knifeSize)
        cmds.move(0, base[1], 0, knifeY[0])
        knifeZ = cmds.polyCube(n='knife3', w=knifeSize, h=knifeSize, d=gapSize)
        cmds.move(0, 0, base[2], knifeZ[0])

        for i in range(1, knifeCount[0]):
            knife = cmds.duplicate(knifeX[0])
            cmds.move(voxelSize * i, 0, 0, knife[0], relative=True)
            cmds.move(translation[0], translation[1], translation[2], knife[0], relative=True)
            source = cmds.polyBoolOp(source[0], knife[0], op=2)

        for i in range(1, knifeCount[1]):
            knife = cmds.duplicate(knifeY[0])
            cmds.move(0, voxelSize * i, 0, knife[0], relative=True)
            cmds.move(translation[0], translation[1], translation[2], knife[0], relative=True)
            source = cmds.polyBoolOp(source[0], knife[0], op=2)

        for i in range(1, knifeCount[2]):
            knife = cmds.duplicate(knifeZ[0])
            cmds.move(0, 0, voxelSize * i, knife[0], relative=True)
            cmds.move(translation[0], translation[1], translation[2], knife[0], relative=True)
            source = cmds.polyBoolOp(source[0], knife[0], op=2)

        cmds.move(translation[0], translation[1], translation[2], knifeX[0], relative=True)
        source = cmds.polyBoolOp(source[0], knifeX[0], op=2)
        cmds.move(translation[0], translation[1], translation[2], knifeY[0], relative=True)
        source = cmds.polyBoolOp(source[0], knifeY[0], op=2)
        cmds.move(translation[0], translation[1], translation[2], knifeZ[0], relative=True)
        source = cmds.polyBoolOp(source[0], knifeZ[0], op=2)

        cmds.delete(source[0], ch=True)
        objName = cmds.rename(source[0], objName)
        cmds.xform(objName, cpc=True)

        return objName


    def energy(self, objName):
        """ Calculate the energy of this voxelization"""
        source = cmds.polySeparate(objName)
        # cmds.xform(source, cpc=True)

        for i in range(len(source)):
            current = source[i]
            # Todo

        return 0
##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    """ Create an instance of our command. """
    return OpenMayaMPx.asMPxPtr(voxelizeCmd())


def syntaxCreator():
    """ Defines the argument and flag syntax for this command. """
    syntax = OpenMaya.MSyntax()
    return syntax


def initializePlugin(mobject):
    """ Initialize the plug-in when Maya loads it. """
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "cg@penn", "1.0", "2020")
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator, syntaxCreator)
    except:
        sys.stderr.write('Failed to register command: ' + kPluginCmdName)


def uninitializePlugin(mobject):
    """ Uninitialize the plug-in when Maya un-loads it. """
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: ' + kPluginCmdName)