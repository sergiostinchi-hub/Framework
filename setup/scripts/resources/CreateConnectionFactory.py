# Authors: Sergio Stinchi

# 1.0.2          Removing mandatory for Queue Manager and changed check for resources
# 1.0.1          Patching scope definition
# 1.0.0          Starting version

import sys
import java
from string import replace

# Variables



commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))

scriptName = "createConnectionFactory.py"
version = "2.0.2"
log.setClass(scriptName)


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
log.INFO( "%s V%s" % (scriptName, version))

# Data
scopeName = ''               # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...)]
                             #            Warning: if the scope is a server and its name is not unique on the cell
                             #                     it must be used the form <Node>:<Server>
name = ''                    # mandatory [The name of the Connection Factory]     
jndiName = ''                # mandatory [The jndi of the Connection Factory]
targetClient = ''            # mandatory [Admitted values: JMS or MQ]
authenticationAlias = ''           # optional
xaRecoveryAuthAlias=''       # optional
description = ''             # optional  [A description of the Connection Factory]
provider=''                  # optional  [Read only]
optConfigurationParameters=[] # Custom Properies
deleteIfExist = 0            # 1 = delete the resource if exists

# JMS only
Type=''                      # optional  [Admitted values: queue or topic. If empty creates a generic Connection factory]
JMSbusName = ''              # mandatory [The bus of the Connection Factory]

# MQ only 
typeConnectionFactory=''     # mandatory [Admitted values: MQConnectionFactory or MQQueueConnectionFactory  
                             #            READ ONLY for JMS can have the following values: ConnectionFactory, QueueConnectionFactory or TopicConnectionFactory]
MQqueueManager =''           # optional  [The Queue Manager that hosts the Connection Factory] 
MQhostName =''               # optional  [hostname of the Queue Manager. If empty local host used]
MQport=''                    # optional  [port of the Queue Manager]
MQchannel=''                 # optional  [channel of the Queue Manager]
MQtransportType =''          # optional  [The way in which a connection is established to WebSphere MQ for this activation specification.
                             # Admitted values: BINDINGS, BINDINGS_THEN_CLIENT or CLIENT. BINDINGS_THEN_CLIENT is the default value.]
connectionNameList=''        # List of Connection name 

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
   
if (name == None) or (len(name.strip()) == 0):
   log.INFO( "ERROR: The variable name is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)

if (jndiName == None) or len(jndiName.strip()) == 0:
   log.INFO( "ERROR: The variable jndiName is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)

if (targetClient == None) or (len(targetClient.strip()) == 0):
   log.INFO( "ERROR: The variable targetClient is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)
elif targetClient.strip() != 'JMS' and targetClient.strip() != 'MQ':
   log.INFO( "ERROR: The variable targetClient has to be JMS or MQ")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)   
targetClient=targetClient.strip()   
   
if targetClient == 'JMS':
   if (JMSbusName == None) or (len(JMSbusName.strip()) == 0):
      log.INFO( "ERROR: The variable JMSbusName is mandatory")
      log.INFO( "%s done" % (scriptName))
      sys.exit(-1)
   if (Type != None) and (len(Type.strip()) != 0):
      if Type.strip() != 'queue' and Type.strip() != 'topic':
         log.INFO( "WARNING: The variable Type has to be queue or topic. Creating generic Connection Factory.")
         Type = ''
elif targetClient == 'MQ':
   if len(MQchannel) > 20:
      log.INFO( "ERROR: The variable MQchannel cannot be longer of 20 characters")
      log.INFO( "%s done" % (scriptName))
      sys.exit(-1)
      
   if (MQport != None) and len(MQport.strip()) != 0 :
      if MQport.strip().isdigit():
         if int(MQport) <=0:
            log.INFO( "WARNING: The variable MQport has to be > 0. Using default 1414")
            MQport = '1414'
      else:
         log.INFO( "WARNING: The variable MQport has to be numeric. Using default 1414")
         MQport = '1414'
   
   if (typeConnectionFactory != None) and len(typeConnectionFactory.strip()) != 0 :
      if typeConnectionFactory == 'MQConnectionFactory':
         Type='CF'
      elif typeConnectionFactory == 'MQQueueConnectionFactory':
         Type='QCF'
      else:
         log.INFO( "WARNING: The variable typeConnectionFactory has to be MQConnectionFactory or MQQueueConnectionFactory. Creating generic MQ Connection Factory.")
         Type=''

   if (MQtransportType != None) and len(MQtransportType.strip()) != 0 :
      if MQtransportType.strip() not in ['BINDINGS', 'BINDINGS_THEN_CLIENT', 'CLIENT']:
         log.INFO( "ERROR: The variable MQtransportType could be only ['BINDINGS', 'BINDINGS_THEN_CLIENT', 'CLIENT']")
         log.INFO( "%s done" % (scriptName))
         sys.exit(-1)


if deleteIfExist not in [0, 1]:
   log.INFO( "ERROR: The variable deleteIfExist can be 0 or 1")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)
   
log.INFO( "Check data read done")
# Check scopeName ...
log.INFO( "Check scope %s ..." % (scopeName))

(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)

# Create Connection Factory
log.INFO( "Create Connection Factory ...")
#out = checkIfResourceExist(scopeid, name ,'ConnectionFactory')
#if out != None:
(resourceId , resourceName) = checkIfResourceExist(scopeid, name, "ConnectionFactory")
if resourceId != None: 
   log.INFO( "Connection Factory %s already exists" % name)
   if deleteIfExist == 1:
      log.INFO( "Delete existing Connection Factory:")
      try: 
#         AdminConfig.remove(out)
         AdminConfig.remove(resourceId)
         log.INFO( "OK")
      except: clearExit("KO\nRollback and exit", -1)
   else: clearExit("", 0)   

if Type!=None and len(Type.strip()) != 0: Type = '-type %s' % (Type)
if description!=None and len(description.strip()) != 0: description = "-description '%s'" % (description)
if xaRecoveryAuthAlias!=None and len(xaRecoveryAuthAlias.strip()) != 0: xaRecoveryAuthAlias = '-xaRecoveryAuthAlias %s' % (xaRecoveryAuthAlias)
if targetClient == 'JMS':
    if authenticationAlias!=None and len(authenticationAlias.strip()) != 0: authenticationAlias = '-authDataAlias %s' % (authenticationAlias)
    log.INFO( "JMS %s: Create %s in scope %s :" % (typeConnectionFactory,name,scopeName),1)
    try:
       print" AdminTask.createSIBJMSConnectionFactory(%s, [-name %s -jndiName %s -busName %s %s %s %s %s ]" % (scopeid,name,jndiName,JMSbusName,Type,description,authenticationAlias,xaRecoveryAuthAlias)
       newCF = AdminTask.createSIBJMSConnectionFactory(scopeid, ["-name %s -jndiName %s -busName %s %s %s %s %s" % (name,jndiName,JMSbusName,Type,description,authenticationAlias,xaRecoveryAuthAlias)]) 
       print "createSIBJMSConnectionFactory == %s " %  newCF
       setupCustomProperty(newCF,optConfigurationParameters)
       log.INFO( " OK",2)
    except:
       log.INFO( " KO",2)
       type, value, traceback = sys.exc_info()
       log.INFO( "ERROR: %s (%s)" % (str(value), type))
       clearExit("Rollback and exit", -1)

elif targetClient == 'MQ':
    log.INFO( "MQ %s: Create %s in scope %s :" % (typeConnectionFactory,name,scopeName),1)
    try:
       if MQqueueManager != None and len(MQqueueManager.strip()) != 0: MQqueueManager = '-qmgrName %s' % (MQqueueManager)
       if MQhostName != None and len(MQhostName.strip()) != 0: MQhostName = '-qmgrHostname %s' % (MQhostName)
       if authenticationAlias!=None and len(authenticationAlias.strip()) != 0: authenticationAlias = '-containerAuthAlias  %s' % (authenticationAlias)
       if connectionNameList != None and len(connectionNameList.strip()) != 0: connectionNameList = '-connectionNameList %s' % (connectionNameList)
       if MQtransportType != None and len(MQtransportType.strip()) != 0 : MQtransportType = '-wmqTransportType %s' % (MQtransportType)
      # log.INFO("-scopeID %s -name %s -jndiName %s %s %s -qmgrPortNumber %s -qmgrSvrconnChannel %s            %s %s %s %s %s %s" % (scopeid,name,jndiName,MQqueueManager,MQhostName,MQport,MQchannel,Type,description,authenticationAlias,xaRecoveryAuthAlias,MQtransportType,connectionNameList))
       print "AdminTask.createWMQConnectionFactory(%s, [-name %s -jndiName %s %s %s -qmgrPortNumber %s -qmgrSvrconnChannel %s          %s %s %s %s %s %s %s)" % (scopeid,name,jndiName, MQqueueManager,MQhostName,MQport,MQchannel,Type,description,authenticationAlias,xaRecoveryAuthAlias,MQtransportType,connectionNameList,"-customProperties [ [fakeprops fakeval ] ]")                                      
       newCF=AdminTask.createWMQConnectionFactory(scopeid, ["-name %s -jndiName %s %s %s -qmgrPortNumber %s -qmgrSvrconnChannel %s          %s %s %s %s %s %s %s" % (name,jndiName, MQqueueManager,MQhostName,MQport,MQchannel,Type,description,authenticationAlias,xaRecoveryAuthAlias,MQtransportType,connectionNameList,"-customProperties [ [fakeprops fakeval ] ]")])
       print "createWMQConnectionFactory == %s " %  newCF
       setupCustomProperty(newCF,optConfigurationParameters)  
       log.INFO( " OK",2)
    except:
       log.INFO( " KO",2)
       type, value, traceback = sys.exc_info()
       log.INFO( "ERROR: %s (%s)" % (str(value), type))
       clearExit("Rollback and exit", -1)
else:
    log.INFO( "TargetClient Not in Scope , No Action can Taken")
    
syncEnv(AdminConfig.hasChanges())
log.INFO( "Create Connection Factory done")
# Done
log.INFO( "%s V%s done" % (scriptName, version))
