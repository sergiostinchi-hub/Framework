# Authors: Sergio Stinchi

# Version        Description
# 1.1.1          Removing mandatory for Queue Manager and changed check for resources
# 1.1.0          Correct Variable description
# 1.0.0          Starting version

# Import
import sys
import java
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

scope=''
scopeid=''
name=''
classPath=''
isolatedClassLoader=''
nativePath=''
description=''

# Variables
scriptName = "CreateSharedLibrary.py"
version = "1.2.0"

log.setClass(scriptName)
printBasicScriptInfo("Sergio Stinchi",scriptName,version)

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

def reset(text):
   if len(text) > 0: print text
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   print "Execute on file %s done" 

# Command Line
argc = len(sys.argv)
if argc != 1:
   print "Usage: %s <target data file>" % (scriptName)
   sys.exit(-1)
        
# Start
print "%s V%s" % (scriptName, version)

# Read target data file
print "Read target data file ..."
try: execfile(sys.argv[0])
except IOError, ioe:
   print "ERROR: " + str(ioe)
   sys.exit(-1)
else: print "Read target data file done"

# Check data read
print "Check data read ..."


# set default values
if (scopeName == None) or (len(scopeName.strip()) == 0):
   print "ERROR: The variable scopeName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
if (name == None) or (len(name.strip()) == 0):
   print "ERROR: The variable libname is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
if (classPath == None) or (len(classPath.strip()) == 0):
   print "ERROR: The variable jarfile is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)  

if (isolatedClassLoader == None) or (len(isolatedClassLoader.strip()) == 0):
   print "ERROR: The variable isolatedClassLoader is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)  

if (nativePath !=None) and (len(nativePath.strip()) == 2):
   print "native path = %s " %(nativePath)
   nativePath = ''

if isolatedClassLoader not in ['true','false']: 
   print "ERROR: The variable isolatedClassLoader can be true or false" 
   print "%s done" % (scriptName) 
   sys.exit(-1) 
   
if deleteIfExist not in [0, 1]: 
   print "ERROR: The variable deleteIfExist can be 0 or 1" 
   print "%s done" % (scriptName) 
   sys.exit(-1) 

print "isolatedClassLoader == %s " %(isolatedClassLoader)
(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)   

# Create AS
print "Create Shared Lib"


# Shared Library and Class Loader methods
(resourceId , resourceName) = checkIfResourceExist(scopeid, name, "Library")
if resourceId != None: 
   print "Shared Library %s already exists" % name 
   if deleteIfExist == 1: 
      print "Delete existing Shared Library :",
      try: 
         AdminConfig.remove(resourceId) 
         print "OK" 
      except: 
         print "KO" 
         reset("Unable to delete Resource %s" % (name))
      try: 
          print "Create Shared Library  %s in scope : %s" % (name,scopeid),
          AdminConfig.create('Library', scopeid, [['nativePath',nativePath],['name', name],['isolatedClassLoader', isolatedClassLoader],['description',description],['classPath', classPath]])
          print " OK"
      except: 
          print "KO" 
          type, value, traceback = sys.exc_info() 
          print "ERROR: %s (%s)" % (str(value), type) 
          clearExit("Rollback and exit", -1)
   else:
        print "Creation Resource Skipped"
   print "Create Shared Library done" 
else:
   try: 
      print "Create Shared Library  %s in scope : %s" % (name,scopeid),
      AdminConfig.create('Library', scopeid, [['nativePath',nativePath],['name', name],['isolatedClassLoader', isolatedClassLoader],['description',description],['classPath', classPath]])
      print " OK"
   except: 
      print "KO" 
      type, value, traceback = sys.exc_info() 
      print "ERROR: %s (%s)" % (str(value), type) 
      clearExit("Rollback and exit", -1)
        
# Done
print "%s V%s done" % (scriptName, version)
print "Save ..."
syncEnv(AdminConfig.hasChanges())

