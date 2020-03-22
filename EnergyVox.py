import sys

# Imports to use the Maya Python API
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

# Import the Python wrappers for MEL commands
import maya.cmds as cmds

# Import MEL commands
import maya.mel as mel

# The name of the command.
kPluginCmdName = 'energyvox'

# [in] shortName the string representing the short (< 4 character) version of the flag
# [in] longName the string representing the int (> 3 character) version of the flag
kNameFlagShort = "-nf"
kNameFlagLong = "-name"
kIdFlagShort = "-i"
kIdFlagLong = "-myIdFlag"

##########################################################
# Plug-in
##########################################################
class energyVox(OpenMayaMPx.MPxCommand):

    def __init__(self):
        ''' Constructor. '''
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, args):
        ''' Command execution. '''
        mel.eval('$Evox = ' + str(15) + ';')

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
            iterSel.next()

    def output(self, vec):
        mel.eval('print <<' + str(vec[0]) + ',' + str(vec[1]) + ',' + str(vec[2]) + '>>;')

##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    ''' Create an instance of our command. '''
    return OpenMayaMPx.asMPxPtr(energyVox())


def syntaxCreator():
    ''' Defines the argument and flag syntax for this command. '''
    syntax = OpenMaya.MSyntax()
    return syntax


def initializePlugin(mobject):
    ''' Initialize the plug-in when Maya loads it. '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "cg@penn", "1.0", "2020")
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator, syntaxCreator)
    except:
        sys.stderr.write('Failed to register command: ' + kPluginCmdName)
    mel.eval('global float $Evox;')


def uninitializePlugin(mobject):
    ''' Uninitialize the plug-in when Maya un-loads it. '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: ' + kPluginCmdName)