#! /usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.1.0          Addedd logging 
# 1.1.0          Modify print function
# 1.0.0          Starting version


# Import

import java
from string import replace
global f, reportName


commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Variables
scriptName = "ReadSharedLibrary.py"
version = "1.2.0"
deleteIfExist="0"

log.INFO("%s V%s" % (scriptName, version))

# Command Line
argc = len(sys.argv)
if argc != 2:
   log.INFO("Usage: %s <output path> <scope> " % (scriptName))
   sys.exit(-1)
   
log.INFO("Read target data file ...")
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

log.DEBUG("outputPath = %s" %(outputPath))
log.DEBUG("inputScopeName = %s" %(inputScopeName))

#check parameter
log.INFO("Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)
   
def listSharedLib(SharedLib_list, scopeId,scName,scType):
   configurationParameters = ""
   for sharedLib in SharedLib_list.splitlines():
      if not isObjectInScope(sharedLib,scName,scType):
          continue
      sc=getScopeResources(sharedLib)
      log.INFO("SharedLib %s - ID %s" % (AdminConfig.showAttribute(sharedLib, 'name'), sharedLib)) 
      partName = AdminConfig.showAttribute(sharedLib, 'name')
      if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit",-1)
      fileName = "%s.%s.SharedLib.py" % (replace(partName, " ", "_"), replace(sc, ":", "_"))
      log.INFO("Create File %s for SharedLib %s " % (fileName, partName))
      fp = fileName
      displayList = []
      f = open(str(outputPath) + "/"+ str(fileName), "w")
      name = AdminConfig.showAttribute(sharedLib, 'name')
      classPath = AdminConfig.showAttribute(sharedLib, 'classPath')
      isolatedClassLoader = AdminConfig.showAttribute(sharedLib, 'isolatedClassLoader')
      nativePath = AdminConfig.showAttribute(sharedLib, 'nativePath')
      description = AdminConfig.showAttribute(sharedLib, 'description')
      displayList.append("scopeName='%s'" % (scName))
      displayList.append("name='%s'" % (name))
      displayList.append("classPath='%s'" % (classPath))
      if description!=None:
          displayList.append("description='%s'" % (applyApexTranslation(description)))
      else:
          displayList.append("description=''")
      
      displayList.append("isolatedClassLoader='%s'" % (isolatedClassLoader))
      displayList.append("nativePath='%s'" % (nativePath))
      displayList.append("deleteIfExist=%s" % (deleteIfExist))
      void = display(displayList, f)
      f.close()
# end def

# il nome del server quando è uguale al nome del cluster è di tipo serverTemplate
def launch(servers, nodes, clusters, cell):
   if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        SharedLib_list = AdminConfig.list('Library', cell[0])
        listSharedLib(SharedLib_list, cell[0], cellName, "cells")
   if len(servers) > 0:
      for server in servers:
         ServerName = getServerName(server)
         log.INFO("Retrieve SharedLib for server %s .. " % (ServerName))
         if checkIfIsServerTemplate(server) == False:
            nodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (nodeName, ServerName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer)
            if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
               SharedLib_list = AdminConfig.list('Library', server)
               listSharedLib(SharedLib_list, server, serverName, "servers")
         else:
             log.INFO("%s is a Dynamic Cluster Server Template " % (server))
   if len(nodes) > 0:
      for node in nodes:
         nodeName = AdminConfigShowAttribute(node, 'name')
         log.INFO("Retrieve SharedLib for Node %s .. " % nodeName)
         if not nodeIsDmgr(nodeName) and not nodeIsIHS(nodeName):
            SharedLib_list = AdminConfig.list('Library', node)
            listSharedLib(SharedLib_list, node, nodeName, 'nodes')
   if len(clusters) > 0:
      for cluster in clusters:
         ClusterName = AdminConfigShowAttribute(cluster, 'name')
         log.INFO("Retrieve SharedLib for Cluster %s .. " % ClusterName)
         SharedLib_list = AdminConfig.list('Library', cluster)
         listSharedLib(SharedLib_list,cluster,ClusterName,'clusters')

# End Def
# inizialize parameter    
cell = []
servers = []
nodes = []
clusters = []
if inputScopeName == 'ALL':
   cell=AdminConfig.list("Cell").splitlines()
   servers = AdminConfig.list('Server').splitlines()
   nodes = AdminConfig.list('Node').splitlines()
   clusters = AdminConfig.list('ServerCluster').splitlines()
   launch(servers, nodes, clusters, cell)   
elif scope == 'Cell':
   cell = [scopeid]
   launch(servers, nodes, clusters, cell)
elif scope == 'Server':
    servers = [scopeid]
    launch(servers, nodes, clusters, cell)
elif scope == 'Node':
    nodes = [scopeid]
    launch(servers, nodes, clusters, cell)
elif scope == 'ServerCluster':
    clusters = [scopeid]
    launch(servers, nodes, clusters, cell)

log.INFO("%s V%s done" % (scriptName, version))
