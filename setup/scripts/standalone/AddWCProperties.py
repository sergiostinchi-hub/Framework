#! /usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version


# Import

import java
from string import replace
global f, reportName


commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
deleteIfExist = "0"
# Variables
scriptName = "AddWCProperties.py"
version = "1.0.0"
propName = "com.ibm.ws.webcontainer.HTTPOnlyCookies"
propValue = "*"

properties = [ ['com.ibm.ws.webcontainer.HTTPOnlyCookies', '*'] ]  

print "%s V%s" % (scriptName, version)

# Command Line
argc = len(sys.argv)
if argc != 3:
   log.INFO("Usage: <ScopeName>  <WcPropertyName> <WcPropertyValue>")
   sys.exit(-1)
   
inputScopeName = sys.argv[0]
inputWcPropertyName=sys.argv[1]
inputWcPropertyValue=sys.argv[2]

log.INFO("inputScopeName = %s" % inputScopeName)


if (inputWcPropertyName == None) or (len(inputWcPropertyName.strip()) == 0):
   print "ERROR: The variable inputWcPropertyName cannot be blank or null"
   print "%s done" % (scriptName)
   sys.exit(-1)

if (inputWcPropertyValue == None) or (len(inputWcPropertyValue.strip()) == 0):
   print "ERROR: The variable inputWcPropertyValue cannot be blank or null"
   print "%s done" % (scriptName)
   sys.exit(-1)


propName= inputWcPropertyName
propValue =inputWcPropertyValue

# check parameter
log.INFO("Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

      
def applyWCProperty(propname, propvalue, serverID):
        webcontainer_id = AdminConfig.list('WebContainer', serverID)
        setCustomPropertyOnObject(webcontainer_id, propname, propvalue)
        
def launch(servers, nodes, clusters):
    if len(servers) > 0:
       log.INFO(" ----- SERVERS ----- ")
       for server in servers:
         serverName = getServerName(server)
         if checkIfIsServerTemplate(server) == False:
            NodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (NodeName, serverName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer) 
            if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
               log.INFO( "Apply WebContainer properties for server %s .. " % serverName)
               applyWCProperty(propName, propValue, server)
    
    if len(nodes) > 0:
       log.INFO(" ----- NODES ----- ")
       for node in nodes:
          nodeName = AdminConfig.showAttribute(node, 'name')
          if not nodeIsDmgr(nodeName) and not nodeIsIHS(nodeName):
            # log.INFO( "Apply WebContainer properties for servers in node %s .. " % nodeName)
            optionalParamList = ['-nodeName', nodeName]
            servers = AdminTask.listServers(optionalParamList)
            # log.INFO( "Servers are %s" %(servers))
            for server in servers.splitlines():
               serverName = getServerName(server)
               if checkIfIsServerTemplate(server) == False:
                  NodeServer = "%s:%s" % (nodeName, serverName)
                  if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
                     log.INFO( "Apply WebContainer properties for server %s  in Node %s " % (serverName,nodeName))
                     applyWCProperty(propName, propValue, server)
                     
    if len(clusters) > 0:
       log.INFO(" ----- CLUSTERS ----- ")
       for cluster in clusters:
          ClusterName = AdminConfig.showAttribute(cluster, 'name')
          member_conf_ids = AdminConfig.showAttribute(cluster, "members")
          member_conf_ids = member_conf_ids[1:-1]
          # split by space
          for member_conf_id in member_conf_ids.split():
             # Obtain server name and node name
             serverName = AdminConfig.showAttribute(member_conf_id, "memberName")
             nodeName = AdminConfig.showAttribute(member_conf_id, "nodeName")
             if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
                log.INFO("Apply WebContainer properties for %s servers in cluster %s .. " % (serverName, ClusterName))
                serverId = AdminConfig.getid('/Node:%s/Server:%s/' %(nodeName,serverName))
                applyWCProperty(propName, propValue, serverId)

    
if inputScopeName == 'ALL':
   servers = AdminConfig.list('Server').splitlines()
   nodes = AdminConfig.list('Node').splitlines()
   clusters = AdminConfig.list('ServerCluster').splitlines()
   launch(servers, nodes, clusters)
elif scope == 'Server':
    servers = [scopeid]
    nodes = []
    clusters = []
    launch(servers, nodes, clusters)
elif scope == 'Node':
    servers = []
    nodes = [scopeid]
    clusters = []
    launch(servers, nodes, clusters)
elif scope == 'ServerCluster':
    servers = []
    nodes = []
    clusters = [scopeid]
    launch(servers, nodes, clusters)

syncEnv(AdminConfig.hasChanges())

log.INFO("%s V%s done" % (scriptName, version))
