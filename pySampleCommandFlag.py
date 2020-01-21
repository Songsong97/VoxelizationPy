# sampleCommandFlagTuple.py

import sys
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

# ... additional imports here ...

kPluginCmdName = 'myCommandWithTupleFlag'

kShortFlagName = '-tf'
kLongFlagName = '-myTupleFlag'


##########################################################
# Plug-in
##########################################################
class MyCommandWithFlagTupleClass(OpenMayaMPx.MPxCommand):

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
        '''
        The presence of this function is not enforced,
        but helps separate argument parsing code from other
        command code.
        '''

        # The following MArgParser object allows you to check if specific flags are set.
        argData = OpenMaya.MArgParser(self.syntax(), args)

        if argData.isFlagSet(kShortFlagName):
            # In this case, we print the passed flags's three parameters, indexed from 0 to 2.
            flagParam0 = argData.flagArgumentInt(kShortFlagName, 0)
            flagParam1 = argData.flagArgumentInt(kShortFlagName, 1)
            flagParam2 = argData.flagArgumentInt(kShortFlagName, 2)

            print kLongFlagName + '[0]: ' + str(flagParam0)
            print kLongFlagName + '[1]: ' + str(flagParam1)
            print kLongFlagName + '[2]: ' + str(flagParam2)

        # ... If there are more flags, process them here ...


##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    ''' Create an instance of our command. '''
    return OpenMayaMPx.asMPxPtr(MyCommandWithFlagTupleClass())


def syntaxCreator():
    ''' Defines the argument and flag syntax for this command. '''
    syntax = OpenMaya.MSyntax()

    # In this example, our flag will be expecting three OpenMaya.MSyntax.kDouble parameters.
    syntax.addFlag(kShortFlagName, kLongFlagName, OpenMaya.MSyntax.kDouble, OpenMaya.MSyntax.kDouble,
                   OpenMaya.MSyntax.kDouble)

    # ... Add more flags here ...

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