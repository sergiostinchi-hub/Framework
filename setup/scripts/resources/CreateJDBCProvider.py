# Authors: Sergio Stinchi, Andrea Minuto

# Version        Description
# 1.0.6          Disabled deleteIfExist function for this version
# 1.0.5          Changed check for resources
# 1.0.4          Added WebSphere variables management
# 1.0.3          Corrected exception management
# 1.0.2          Corrected scope searching algorithm
# 1.0.1          Corrected by Andrea Minuto
# 1.0.0          Starting version

# Import
import sys
import java


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

# Variables
scriptName = "createJDBCProvider.py"
version = "1.0.5"
        
log.setClass(scriptName)
printBasicScriptInfo("Sergio Stinchi",scriptName,version)

# Data
scopeName = ''                # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...) ]
                              #            Warning: if the scope is a server and its name is not unique on the cell 
                              #                     it must be used the form <Node>:<Server> 
databaseType = ''             # mandatory [Database type. Admitted values: DB2, Derby, Informix, Oracle, Sybase, SQL Server, User-defined]
providerType = ''             # mandatory [The JDBC provider type, i.e: DB2 Universal JDBC Driver Provider, Informix JDBC Driver or Oracle JDBC Driver]
classpath = ''                # mandatory [Specifies a list of paths or JAR file names that form the location for the resource provider classes]
name = ''                     # mandatory [The name of the JDBC provider]
description = ''              # optional  [The description for the JDBC provider]
implementationClassName = ''  # optional  [Specifies the Java class name for the JDBC driver implementation]
nativePath = ''               # optional  [Specifies a list of paths that form the location for the resource provider native libraries]
isolated = 'false'            # optional  [Specifies whether the JDBC provider loads within the class loader. Admitted values: true or false. The default value is false. 
                              #            You cannot specify a native path for an isolated JDBC provider]
xa='false'                    # mandatory [It drives the implementation type. Admitted values: true or false. If not provided defaults to false
                              #            Use false if your application runs in a single phase or a local transaction. 
							  #            Use true to run in a global transaction]
deleteIfExist = 0             # 1 = delete the resource if exists  
webSphereVars = []            # WebSphere Variables, list of two items lists (e.g.: [ ['INFORMIX_JDBC_PATH', '/opt/IBM/informix/jdbc'] ])

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
   
if databaseType.strip() not in ['DB2', 'Derby', 'Informix', 'Oracle', 'Sybase', 'SQL Server', 'User-defined']:
   print "ERROR: The variable databaseType could be only ['DB2', 'Derby', 'Informix', 'Oracle', 'Sybase', 'SQL Server', 'User-defined']"
   print "%s done" % (scriptName)
   sys.exit(-1)

if (providerType == None) or (len(providerType.strip()) == 0):
   print "ERROR: The variable providerType is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if xa.strip() not in ['true', 'false']:
   print "ERROR: The variable xa can be true or false"
   print "%s done" % (scriptName)
   sys.exit(-1)
else:
    if xa =='true':
        implementationType='XA data source'
    else:
        implementationType='Connection pool data source'
        
if (classpath == None) or (len(classpath.strip()) == 0):
   print "ERROR: The variable classpath is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if (name == None) or (len(name.strip()) == 0):
   print "ERROR: The variable name is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
   
if isolated.strip() not in ['true', 'false']:
   print "ERROR: The variable isolated is boolean"
   print "%s done" % (scriptName)
   sys.exit(-1)

if deleteIfExist not in [0, 1]:
   print "ERROR: The variable deleteIfExist can be 0 or 1"
   print "%s done" % (scriptName)
   sys.exit(-1)

if isinstance(webSphereVars, type([])) == 0:
   print "ERROR: The variable webSphereVars must be a list"
   print "%s done" % (scriptName)
   sys.exit(-1)

for dummy in webSphereVars:
   if isinstance(dummy, type([])) == 0 or len(dummy) != 2:
      print "ERROR: Each object of variable webSphereVars must be a list of two items"
      print "%s done" % (scriptName)
      sys.exit(-1)
     
print "Check data read done"

# Check scopeName ...
print "Check scope %s ..." % (scopeName)
#scopeGlobal=scopeName
(scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)

# Create JDBC Provider
print "Create JDBC Provider ..."
#out = checkIfResourceExist(scopeid, name ,'JDBCProvider')
#if out != None:
(resourceId , resourceName) = checkIfResourceExist(scopeid, name, "JDBCProvider")
if resourceId != None: 
   #print "JDBC Provider %s already exists " % name
   #if deleteIfExist == 1:
   #   print "Delete existing JDBC Provider: ",
   #   try:
#  #       AdminConfig.remove(out)
   #      AdminConfig.remove(resourceId)
   #      print "OK"
   #   except Exception, ex1:
   #      print   'An error has occurred %s ' %(ex1) 
   #   #except: clearExit("KO\nRollback and exit", -1)
   #else: 
   clearExit("JDBC Provider %s already exists" % name , 0)   
print "Create %s:" % (name),
try:
  # if description != None and len(description.strip()) != 0 : description = "-description '%s'" % (description)
  # if nativePath != None and len(nativePath.strip()) != 0 : nativePath = "-nativePath '%s'" % (nativePath)
   if implementationClassName != None and len(implementationClassName.strip()) != 0 : implementationClassName = "-implementationClassName '%s'" % (implementationClassName)
   if scope == 'Server':
       scopeStr = 'Node=%s,Server=%s' %(nodeName,serverName)
   else:
       scopeStr = scope + "=" + scopeName
       
   classpath = classpath.replace(";", " ") 
   print "Classpath = %s" %(classpath)
   if (databaseType.find('Informix')!=-1):
       AdminTask.createJDBCProvider("[-scope %s -databaseType %s -providerType '%s' -implementationType '%s' -name '%s' -description '%s' -classpath %s -nativePath '%s' ]" %(scopeStr,databaseType,providerType,implementationType,name,description,classpath,nativePath))
   else:
       print "AdminTask.createJDBCProvider('[-scope %s -databaseType %s -providerType '%s' -implementationType '%s' -name '%s' -description '%s' -classpath %s -nativePath '%s' ]" %(scopeStr,databaseType,providerType,implementationType,name,description,classpath,nativePath)
       AdminTask.createJDBCProvider("[-scope %s -databaseType %s -providerType '%s' -implementationType '%s' -name '%s' -description '%s' -classpath %s -nativePath '%s' ]" %(scopeStr,databaseType,providerType,implementationType,name,description,classpath,nativePath))
   print "OK"
except:
   print "KO"
   type, value, traceback = sys.exc_info() 
   print "ERROR: %s (%s)" % (str(value), type) 
   clearExit("Rollback and exit", -1)
# Modify WebSphere Variables
print "Modify WebSphere Variables:",
try:
   #(scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
   scopeRes = getStringScopeForId(scope, scopeid, scopeName, nodeName, serverName, clusterName)
   variableMap = AdminConfig.getid(scopeRes + '/VariableMap:/')
   entries = AdminConfig.showAttribute(variableMap, 'entries')
   entries = entries[1:-1].split()
   for webSphereVar in webSphereVars:
      name = webSphereVar[0]
      value = webSphereVar[1]
      if value.find('"') != -1: value = "'" + value + "'"
      elif value.find("'") != -1: value = '"' + value + '"'
      elif len(value) == 0: value = "''"      
      for prop in entries:
         symbolicName = AdminConfig.showAttribute(prop, 'symbolicName')
         if symbolicName == name: 
            AdminConfig.modify(prop, "[ ['value' " + value + "] ]")
            name = None
      if name != None:
         attr = [ ['symbolicName', name], ['value', value] ]
         AdminConfig.create('VariableSubstitutionEntry', variableMap, attr)
   print "OK"
except:
   print "KO"
   type, value, traceback = sys.exc_info()
   print traceback
   print "ERROR: %s (%s)" % (str(value), type)
   clearExit("Rollback and exit", -1)

print "Create JDBC Provider done"

syncEnv(AdminConfig.hasChanges())

# Done
print "%s V%s done" % (scriptName, version)
