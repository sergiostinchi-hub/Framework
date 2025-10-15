# Authors: Sergio Stinchi

# Version        Description
# 1.1.1          Changed check for resources
# 1.1.0          Add StringNameSpaceBinding check
# 1.0.0          Starting version

# Import
import sys
import java
from string import replace



commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))



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
# Variables
scriptName = "CreateNameSpaceBinding.py"
version = "1.1.1"

log.setClass(scriptName)
printBasicScriptInfo("Sergio Stinchi",scriptName,version)


# common data
scopeName = ''                # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...) ]
                              #            Warning: if the scope is a server and its name is not unique on the cell 
                              #                     it must be used the form <Node>:<Server> 
name = ''                     # mandatory [Specifies the name that uniquely identifies this configured binding.]
nameInNameSpace = ''          # mandatory [Specifies the name used for this binding in the namespace.]
typeNameSpaceBinding = ''     # mandatory [Shows the type of binding configured. Possible choices are at the moment: String or EJB (CORBA and Indirect not yet).
                              #            Admitted values: StringNameSpaceBinding or EjbNameSpaceBinding]
# for StringNameSpaceBinding only
stringToBind = ''             # mandatory [Specifies the string to be bound into the namespace.]
# for EjbNameSpaceBinding only
bindingLocation = ''          # mandatory [Specifies if the enterprise bean is configured on a single server or on a cluster.
                              #            Admitted values: SINGLESERVER or SERVERCLUSTER]
applicationNodeName = ''      # optional  [If Single server is specified, type the node name (mandatory).]
applicationServerName = ''    # mandatory [Specifies the name of the server in which the enterprise bean is configured.]
ejbJndiName = ''              # mandatory [Specifies the JNDI name of the deployed enterprise bean.]
# for all
scope = ''                    # Read only [Name of the Server, Node or Cluster where the enterprise bean is configured.]
deleteIfExist = 0


# Read target data file
print "Read target data file ..."
try: execfile(sys.argv[0])
except IOError, ioe:
   print "ERROR: " + str(ioe)
   sys.exit(-1)
else: print "Read target data file done"

# Check data read
print "Check data read ..."
if (scopeName == None) or (len(scopeName.strip()) == 0):
   print "ERROR: The variable scopeName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
if (name == None) or (len(name.strip()) == 0):
   print "ERROR: The variable name is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
if (nameInNameSpace == None) or (len(nameInNameSpace.strip()) == 0):
   print "ERROR: The variable nameInNameSpace is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
if typeNameSpaceBinding.strip() not in ['StringNameSpaceBinding', 'EjbNameSpaceBinding']:
   print "ERROR: The variable typeNameSpaceBinding could be only ['StringNameSpaceBinding', 'EjbNameSpaceBinding']"
   print "%s done" % (scriptName)
   sys.exit(-1)

if typeNameSpaceBinding.strip() == 'StringNameSpaceBinding':
   if (stringToBind == None) or (len(stringToBind.strip()) == 0):
      print "ERROR: The variable stringToBind is mandatory"
      print "%s done" % (scriptName)
      sys.exit(-1)

if typeNameSpaceBinding.strip() == 'EjbNameSpaceBinding':
   if (applicationServerName == None) or (len(applicationServerName.strip()) == 0):
      print "ERROR: The variable applicationServerName is mandatory"
      print "%s done" % (scriptName)
      sys.exit(-1)

   if (ejbJndiName == None) or (len(ejbJndiName.strip()) == 0):
      print "ERROR: The variable ejbJndiName is mandatory"
      print "%s done" % (scriptName)
      sys.exit(-1)
   
   if (bindingLocation == None) or len(bindingLocation.strip()) != 0 :
      if bindingLocation.strip() not in ['SINGLESERVER', 'SERVERCLUSTER']:
         print "WARNING: The variable bindingLocation has to be SINGLESERVER or SERVERCLUSTER. Using default SERVERCLUSTER"
         bindingLocation = 'SERVERCLUSTER'

   if bindingLocation.strip() == 'SINGLESERVER':		 
      if (applicationNodeName == None) or (len(applicationNodeName.strip()) == 0):
         print "ERROR: The variable applicationNodeName is mandatory"
         print "%s done" % (scriptName)
         sys.exit(-1)
   
if deleteIfExist not in [0, 1]:
   print "ERROR: The variable deleteIfExist can be 0 or 1"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
print "Check data read done"

# set default values

# Check scopeName ...
print "Check scope %s ..." % (scopeName)
(scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
ApplySystemPropertyDmgr('com.ibm.websphere.management.configservice.validateNames','true')
# Create nameSpaceBinding
print "Create nameSpaceBinding ... %s" % (name)
#out = checkIfResourceExist(scopeid, name, typeNameSpaceBinding)
#if out != None:
(resourceId , resourceName) = checkIfResourceExist(scopeid, name, typeNameSpaceBinding)
if resourceId != None: 
   print "nameSpaceBinding %s already exists" % name
   if deleteIfExist == 1:
      print "Delete existing nameSpaceBinding:",
      try: 
         AdminConfig.remove(resourceId)
         print "OK"
      except: clearExit("KO\nRollback and exit", -1) 
   else: clearExit("", 0)   
try:
   if typeNameSpaceBinding == 'EjbNameSpaceBinding':
      print "create EjbNameSpaceBinding %s" % (name),
      AdminConfig.create('EjbNameSpaceBinding', scopeid, '[[name "%s"] [nameInNameSpace "%s"]  [applicationNodeName "%s"] [applicationServerName "%s"] [bindingLocation "%s"] [ejbJndiName "%s"]]' %(name,nameInNameSpace,applicationNodeName,applicationServerName,bindingLocation,ejbJndiName))
      print " OK"
   elif typeNameSpaceBinding == 'StringNameSpaceBinding':
      print "create StringNameSpaceBinding %s" % (name),
      attrs = '[[name "%s"] [nameInNameSpace "%s"] [stringToBind "%s"]]' %(name,nameInNameSpace,stringToBind)
      AdminConfig.create('StringNameSpaceBinding', scopeid , attrs)     
      print " OK"
except:
   print "KO"
   type, value, traceback = sys.exc_info()
   print "ERROR: %s (%s)" % (str(value), type)
   clearExit("Rollback and exit", -1)
print "Save ..."

syncEnv(AdminConfig.hasChanges())
# Done
print "%s V%s done" % (scriptName, version)
