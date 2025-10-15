# Authors: Sergio Stinchi

# Version        Description
# 1.5.0          Changed check for resources
# 1.4.0          Deleted duplicated row for description in the JMS case
# 1.3.0          Correct method checkIfJ2CAdminObjectExist
# 1.2.0          Add scopeDestination variable
# 1.1.0          Add checkIfDestinationExist method
# 1.0.0          Starting version
# Import 
import sys 
import java 
import time
from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
  
# Variables 
scriptName = "CreateQueue.py" 
version = "1.6.0" 

skip = 'true'
skipdestination = 'true'
# Data 
scopeName = ''             # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...) ]
                           #            Warning: if the scope is a server and its name is not unique on the cell 
                           #                     it must be used the form <Node>:<Server> 
queueDestName = ''         # mandatory [The Name of Destination on Target BUS or MQ]
name = ''                  # mandatory [The name of the Queue]     
jndiName = ''              # mandatory [The jndi of the Queue]
targetClient = ''          # mandatory [Admitted values: JMS or MQ]
description = ''           # optional  [A description of the Queue]
deleteIfExist = 0          # 1 = delete the resource if exists

# JMS only
busName = ''               # mandatory [The bus of the Queue]
scopeDestinationName = ''  # mandatory [The name of the scope of the Destination Target (server or cluster) where 
                           #            the Destination is installed. If empty the scopeName will be used instead
                           #            Warning: if the scope is a server and its name is not unique on the cell 
                           #                     it must be used the form <Node>:<Server> 

# MQ only 
baseQueueManagerName=''    # optional  [The queue manager that hosts the WebSphere MQ queue]
# The following are read only at the moment, not managed here
queueManagerHost = ''
queueManagerPort = ''
serverConnectionChannelName = ''
userName = ''
useRFH2='false'


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

def convertPersistenteValue(val):
    if val=='QUEUE_DEFINED': return 'QDEF'
    if val=='PERSISTENT': return 'PERS'
    if val=='NONPERSISTENT': return 'NON'
    if val=='HIGH': return 'HIGH'
    return 'APP'    

     
# Command Line 
argc = len(sys.argv) 
if argc != 1: 
   print "Usage: %s <target data file>" % (scriptName) 
   sys.exit(-1) 
        
log.setClass(scriptName)
printBasicScriptInfo("Sergio Stinchi",scriptName,version)
  

# Read target data file 
print "Read target data file ..." 
try: execfile(sys.argv[0]) 
except IOError, ioe: 
   print "ERROR: " + str(ioe) 
   sys.exit(-1) 
else: print "Read target data file done" 
  
# Check data read 
print "Check data read ..." 
if len(scopeDestinationName) == 0: scopeDestinationName = scopeName 


if (targetClient == None) or (len(targetClient.strip()) == 0):
   print "ERROR: The variable targetClient is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)
elif targetClient.strip() != 'JMS' and targetClient.strip() != 'MQ':
   print "ERROR: The variable targetClient has to be JMS or MQ"
   print "%s done" % (scriptName)
   sys.exit(-1)   
targetClient=targetClient.strip()   
     
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

if (queueDestName == None) or len(queueDestName.strip()) == 0:
   print "ERROR: The variable queueDestName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

if targetClient == 'JMS':
   if (busName == None) or (len(busName.strip()) == 0):
      print "ERROR: The variable busName is mandatory"
      print "%s done" % (scriptName)
      sys.exit(-1)
   if (scopeDestinationName == None) or (len(scopeDestinationName.strip()) == 0):
      print "ERROR: The variable scopeDestinationName is mandatory" 
      print "%s done" % (scriptName) 
      sys.exit(-1) 

if deleteIfExist not in [0, 1]: 
   print "ERROR: The variable deleteIfExist can be 0 or 1" 
   print "%s done" % (scriptName) 
   sys.exit(-1) 
    
if useRFH2 not in ['true', 'false']: 
   print "ERROR: The variable useRFH2 can be true or false" 
   print "%s done" % (scriptName) 
   sys.exit(-1)     
    
print "Check data read done" 
  
(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
(scopeDest, scopeDestId , scopeDestName , nodeDestName, serverDestName, clusterDestName) = checkScopeName(scopeDestinationName)
# Create queue 
if targetClient == 'MQ': 
#   out = checkIfResourceExist(scopeid, name, "MQQueue") 
#   if out != None: 
   (resourceId , resourceName) = checkIfResourceExist(scopeid, name, "MQQueue")
   if resourceId != None: 
      print "MQ Queue %s already exists" % name 
      if deleteIfExist == 1: 
         print "Delete existing queue:",
         try: 
#            AdminConfig.remove(out) 
            AdminConfig.remove(resourceId) 
            print "OK" 
         except: 
            print "KO" 
            reset("Unable to delete Resource %s" % (name))
      else:
         sys.exit(0) 
   try: 
      print "Create MQ Queue %s:" % (name),
      command = "[-name %s -jndiName '%s' -queueName '%s'  -useRFH2 %s -qmgr '%s' " % (name,jndiName,queueDestName,useRFH2,baseQueueManagerName)
      if description!=None and len(description.strip()) != 0: command += " -description '%s' " % (description)
      if persistence!=None and len(persistence.strip()) != 0: command += " -persistence '%s' " % (convertPersistenteValue(persistence))
      command += "]"
      #print "command = %s" % (command)
      print "[CreateQueue.py] >>>> AdminTask.createWMQQueue('%s', %s)" % (scopeid,command)
      AdminTask.createWMQQueue(scopeid, command)
      print "OK" 
   except: 
      print "KO" 
      type, value, traceback = sys.exc_info() 
      print "ERROR: %s (%s)" % (str(value), type) 
      clearExit("Rollback and exit", -1) 
   print "Create MQ queue done" 

if targetClient == 'JMS': 
   print "Check if SIB Jms Queue Exist ...... "
   (resourceId , resourceName) = checkIfResourceExist(scopeid, name, "J2CAdminObject")
   if resourceId != None: 
      if deleteIfExist == 1: 
         skip = 'false'
         print "Queue %s already exists delete existing Queue." % name,
         try:
#            AdminTask.deleteSIBJMSQueue(out)  
            AdminConfig.remove(resourceId)  
            print "OK" 
         except:
            print "KO"
            type, value, traceback = sys.exc_info() 
            print "ERROR: %s (%s)" % (str(value), type)
      else: 
            print "JMS Queue %s already exists, skip creation " % name
   else:
       skip='false'
   print "Check if Destination Exist ...... "
   out = checkIfDestinationExist(queueDestName, busName) 
   if out != None: 
      if deleteIfExist == 1: 
         skipdestination = 'false'
         print "Destination %s already exists delete existing destination." % name,
         try: 
            AdminConfig.remove(out) 
            print "OK" 
         except:
            print "KO"
            type, value, traceback = sys.exc_info() 
            print "ERROR: %s (%s)" % (str(value), type)
      else: 
            print "Destination %s already exists, skip creation " % name
   else:
      skipdestination = 'false'

   if description!=None and len(description.strip()) != 0: description = "-description '%s'" % (description)
   if skipdestination == 'false':
      print "Create Destination %s " % (queueDestName),
      serverDestTarget = " -node %s -server %s " % (nodeDestName, serverDestName) 
      clusterDestTarget = " -cluster %s" % (clusterDestName)
      if scopeDest == 'ServerCluster': target = clusterDestTarget
      elif scopeDest == 'Server': target = serverDestTarget
      else: clearExit("No Scope defined - Rollback and exit", -1) 
      try:
         #print "AdminTask.createSIBDestination([-bus %s -name %s -type Queue %s %s -reliability ASSURED_PERSISTENT ])" % (busName, queueDestName, target, description)
         AdminTask.createSIBDestination("[-bus '%s' -name '%s' -type Queue %s %s -reliability ASSURED_PERSISTENT ]" % (busName, queueDestName, target, description))
         print "OK" 
         #if AdminConfig.hasChanges() == 1:AdminConfig.save()
      except:  
         print "KO"
         type, value, traceback = sys.exc_info() 
         print "ERROR: %s (%s)" % (str(value), type) 
         clearExit("Rollback and exit", -1)
   if skip == 'false':
      # Create Queue
      print "Create Queue %s " % (name),
      try:
         AdminTask.createSIBJMSQueue(scopeid, "[-name '%s' -jndiName '%s' -queueName '%s' %s -busName '%s']" % (name, jndiName, queueDestName, description, busName)) 
         print "OK" 
         #if AdminConfig.hasChanges() == 1:AdminConfig.save()
      except:  
         print "KO"
         type, value, traceback = sys.exc_info() 
         print "ERROR: %s (%s)" % (str(value), type) 
         clearExit("Rollback and exit", -1)

      print "Create JMS queue done" 
print "Save ..." 
syncEnv(AdminConfig.hasChanges())
 
print "%s V%s done" % (scriptName, version)
