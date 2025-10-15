# Authors: Sergio Stinchi

# Version        Description
# 1.1.0          Correct Variable description
# 1.0.0          Starting version

# Import
import sys
import java
from string import replace
from time import gmtime, strftime
import time
from types import * 

scriptName = "ConfigureRuntimeTraceLevel.py"
version = "1.3.0"
log.INFO( "%s V%s" % (scriptName, version))

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))

# Auxiliary functions
def clearExit(text, status):
   if len(text): log.INFO( text)
   AdminConfig.reset()
   log.INFO( "%s done" % scriptName)
   sys.exit(status)
   return
# Command Line
argc = len(sys.argv)
if argc != 2:
   log.INFO( "Usage: %s <scope> <TraceLevel>   " % (scriptName))
   sys.exit(-1)

# Read target data file
log.INFO( "Read target data  ...")
inputScopeName = sys.argv[0]
_globaltraceString = sys.argv[1]

log.INFO( "traceStrirng = %s" % (_globaltraceString))
log.INFO( "inputScopeName = %s" % (inputScopeName))
deleteIfExist="0"

# check parameter
log.INFO( "Check Parameter .... ")
(scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)
if scope != 'Server' and scope != 'ServerCluster':
    clearExit("ERROR: the scope %s is not allowed" %(scope))

# Variables
_baseTraceString="*=info"
delay=60

tm1 = strftime("%d-%m-%Y %H.%M.%S",gmtime())
print "[%s] %s %s " %(tm1,scriptName, version)

def printStatement(msg):
       tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
       print "[%s] %s" % (tm, str(msg))
    
def customDelay(delay):
    time.sleep(delay)
  
def enableRunTimeTrace(nodeName,serverName, traceString):
  try:
     ts = AdminControl.queryNames('type=TraceService,node=%s,process=%s,*' %(nodeName,serverName))
     traceRuntime = AdminControl.getAttribute(ts,'traceRuntimeConfig')
     AdminControl.setAttribute(ts,"traceSpecification",traceString)
     objNameString = AdminControl.completeObjectName('type=TraceService,node=%s,process=%s,*' %(nodeName,serverName)) 
     AdminControl.invoke(objNameString, 'setTraceOutputToFile', ['',100,10,'BASIC'])
     printStatement("INFO: Apply RunTime Trace on node:%s for server:%s : [%s]" %(nodeName,serverName,traceString))
  except:
     printStatement("ERROR: Cannot apply runtimeTrace on node:%s for server:%s because is not Active or does not exist" %(nodeName,serverName))
#endDef

def disableRunTimeTrace(nodeName,serverName, traceString):
   try:
      ts = AdminControl.queryNames('type=TraceService,node=%s,process=%s,*' %(nodeName,serverName))
      AdminControl.setAttribute(ts,"traceSpecification",traceString)
      objNameString = AdminControl.completeObjectName('type=TraceService,node=%s,process=%s,*' %(nodeName,serverName)) 
      AdminControl.invoke(objNameString, 'setTraceOutputToFile', ['',5,10,'BASIC'])
      printStatement("INFO: Apply RunTime Trace on node:%s for server:%s : [%s]" %(nodeName,serverName,traceString))
   except: 
      printStatement("ERROR: Cannot apply runtimeTrace on node:%s for server:%s because is not Active or does not exist"  %(nodeName,serverName))
#endDef

def enableServerTrace(serverId):
    serverName = AdminConfigShowAttribute(serverId,'name')
    printStatement("Apply trace for Server: %s" %(serverName))
    nodeName = getNodeNameForServer(serverId)
    enableRunTimeTrace(nodeName,serverName,_globaltraceString)

def enableClusterTrace(clusterId):
   serverids= AdminConfig.list('ClusterMember', clusterId).splitlines()
   clsName = AdminConfigShowAttribute(clusterId,'name')
   for serverid in serverids:
       serverName = AdminConfig.showAttribute(serverid, 'memberName')
       serverNodeName = AdminConfig.showAttribute(serverid, 'nodeName')
       printStatement("Apply trace for cluster: %s : Server %s:%s" %(clsName,serverNodeName,serverName))
       enableRunTimeTrace(serverNodeName,serverName, _globaltraceString)

def restoreServerTrace(severId):
    serverName = AdminConfigShowAttribute(severId,'name')
    nodeName = getNodeNameForServer(severId)
    enableRunTimeTrace(nodeName,serverName,_baseTraceString)

def restoreClusterTrace(clusterId):
   serverids= AdminConfig.list('ClusterMember', clusterId).splitlines()
   clsName = AdminConfigShowAttribute(clusterId,'name')
   for serverid in serverids:
       serverName = AdminConfig.showAttribute(serverid, 'memberName')
       serverNodeName = AdminConfig.showAttribute(serverid, 'nodeName')
       printStatement("Apply trace for cluster: %s : Server %s:%s" %(clsName,serverNodeName,serverName))
       enableRunTimeTrace(serverNodeName,serverName, _baseTraceString)

if scope =='Server':
    serverId = scopeid
    enableServerTrace(serverId)
    printStatement ("INFO: Waiting for %s seconds before restore trace to base level" %(delay))
    customDelay(delay)
    printStatement("INFO: Restore trace to base level")
    restoreServerTrace(serverId)
if scope == 'ServerCluster':
    clusterId = scopeid
    enableClusterTrace(clusterId)
    printStatement ("INFO: Waiting for %s seconds before restore trace to base level" %(delay))
    customDelay(delay)
    printStatement("INFO: Restore trace to base level")
    restoreClusterTrace(clusterId)

log.INFO( "%s V%s terminated" % (scriptName, version))
