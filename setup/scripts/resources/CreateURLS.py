# Authors: Sergio Stinchi

# Version        Description
# 1.2.0          Changed check for resources
# 1.1.0          Add Function checkScopeName()
# 1.0.0          Starting version

# Import
import sys
import java
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Global variables
authors="Sergio Stinchi WebSphere Lab Services"
scriptName = "CreateURLS.py"
version = "2.0.0"
printBasicScriptInfo(authors,scriptName,version)

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

# Data
scopeName = ''               # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...)]
                             #            Warning: if the scope is a server and its name is not unique on the cell
                             #                     it must be used the form <Node>:<Server>
name = ''                    # mandatory [The name of the resource]     
jndiName = ''                # mandatory [The jndi of the resource]
providerName=''              # mandatory [Specifies the URL provider name for the URL configuration.]
spec=''                      # mandatory [Specifies the string from which to form a URL.]
deleteIfExist=0


# Read target data file
log.INFO("Read target data file ...")
try: execfile(sys.argv[0])
except IOError, ioe:
   print "ERROR: " + str(ioe)
   sys.exit(-1)
else: log.INFO( "Read target data file done")

if (scopeName == None) or (len(scopeName.strip()) == 0):
   print "ERROR: The variable scopeName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
if (name == None) or (len(name.strip()) == 0):
   print "ERROR: The variable name is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if (jndiName == None) or len(jndiName.strip()) == 0:
   print "ERROR: The variable jndiName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if (providerName == None) or (len(providerName.strip()) == 0):
   print "ERROR: The variable providerName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
if (spec == None) or (len(spec.strip()) == 0):
   print "ERROR: The variable spec is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if deleteIfExist not in [0, 1]:
   print "ERROR: The variable deleteIfExist can be 0 or 1"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
log.INFO(  "Check data read done")

# set default values

# Check scopeName ...
log.INFO( "Check scope %s ..." % (scopeName))
(scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)  
#Was855Cell(cells/Was855Cell|cell.xml#Cell_1) 
check = scopeid[scopeid.find("(")+1:scopeid.find("|")+1] 
log.DEBUG("check == %s" %check)
# Create URL
log.INFO( "Create URL ... %s:" % (name),1)
(resourceId , resourceName) = checkIfResourceExist(scopeid, name, "URL")
if resourceId != None: 
   log.INFO( " WARNING URL %s already exists " % (name),2) 
   if deleteIfExist == 1:
      log.INFO( "Delete existing URL:",1),
      try: 
         AdminConfig.remove(resourceId)
         log.INFO( "OK",2)
      except: clearExit("KO\nRollback and exit", -1) 
   else: clearExit("", 0)   
try:
    log.INFO( "Create URL %s " % (name),1)
    name = ['name', name]
    spec = ['spec', spec]
    jndiName = ['jndiName', jndiName]
    UrlProviderList = AdminConfig.list('URLProvider',scopeid).splitlines()
    for UrlProvider in UrlProviderList:
        providerID=UrlProvider
        if providerID.find(check)> -1:
            #log.INFO("found correct providerID = %s" %providerID)
            providerName=AdminConfig.showAttribute(providerID,'name')
            urlAttrs = [name, jndiName, spec]
            ulrId = AdminConfig.create('URL', providerID, urlAttrs)         
            log.INFO( "OK",2)
except SystemExit, e: sys.exit(e)
except:
      type, value, traceback = sys.exc_info()
      log.INFO( "ERROR: %s (%s)" % (str(value), type))
      clearExit("Rollback and exit", -1)

syncEnv(AdminConfig.hasChanges())

# Done
log.INFO( "%s V%s done" % (scriptName, version))
