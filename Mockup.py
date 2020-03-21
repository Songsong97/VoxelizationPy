import sys

# Imports to use the Maya Python API
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

# Import the Python wrappers for MEL commands
import maya.cmds as cmds

# The name of the command.
kPluginCmdName = 'pyMockup'

# [in] shortName the string representing the short (< 4 character) version of the flag
# [in] longName the string representing the int (> 3 character) version of the flag
kNameFlagShort = "-nf"
kNameFlagLong = "-name"
kIdFlagShort = "-i"
kIdFlagLong = "-myIdFlag"

##########################################################
# Plug-in
##########################################################
class pyMockup(OpenMayaMPx.MPxCommand):

    def __init__(self):
        ''' Constructor. '''
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, args):
        ''' Command execution. '''

        # Parsing your arguments first.

        window = cmds.window(title="Everything Box Transformer", widthHeight=(320, 80),
                             minimizeButton=False, maximizeButton=False)
        cmds.columnLayout(columnAttach=('both', 50), rowSpacing=10, columnWidth=350)

        cmds.floatSliderGrp(label='Voxel Size', field=True, minValue=-10.0, maxValue=10.0, fieldMinValue=-100.0,
                            fieldMaxValue=100.0, value=0)
        cmds.button(label='Voxelize')
        cmds.button(label='Fit Tree')
        cmds.button(label='Generate Sequence')
        cmds.button(label='Cancel', command=('cmds.deleteUI(\"' + window + '\", window=True)'))
        cmds.showWindow(window)

    def parseArguments(self, args):
        # The following MArgParser object allows you to check if specific flags are set.
        argData = OpenMaya.MArgParser(self.syntax(), args)

        inputName = ""
        inputID = "0"

        if argData.isFlagSet(kNameFlagShort):
            flagParam = argData.flagArgumentString(kNameFlagShort, 0)
            inputName = str(flagParam)

        if argData.isFlagSet(kIdFlagShort):
            flagParam = argData.flagArgumentInt(kIdFlagShort, 0)
            inputID = str(flagParam)

        return [inputName, inputID]

##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    ''' Create an instance of our command. '''
    return OpenMayaMPx.asMPxPtr(pyMockup())


def syntaxCreator():
    ''' Defines the argument and flag syntax for this command. '''
    syntax = OpenMaya.MSyntax()

    syntax.addFlag(kNameFlagShort, kNameFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(kIdFlagShort, kIdFlagLong, OpenMaya.MSyntax.kLong)

    return syntax


def initializePlugin(mobject):
    ''' Initialize the plug-in when Maya loads it. '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "cg@penn", "1.0", "2012")
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator, syntaxCreator)
    except:
        sys.stderr.write('Failed to register command: ' + kPluginCmdName)


def uninitializePlugin(mobject):
    ''' Uninitialize the plug-in when Maya un-loads it. '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: ' + kPluginCmdName)