# Author: Stinchi Sergio

# Version        Description
# 1.0.0          Starting version

# Import
import os
import sys
import re
import java
import AdminUtilities
import difflib
import time
from java.lang import System
# Start
scriptName = "setupUnrestrictedPolicyCP.py"
version = "1.2(2018-05-12)"
# Start
commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))
log.INFO("%s V%s" % (scriptName, version))

# Command Line
argc = len(sys.argv)
if argc != 1:
   log.INFO("Usage: %s <security policy path> " % (scriptName))
   sys.exit(-1)


unrestrictedPath=sys.argv[0]
unrestrictedPath=unrestrictedPath.strip()
# clearExit Variable
startt = 0
def clearExit(text, status):
   if len(text)>0: log.INFO( text )
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   log.INFO( "Elapsed Time: %.3f s" % (time.clock() - startt))
   log.INFO( "%s done" % scriptName)
   sys.exit(status)
   return

def customExit(text, status):
   if len(text): log.INFO( text )
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   log.INFO( "Elapsed Time: %.3f s" % (time.clock() - startt))
   log.INFO( "%s done" % scriptName )
   sys.exit(0)


def getVersionInfo():
    try:
        serverVersion = AdminControl.getAttribute(AdminControl.queryNames('WebSphere:*,type=Server,j2eeType=J2EEServer,name=dmgr'), 'platformVersion')
        #log.INFO( "serverVersion = %s" %serverVersion
    except:
        try: 
            serverVersion = AdminControl.getAttribute(AdminControl.queryNames('WebSphere:*,type=Server,j2eeType=J2EEServer,name=*'), 'platformVersion')
            #log.INFO( "serverVersion_1 = %s" %serverVersion
        except: 
            clearExit("ERROR during retrieve version Info", "-1")
    if serverVersion < '6.1': clearExit("ERROR: Too old version of WAS.\nThe script is compatible with WAS 6.1 and later", -1)
    return serverVersion

def convertToList( inlist ):
    outlist = []
    if (len(inlist) > 0):
       if (inlist[0] == '[' and inlist[len(inlist) - 1] == ']'):
          # Special checking when the config name contain space 
          if (inlist[1] == "\"" and inlist[len(inlist)-2] == "\""):
             clist = inlist[1:len(inlist) -1].split(")\" ")
          else:
             clist = inlist[1:len(inlist) - 1].split(" ")
          #endIf
       else:
          clist = inlist.split(java.lang.System.getProperty("line.separator"))
       #endIf
        
       for elem in clist:
           elem = elem.rstrip();
           if (len(elem) > 0):
              if (elem[0] == "\"" and elem[len(elem) -1] != "\""):
                 elem = elem+")\""
              #endIf   
              outlist.append(elem)
           #endIf
        #endFor
    #endIf    
    return outlist
#endDef



def doesDynamicClusterExist(clusterName):
   esito=''
   log.DEBUG( "doesDynamicClusterExist - clusterName= %s" %clusterName)
   dcid = AdminConfig.getid("/DynamicCluster:" + clusterName)
   if (dcid != None and dcid != ""):
      esito= "true"
   else:
      esito= "false"
   log.DEBUG( "doesDynamicClusterExist - esito= %s" %esito)
   return esito


def ifIsServertTemplateForCluster(serverId,clusterName):
     #log.INFO( " serverId = %s" %serverId
     #log.INFO( " clusterName = %s" %clusterName
     if serverId.find(clusterName+"(") != -1:
         #log.INFO(("ScopeId %s is ServerTemplate " %(serverId) 
         return 'True'
     else:
         return 'False'

def checkIfIsServerTemplate(ScopeId):
     if ScopeId.find('/dynamicclusters/') != -1:
         #log.INFO( "ScopeId %s is ServerTemplate " %(ScopeId) 
         return 'True'
     else:
         return 'False'

def getNodeNameForServer(ServerID):
   beg = ServerID.find('/nodes/') + len('/nodes/')
   end = ServerID.find('/', beg)
   out = ServerID[beg:end]    
   return  out

def ifServerIsPartOfDinamicCluster(serverID):
    esito=''
    serverName = AdminConfig.showAttribute(serverID, "name")
    #log.INFO( "SERVER: %s" %serverName
    clusterName = AdminConfig.showAttribute(serverID,"clusterName")
    #log.INFO( "clusterName =%s" %clusterName
    if clusterName==None:
       esito= None
    else:
        #log.INFO( "CluterName %s for server %s" %(clusterName,serverName)
        esito= doesDynamicClusterExist(clusterName)
        #log.INFO( "ifServerIsPartOfDinamicCluster esito Finale= %s" %esito
        return esito

def cleanJVMArguments(genericJVMArgs):
    jvmArgs = genericJVMArgs.split(" ")
    log.TRACE("jvmArgs = %s" %jvmArgs)
    cleanedjvmArgs=[]
    for jvmArg in jvmArgs:
        if jvmArg.find("jurisdictionPolicyDir")==-1:
            cleanedjvmArgs.append(jvmArg)
        log.TRACE("cleanedjvmArgsList =  %s " %cleanedjvmArgs)
        #end if
        cleanedjvmArgsStr=' '.join(cleanedjvmArgs)
    log.TRACE("cleanedjvmArgsStr = %s" %cleanedjvmArgsStr)
    return cleanedjvmArgsStr
    
def start():
    try:
        unrestrictedCommand="-Dcom.ibm.security.jurisdictionPolicyDir=%s" %unrestrictedPath
        versionInfo=getVersionInfo()
        v=versionInfo.split(".")[0]
        #log.INFO("## WebSphere Version %s ## " %v
        if v >= '8':
            dynamiClusters= AdminTask.listDynamicClusters().splitlines()
        cell = AdminConfig.list('Cell')
        cellName = AdminConfig.showAttribute(cell, 'name')
        clusters = AdminConfig.list('ServerCluster').splitlines()
        for cluster in clusters:
                clusterName=AdminConfig.showAttribute(cluster, 'name')
                if v >= '8':
                    if doesDynamicClusterExist(clusterName)=='true':
                        log.INFO( "################################################################ ")
                        log.INFO( "Setting Urestricted Policy for Dynamic Cluster " )
                        log.INFO( "################################################################ ")
                        log.INFO( " " )
                        log.INFO( "setupUnrestrictedPolicyCP:%s:" %clusterName,1)
                        log.TRACE( "ClusterName %s is dinamic" %clusterName )
                        clusterId = AdminConfig.getid('/Cell:%s/DynamicCluster:%s/'%(cellName,clusterName))  
                        log.INFO( "DC ClusterID  = %s" %clusterId)
                        genericJVMArgs= AdminTask.showJVMProperties(clusterId, '[-propertyName genericJvmArguments]')
                        cleanedjvmArgsStr = cleanJVMArguments(genericJVMArgs)
                        genericJVMArgs = cleanedjvmArgsStr + " " + unrestrictedCommand
                        servers=AdminTask.listServers().splitlines()
                        for server in servers:
                            if ifIsServertTemplateForCluster(server,clusterName) == 'True':
                               log.TRACE( "Il ServerTemplate per il cluster %s = %s " %(clusterName,server))
                               AdminTask.setJVMProperties(server, '[-genericJvmArguments "%s" ]' %genericJVMArgs)
                               log.INFO( "OK" ,2)
                    else:
                        log.INFO( " ")
                        log.INFO( "################################################################ ")
                        log.INFO( "Setting Urestricted Policy for %s members " %clusterName )
                        log.INFO( "################################################################ ")
                        log.INFO( " " )
                        members = AdminConfig.showAttribute(cluster, "members")
                        members = AdminUtilities.convertToList(members)
                        #log.INFO( "members = %s" % members
                        if len(members) > 0:
                           #log.INFO( "cluster " + clusterName + " has %s members" % (len(members)
                           for member in members:
                              serverName = AdminConfig.showAttribute(member, "memberName")
                              nodeName= AdminConfig.showAttribute(member, "nodeName")
                              str1 = "/Cell:%s/Node:%s/Server:%s" % (cellName, nodeName, serverName)
                              id = AdminConfig.getid(str1)
                              #log.INFO( "Server ID = %s" %id
                              genericJVMArgs=AdminTask.showJVMProperties('[-serverName %s -nodeName %s -propertyName genericJvmArguments]' %(serverName,nodeName))
                              #log.INFO( "Set Urestricted Policy Files Custom Properties for Server %s:%s " %(nodeName,serverName),
                              log.INFO( "setupUnrestrictedPolicyCP:%s:%s:" %(nodeName,serverName),1)
                              cleanedjvmArgsStr = cleanJVMArguments(genericJVMArgs)
                              genericJVMArgs = cleanedjvmArgsStr + " " + unrestrictedCommand
                              log.TRACE("Setting %s" %genericJVMArgs)
                              AdminTask.setJVMProperties('[-nodeName %s -serverName %s -genericJvmArguments "%s" ]' %(nodeName,serverName,genericJVMArgs))
                              log.INFO( "OK",2)
                    #end if
                #end if
        log.INFO( " " )
        log.INFO( "################################################################ ")
        log.INFO( "Setting Urestricted Policy for all Application Server")
        log.INFO( "################################################################ ")
        log.INFO( " " )
        servers = AdminTask.listServers(['-serverType', 'APPLICATION_SERVER']).splitlines()
        for server in servers:
           if v >= '8':
               esito=ifServerIsPartOfDinamicCluster(server)
           else:
               esito='false' 
           serverName = AdminConfig.showAttribute(server, "name")
           if esito=='true':
              log.INFO( "setupUnrestrictedPolicyCP:%s: Already Present" %serverName)
           else:
              serverName = AdminConfig.showAttribute(server, "name")
              nodeName= getNodeNameForServer(server)
              genericJVMArgs= AdminTask.showJVMProperties(server, '[-propertyName genericJvmArguments]')
              cleanedjvmArgsStr = cleanJVMArguments(genericJVMArgs)
              log.INFO( "setupUnrestrictedPolicyCP:%s:%s:" %(nodeName,serverName),1)
              genericJVMArgs = cleanedjvmArgsStr + " " + unrestrictedCommand
              log.TRACE("Setting %s" %genericJVMArgs)
              AdminTask.setJVMProperties('[-nodeName %s -serverName %s -genericJvmArguments "%s" ]' %(nodeName,serverName,genericJVMArgs))
              log.INFO( "OK",2)
           #end if
        #end for
    except:
        log.INFO( "KO",2)
        type, value, traceback = sys.exc_info()
        log.INFO( "ERROR: %s (%s)" % (str(value), type))


    
start()

log.INFO( "Save ...")
if AdminConfig.hasChanges() == 1:
    log.INFO( "Synchronization ...")
    AdminConfig.save()
    nodes = AdminControl.queryNames('type=NodeSync,*')
    if len(nodes) > 0:
        nodelist = nodes.split(lineSeparator)      
        for node in nodelist:
            beg = node.find('node=') + 5
            end = node.find(',', beg)
            log.INFO( "Synchronization for node \"" + node[beg:end] + "\" :",1)
            try: AdminControl.invoke(node, 'sync')
            except: log.INFO( "KO",2)
            else: log.INFO( "OK",2)
    else:
        log.INFO( "There aren't  Nodeagents running")
        log.INFO( "Synchronization done")