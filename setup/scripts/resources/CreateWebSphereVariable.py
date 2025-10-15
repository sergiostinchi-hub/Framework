# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version

# Import
import sys
import java

# Variables
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))


scriptName = "CreateWebSphereVariable.py"
version = "1.0.4"
printBasicScriptInfo("Sergio Stinchi",scriptName,version)
log.setClass(scriptName)

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

# Command Line
argc = len(sys.argv)
if argc != 1:
   print "Usage: %s <target data file>" % (scriptName)
   sys.exit(-1)
        
# Start



# Data
variables = [['ServerCluster', 'WASBE', 'PIPPO', 'PIPPO'], ['ServerCluster', 'WASBE', 'pluto', 'pluto']]  # [['SERVERClustrer or Server','SCOPE NAME','NAME','VALUE']]
                                                                                                
# SCOPE_NAME     # mandatory, mandatory, the name of the scope resource (i.e: Telematico, DogTelProNode01, ...)
                 # Warning: if the scope is a server and its name is not unique on the cell
                 # it must be used the form <Node>:<Server>
# NAME           # mandatory
# VALUE          # mandatory

# Read target data file
print "Read target data file ..."
try: execfile(sys.argv[0])
except IOError, ioe:
   print "ERROR: " + str(ioe)
   sys.exit(-1)
else: print "Read target data file done"

# Check data read
print "Check data read ..."
if len(variables) > 0:
   if isinstance(variables, type([])) == 0:
      print "ERROR: The variable variables must be a list"
      print "%s done" % (scriptName)
      sys.exit(-1)
   for dummy in variables:
      if isinstance(dummy, type([])) == 0 or len(dummy) != 4:
         print "ERROR: Each object of variable variables must be a list of three items"
         print "%s done" % (scriptName)
         sys.exit(-1)


print "Modify or Create WebSphere Variables"
if len(variables) > 0:
   try:
      ScopeName = ''
      for webSphereVar in variables:
         (scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(webSphereVar[1])
         scopeRes = getStringScopeForId(scope, scopeid, scopeName, nodeName, serverName, clusterName)
         print "scopeRes = %s" % (scopeRes)
      	 variableMap = AdminConfig.getid(scopeRes + '/VariableMap:/')
         entries = AdminConfig.showAttribute(variableMap, 'entries')
         entries = entries[1:-1].split()
         name = webSphereVar[2]
         value = webSphereVar[3]
         if value.find('"') != -1: value = "'" + value + "'"
         elif value.find("'") != -1: value = '"' + value + '"'
         elif len(value) == 0: value = "''"      
         for prop in entries:
            symbolicName = AdminConfig.showAttribute(prop, 'symbolicName')
            if symbolicName == name:
               print "Modify Variable %s with Value %s in Scope %s:%s " % (name, value, webSphereVar[0], webSphereVar[1]),
               AdminConfig.modify(prop, "[ ['value' " + value + "] ]")
               name = None
         if name != None:
            print "Create Variable %s with Value %s in Scope %s:%s " % (name, value, webSphereVar[0], webSphereVar[1]),
            attr = [ ['symbolicName', name], ['value', value] ]
            AdminConfig.create('VariableSubstitutionEntry', variableMap, attr)
         print "OK"
   except:
      print "KO"
      type, value, traceback = sys.exc_info()
      print "ERROR: %s (%s)" % (str(value), type)
      clearExit("Rollback and exit", -1)

print "Setting WebSphere Variables"
if AdminConfig.hasChanges() == 1:
   # Save
   print "Save ..."
   AdminConfig.save()
   print "Save done"

   # Synchronization
syncEnv(AdminConfig.hasChanges())

# Done
print "%s V%s done" % (scriptName, version)   
