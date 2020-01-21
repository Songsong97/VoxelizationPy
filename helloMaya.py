import sys

# Imports to use the Maya Python API
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

# The name of the command.
kPluginCmdName = 'pyHelloMaya'

# kNameFlagShort = "-n"
# kNameFlagLong = "-name"
kIdFlagShort = "-i"
kIdFlagLong = "-myIdFlag"

##########################################################
# Plug-in
##########################################################
class helloMayaCommand(OpenMayaMPx.MPxCommand):

    def __init__(self):
        ''' Constructor. '''
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, args):
        ''' Command execution. '''

        # We recommend parsing your arguments first.
        self.parseArguments(args)

        # Remove the following 'pass' keyword and replace it with the code you want to run.
        pass

    def parseArguments(self, args):
        # The following MArgParser object allows you to check if specific flags are set.
        argData = OpenMaya.MArgParser(self.syntax(), args)

        # ... If there are more flags, process them here ...
        # if argData.isFlagSet(kNameFlag):
        #     flagParam = argData.flagArgumentString(kNameFlag, 0)
        #     print kNameFlag + ": " + flagParam

        if argData.isFlagSet(kIdFlagShort):
            # In this case, we print the passed flags's three parameters, indexed from 0 to 2.
            flagParam = argData.flagArgumentInt(kIdFlagShort, 0)
            print kIdFlagShort + ': ' + str(flagParam)


##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    ''' Create an instance of our command. '''
    return OpenMayaMPx.asMPxPtr(helloMayaCommand())


def syntaxCreator():
    ''' Defines the argument and flag syntax for this command. '''
    syntax = OpenMaya.MSyntax()

    # syntax.addFlag(kNameFlag, kNameFlag, OpenMaya.MSyntax.kString)
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