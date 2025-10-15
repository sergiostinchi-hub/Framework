# Authors: Sergio Stinchi, Lorenzo Monaco

# 1.0.0          Starting version

import sys
import java
from string import replace




commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))

# Variables
scriptName = "CreateJ2CConnectionFactory.py"
version = "1.0.0"


# Auxiliary functions
def clearExit(text, status):
   if len(text): log.INFO( text)
   AdminConfig.reset()
   log.INFO( "%s done" % scriptName)
   sys.exit(status)
   return


# Command Line
argc = len(sys.argv)
if argc != 1:
   log.INFO( "Usage: %s <target data file>" % (scriptName))
   sys.exit(-1)
        
# Start
log.setClass(scriptName)
printBasicScriptInfo("Sergio Stinchi",scriptName,version)

# Data
scopeName = ''                            # mandatory [The name of the resource scope]
                                          #            Warning: It has to be a valid Node name
J2CResourceAdapter = ''                   # mandatory [The name of the resource adapter]
name = ''                                 # mandatory [The name of the Connection Factory]     
jndiName = ''                             # mandatory [The jndi of the Connection Factory]
description = ''                          # optional  [A description of the Connection Factory]
deleteIfExist = 0                         # 1 = delete the resource if exists
Type=''                                   # optional  [Admitted values: queue or topic. If empty creates a generic Connection factory]
configurationParameters = []              # optional  [A list of all the required resources: name, value
                                          #            i.e.: [ ['URL', 'jdbc:oracle:thin:@26.2.163.221:1521:A10A'] ] ]
# Authentication Alias data
authenticationAlias = ''                  # optional  [Authentication Alias Name used for database authentication at run time
                                          #            If this attribute, authenticationUsername and authenticationPassword are all inserted the script will also create the alias if not existing]
authenticationUsername = ''               # optional  [Authentication Alias Username]
authenticationPassword = ''               # optional  [Authentication Alias Password]
authenticationDescription = ''            # optional  [Authentication Alias Description]
authMechanismPreference=''                # optional  [Specifies the authentication mechanism. Valid values are BASIC_PASSWORD for basic authentication and KERBEROS for Kerberos authentication
                                          #            Admitted values: BASIC_PASSWORD and KERBEROS]
      		 
# Read target data file
log.INFO( "Read target data file ...")
try: execfile(sys.argv[0])
except IOError, ioe:
   log.INFO( "ERROR: " + str(ioe))
   sys.exit(-1)
else: log.INFO( "Read target data file done")

# Check data read
log.INFO( "Check data read ...")

if (scopeName == None) or (len(scopeName.strip()) == 0):
   log.INFO( "ERROR: The variable scopeName is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)
   
if (J2CResourceAdapter == None) or (len(J2CResourceAdapter.strip()) == 0):
   log.INFO( "ERROR: The variable J2CResourceAdapter is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)

if (name == None) or (len(name.strip()) == 0):
   log.INFO( "ERROR: The variable name is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)

if (jndiName == None) or len(jndiName.strip()) == 0:
   log.INFO( "ERROR: The variable jndiName is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)

if (Type == None) or len(Type.strip()) == 0:
   log.INFO( "ERROR: The variable Type is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)

if deleteIfExist not in [0, 1]:
   log.INFO( "ERROR: The variable deleteIfExist can be 0 or 1")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)
   
if (authMechanismPreference != None) and len(authMechanismPreference.strip()) != 0 :
   if authMechanismPreference.strip() not in ['BASIC_PASSWORD', 'KERBEROS']:
      log.INFO( "ERROR: The variable authMechanismPreference has to be BASIC_PASSWORD or KERBEROS")
      log.INFO( "%s done" % (scriptName))
      sys.exit(-1)

log.INFO( "Check data read done")
# Check scopeName ...
log.INFO( "Check scope %s ..." % (scopeName))

cellName = getCellName()
(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
adapterId = "/Cell:%s/Node:%s/J2CResourceAdapter:%s" % (cellName, nodeName, J2CResourceAdapter)
adapterId = AdminConfig.getid(adapterId)

if len(authenticationAlias.strip()) > 0 and len(authenticationUsername.strip()) > 0 and len(authenticationPassword.strip()) > 0:
   found = 0
   jaasAliasList = AdminConfig.list('JAASAuthData').split(lineSeparator)
   for jaasAlias in jaasAliasList:
      if authenticationAlias == AdminConfig.showAttribute(jaasAlias, 'alias'):
         found = 1
         break
   if found == 0:
      log.INFO( "Create Authentication Alias %s:" % (authenticationAlias))
      security = AdminConfig.getid('/Cell:' + AdminControl.getCell() + '/Security:/')
      alias = ['alias', authenticationAlias]
      userid = ['userId', authenticationUsername]
      password = ['password', authenticationPassword]      
      if len(authenticationDescription.strip()) > 0: jaasAttrs = [alias, userid, password, ['description', authenticationDescription]]
      else: jaasAttrs = [alias, userid, password]
      AdminConfig.create('JAASAuthData', security, jaasAttrs)
      log.INFO( "OK")
else:
   log.INFO( "Authentication Alias %s already exists" % (authenticationAlias))
         
# Create J2C Connection Factory
log.INFO( "Create J2C Connection Factory ...")
(resourceId , resourceName) = checkIfResourceExist(scopeid, name, "ConnectionFactory")
if resourceId != None: 
   log.INFO( "J2C Connection Factory %s already exists" % name)
   if deleteIfExist == 1:
      log.INFO( "Delete existing J2C Connection Factory:")
      try: 
         AdminConfig.remove(resourceId)
         log.INFO( "OK")
      except: clearExit("KO\nRollback and exit", -1)
   else: clearExit("", 0)   

if description!=None and len(description.strip()) != 0: description = "-description '%s'" % (description)
if authenticationAlias!=None and len(authenticationAlias.strip()) != 0: authenticationAlias = '-authDataAlias %s' % (authenticationAlias)
try:
   J2CConnectionFactory=AdminTask.createJ2CConnectionFactory(adapterId,["-connectionFactoryInterface %s -name '%s' -jndiName '%s' %s %s" % (Type, name, jndiName, description, authenticationAlias)])   
   if len(authMechanismPreference.strip()) > 0:
      log.INFO( "Modify authMechanismPreference")
      AdminConfig.modify(J2CConnectionFactory, [['authMechanismPreference ', authMechanismPreference]])
      log.INFO( " OK")
   if len(configurationParameters) > 0:
      log.INFO( "Define resourceProperties")
      propertySet = AdminConfig.showAttribute(J2CConnectionFactory, "propertySet")
      propertyList = AdminConfig.list("J2EEResourceProperty", propertySet).splitlines()
      for parameter in configurationParameters:
         modified = 0
         myParam = parameter[0].strip()
         myValue = '%s' % (parameter[1].strip())
         for elem in propertyList:
            #log.INFO( "Attr %s - param %s" % (AdminConfig.showAttribute(elem, 'name'), myParam)	
            if (AdminConfig.showAttribute(elem, 'name') == myParam):
               attr = [['value', myValue]]
               AdminConfig.modify(elem, attr)
               modified = 1
               break
         if modified == 0:
            attr = [['name', parameter[0]], ['value', myValue]]
            AdminConfig.create('J2EEResourceProperty', propertySet, attr)

   log.INFO( "OK")
except:
   log.INFO( "KO")
   type, value, traceback = sys.exc_info()
   log.INFO( "ERROR: %s (%s)" % (str(value), type))
   clearExit("Rollback and exit", -1)

    
syncEnv(AdminConfig.hasChanges())
log.INFO( "Create Connection Factory done")
# Done
log.INFO( "%s V%s done" % (scriptName, version))
