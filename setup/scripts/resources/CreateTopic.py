# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version
# Import 
import sys 
import java 
import time
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
  
# Global variables
authors="Sergio Stinchi WebSphere Lab Services"
scriptName = "CreateTopics.py"
version = "2.0.0"
printBasicScriptInfo(authors,scriptName,version)
deleteIfExist="0"
skip = 'true'


# Data 
scopeName = ''             # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...) ]
                           #            Warning: if the scope is a server and its name is not unique on the cell 
                           #                     it must be used the form <Node>:<Server> 
TopicName = ''             # optional  [The Name of the Topic on Target BUS or MQ]
name = ''                  # mandatory [The name of the Topic]     
jndiName = ''              # mandatory [The jndi of the Topic]
targetClient = ''          # mandatory [Admitted values: JMS or MQ]
description = ''           # optional  [A description of the Topic]
deleteIfExist = 0          # 1 = delete the resource if exists
TopicSpace = ''            # mandatory [The Topic Space of the Topic]
DeliveryMode = ''          # optional  [Admitted values: Application, Persistent or Nonpersistent]

# JMS only
busName = ''               # mandatory [The bus of the Topic]

 
# Auxiliary functions 
def clearExit(text, status): 
   if len(text): print text 
   AdminConfig.reset() 
   print "%s done" % scriptName 
   sys.exit(status) 
   return 

#def checkIfTopicExist(scopeid, resourceName):
#   J2CAdminObjects = AdminTask.listSIBJMSTopics(scopeid)
#   if len(J2CAdminObjects) == 0: return None
#   for J2CAdminObject in J2CAdminObjects.splitlines():
#      name = AdminConfig.showAttribute(J2CAdminObject, 'name')
#      # print "name = %s - resourceName = %s  " % (name,resourceName) 
#      if name.find(resourceName) != -1:
#         return J2CAdminObject
#   return None   


# Command Line 
argc = len(sys.argv) 
if argc != 1: 
   log.INFO( "Usage: %s <target data file>" % (scriptName) )
   sys.exit(-1) 
        
# Start 
log.INFO( "%s V%s" % (scriptName, version) )
  

# Read target data file 
log.INFO( "Read target data file ..." )
try: execfile(sys.argv[0]) 
except IOError, ioe: 
   log.INFO( "ERROR: " + str(ioe) )
   sys.exit(-1) 
else: log.INFO( "Read target data file done" )
  
# Check data read 
log.INFO( "Check data read ..." )


if (targetClient == None) or (len(targetClient.strip()) == 0):
   log.INFO( "ERROR: The variable targetClient is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)
elif targetClient.strip() != 'JMS' and targetClient.strip() != 'MQ':
   log.INFO( "ERROR: The variable targetClient has to be JMS or MQ")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)   
targetClient=targetClient.strip()   
     
if (scopeName == None) or (len(scopeName.strip()) == 0):
   log.INFO( "ERROR: The variable scopeName is mandatory" )
   log.INFO( "%s done" % (scriptName) )
   sys.exit(-1) 

if (name == None) or (len(name.strip()) == 0):
   log.INFO( "ERROR: The variable name is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)

if (jndiName == None) or len(jndiName.strip()) == 0:
   log.INFO( "ERROR: The variable jndiName is mandatory")
   log.INFO( "%s done" % (scriptName))
   sys.exit(-1)

if targetClient == 'JMS': 
    if (TopicSpace == None) or len(TopicSpace.strip()) == 0:
        log.INFO( "ERROR: The variable TopicSpace is mandatory")
        log.INFO( "%s done" % (scriptName))
        sys.exit(-1)
    if (DeliveryMode == None) or len(DeliveryMode.strip()) == 0:
       log.INFO( "ERROR: The variable DeliveryMode is mandatory")
       log.INFO( "%s done" % (scriptName))
       sys.exit(-1)
    elif DeliveryMode.strip() != 'Application' and DeliveryMode.strip() != 'Persistent' and DeliveryMode.strip() != 'Nonpersistent':
       log.INFO( "ERROR: The variable DeliveryMode has to be Application, Persistent or Nonpersistent")
       log.INFO( "%s done" % (scriptName))
       sys.exit(-1)
    elif (busName == None) or (len(busName.strip()) == 0):
      log.INFO( "ERROR: The variable busName is mandatory")
      log.INFO( "%s done" % (scriptName))
      sys.exit(-1)
    else:
      log.INFO( "")
           
if deleteIfExist not in [0, 1]: 
   log.INFO( "ERROR: The variable deleteIfExist can be 0 or 1" )
   log.INFO( "%s done" % (scriptName) )
   sys.exit(-1) 
    
log.INFO( "Check data read done" )
  
(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
# Create Topic 
if targetClient == 'MQ': 
   log.INFO( "## CREATE MQ TOPIC ###### ")
   (resourceId , resourceName) = checkIfResourceExist(scopeid, name, "MQTopic")
   if resourceId != None: 
      log.INFO( "Topic %s already exists" % name )
      if deleteIfExist == 1: 
         log.INFO( "Delete existing Topic:")
         try: 
            AdminConfig.remove(resourceId) 
            log.INFO( "OK" )
            try: 
                log.INFO( "Create MQ Topic %s:" % (name))
                useRFH2 = 'false' 
                command = "[-name %s -jndiName %s -topicName %s  -brokerCCDurSubQueue %s  -brokerPubQmgr %s -useRFH2 false" %(name,jndiName,baseTopicName,brokerCCDurSubQueue,brokerPubQmgr)
                if description!=None and len(description.strip()) != 0: command += " -description '%s' " % (description)
                command += "]"
                log.DEBUG( "command = %s" % (command))
                log.INFO( "AdminTask.createWMQTopic('%s', '%s')" % (scopeid,command))
                AdminTask.createWMQTopic(scopeid, command)
                log.INFO( "OK" )
                syncEnv(AdminConfig.hasChanges())
            except: 
                log.INFO( "KO" )
                type, value, traceback = sys.exc_info() 
                log.INFO( "ERROR: %s (%s)" % (str(value), type) )
                clearExit("Rollback and exit", -1) 
         except: 
            log.INFO( "KO" )
            clearExit("Rollback and exit", -1)
      else: 
            log.INFO( "Topic %s already exists, skip creation " % name)
   else:
        log.INFO( "Create MQ Topic %s:" % (name))
        useRFH2 = 'false' 
        command = "[-name %s -jndiName %s -topicName %s  -brokerCCDurSubQueue %s  -brokerPubQmgr %s -useRFH2 false" %(name,jndiName,baseTopicName,brokerCCDurSubQueue,brokerPubQmgr)
        if description!=None and len(description.strip()) != 0: command += " -description '%s' " % (description)
        command += "]"
        log.DEBUG( "command = %s" % (command))
        log.DEBUG( "AdminTask.createWMQTopic('%s', '%s')" % (scopeid,command))
        AdminTask.createWMQTopic(scopeid, command)
        log.INFO( "OK" )
        syncEnv(AdminConfig.hasChanges())
                

if targetClient == 'JMS': 
   log.INFO( "## CREATE JMS TOPIC ###### ")
   if deleteIfExist == 1: skip = 'false'
   log.INFO( "Check if SIB Jms Topic Exist ...... ")
   (resourceId , resourceName) = checkIfResourceExist(scopeid, name, "J2CAdminObject")
   if resourceId != None: 
      if deleteIfExist == 1: 
         log.INFO( "Topic %s already exists delete existing Topic." % name)
         try:
            AdminConfig.remove(resourceId)  
            log.INFO( "OK" )
         except:
            log.INFO( "KO")
            type, value, traceback = sys.exc_info() 
            log.INFO( "ERROR: %s (%s)" % (str(value), type))
            clearExit("Rollback and exit", -1)
      else: 
            log.INFO( "Topic %s already exists, skip creation " % name)
           
   
   
   log.INFO( "Check if Destination Exist ...... ")
   out = checkIfDestinationExist(TopicSpace, busName) 
   if out != None: 
      if deleteIfExist == 1: 
         log.INFO( "Destination %s already exists delete existing destination." % name)
         try: 
            AdminConfig.remove(out) 
            log.INFO( "OK" )
         except:
            log.INFO( "KO")
            type, value, traceback = sys.exc_info() 
            log.INFO( "ERROR: %s (%s)" % (str(value), type))
            clearExit("Rollback and exit", -1)
      else: 
            log.INFO( "Destination %s already exists, skip creation " % name)
 

   # TO BE TESTED WITHOUT THE FOLLOWING LINE OF CODE
   #if AdminConfig.hasChanges() == 1:AdminConfig.save()
   if skip == 'false':
      log.INFO( "Create Destination %s " % (TopicName))
      if description!=None and len(description.strip()) != 0: description = "-description '%s'" % (description)
      try:
         log.DEBUG("AdminTask.createSIBDestination([-bus '%s' -name '%s' -type TopicSpace %s -reliability ASSURED_PERSISTENT ]" % (busName, TopicSpace, description))
         AdminTask.createSIBDestination("[-bus '%s' -name '%s' -type TopicSpace %s -reliability ASSURED_PERSISTENT ]" % (busName, TopicSpace, description))
         log.INFO( "OK" )
      except:  
         log.INFO( "KO")
         type, value, traceback = sys.exc_info() 
         log.INFO( "ERROR: %s (%s)" % (str(value), type) )
         clearExit("Rollback and exit", -1)
      # Create Topic
      log.INFO( "Create Topic %s " % (name))
      try:
         log.DEBUG("AdminTask.createSIBJMSTopic(scopeid, [-name '%s' -jndiName %s -topicName '%s' %s -busName '%s' -deliveryMode %s -topicSpace '%s']" % (name, jndiName, TopicName, description, busName, DeliveryMode, TopicSpace))
         AdminTask.createSIBJMSTopic(scopeid, "[-name '%s' -jndiName %s -topicName '%s' %s -busName '%s' -deliveryMode %s -topicSpace '%s']" % (name, jndiName, TopicName, description, busName, DeliveryMode, TopicSpace)) 
         log.INFO( "OK" )
         #if AdminConfig.hasChanges() == 1:AdminConfig.save()
      except:  
         log.INFO( "KO")
         type, value, traceback = sys.exc_info() 
         log.INFO( "ERROR: %s (%s)" % (str(value), type) )
         clearExit("Rollback and exit", -1)

      log.INFO( "Create JMS Topic done" )
log.INFO( "Save ..." )
syncEnv(AdminConfig.hasChanges())
log.INFO( "%s V%s done" % (scriptName, version))
