#!/usr/bin/python
# Version        Description
# 1.5.0          Add System Logging
# 1.4.0          Add Read Resources at cell Level
# 1.2.0          Add Read Properties fro NameSpaceBinding for server
# 1.1.0          Add StringNameSpaceBinding check
# 1.0.0          Starting version

import sys
import java
from string import replace
global f, reportName


commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))


# Variables
scriptName = "ReadNameSpaceBinding.py"
version = "1.5.0"
deleteIfExist = "0"
log.INFO("%s V%s" % (scriptName, version))



# Command Line
argc = len(sys.argv)
if argc != 2:
   log.INFO("Usage: %s <path output files> <scope> " % (scriptName))
   sys.exit(-1)

# Read target data file
log.INFO("Read target data file ...")
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

log.DEBUG("outputPath = %s" % (outputPath))
log.DEBUG("inputScopeName = %s" % (inputScopeName))

# check parameter
log.INFO("Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

def getNameSpaceBingingType(nmsp_id):
    beg = nmsp_id.find('#') + 1
    end = nmsp_id.find(')', beg)
    out = nmsp_id[beg:end]    
    return out.split('_')[0]

def wasStringToList(data):
   if len(data) == 0: return []
   if data[0] == '[': data = data[1:]
   if data[-1] == ']': data = data[0:-1]
   return data.split()
   
   
def listNameSpaceBinding(NameSpaceBinding_list, scopeId, scName, scType):
   configurationParameters = ""
   for NameSpaceBinding in NameSpaceBinding_list.splitlines():
      if not isObjectInScope(NameSpaceBinding, scName, scType):
         continue 
      partName = AdminConfig.showAttribute(NameSpaceBinding, 'name')
      typeNameSpaceBinding = getNameSpaceBingingType(NameSpaceBinding)
      log.INFO("   Found %s: %s  " % (typeNameSpaceBinding,partName))
      sc = getScopeResources(NameSpaceBinding)
      partName = replace(partName, " ", "_")
      partName = replace(partName, "/", "_")
      fileName = "%s/%s.%s.NSB.py" % (outputPath, replace(partName, " ", "_"), replace(sc, ":", "_"))
      log.DEBUG("Create File %s for NameSpaceBinding %s " % (fileName, partName))
      fp = fileName
      displayList = []
      f = open(fileName, "w")
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("typeNameSpaceBinding='%s'" % (typeNameSpaceBinding))
      if typeNameSpaceBinding == "StringNameSpaceBinding":
         name = AdminConfig.showAttribute(NameSpaceBinding, 'name')
         nameInNameSpace = AdminConfig.showAttribute(NameSpaceBinding, 'nameInNameSpace')
         stringToBind = AdminConfig.showAttribute(NameSpaceBinding, 'stringToBind')
         displayList.append("name='%s'" % (name))
         displayList.append("nameInNameSpace='%s'" % (nameInNameSpace))
         displayList.append("stringToBind='%s'" % (stringToBind))
      elif typeNameSpaceBinding == "EjbNameSpaceBinding":
          applicationNodeName = AdminConfig.showAttribute(NameSpaceBinding, 'applicationNodeName')
          applicationServerName = AdminConfig.showAttribute(NameSpaceBinding, 'applicationServerName')
          bindingLocation = AdminConfig.showAttribute(NameSpaceBinding, 'bindingLocation')
          ejbJndiName = AdminConfig.showAttribute(NameSpaceBinding, 'ejbJndiName')
          name = AdminConfig.showAttribute(NameSpaceBinding, 'name')
          nameInNameSpace = AdminConfig.showAttribute(NameSpaceBinding, 'nameInNameSpace')
          if applicationNodeName != None:displayList.append("applicationNodeName='%s'" % (applicationNodeName))
          displayList.append("applicationServerName='%s'" % (applicationServerName))
          displayList.append("bindingLocation='%s'" % (bindingLocation))
          displayList.append("ejbJndiName='%s'" % (ejbJndiName))
          displayList.append("name='%s'" % (name))
          displayList.append("nameInNameSpace='%s'" % (nameInNameSpace))         
      elif typeNameSpaceBinding == "IndirectLookupNameSpaceBinding":
         initialContextFactory = AdminConfig.showAttribute(NameSpaceBinding, 'initialContextFactory')
         jndiName = AdminConfig.showAttribute(NameSpaceBinding, 'jndiName')
         name = AdminConfig.showAttribute(NameSpaceBinding, 'name')
         nameInNameSpace = AdminConfig.showAttribute(NameSpaceBinding, 'nameInNameSpace')
         providerURL = AdminConfig.showAttribute(NameSpaceBinding, 'providerURL')
         otherCtxProperties = AdminConfig.showAttribute(NameSpaceBinding, 'otherCtxProperties')
         otherCtxPropertiesStr = " [ "
         otherCtxProperties = wasStringToList(otherCtxProperties)
         for otherCtxProperty in otherCtxProperties:
             name = AdminConfig.showAttribute(otherCtxProperty, 'name')
             value = AdminConfig.showAttribute(otherCtxProperty, 'value')
             required = AdminConfig.showAttribute(otherCtxProperty, 'required')
             description = AdminConfig.showAttribute(otherCtxProperty, 'description')
             if otherCtxPropertiesStr != " [ ":
                 otherCtxPropertiesStr+=","
             otherCtxPropertiesStr += "[%s,%s,%s,%s] " % (name, value, required, description)
         otherCtxPropertiesStr += "]"
         displayList.append("initialContextFactory='%s'" % (initialContextFactory))
         displayList.append("jndiName='%s'" % (jndiName))
         displayList.append("nameInNameSpace='%s'" % (nameInNameSpace))
         displayList.append("providerURL='%s'" % (providerURL))
         displayList.append("otherCtxProperties='%s'" % (otherCtxPropertiesStr))
      elif typeNameSpaceBinding == "CORBAObjectNameSpaceBinding":
        corbanameUrl = AdminConfig.showAttribute(NameSpaceBinding, 'corbanameUrl')
        federatedContext = AdminConfig.showAttribute(NameSpaceBinding, 'federatedContext')
        name = AdminConfig.showAttribute(NameSpaceBinding, 'name')
        nameInNameSpace = AdminConfig.showAttribute(NameSpaceBinding, 'nameInNameSpace')
        displayList.append("name='%s'" % (name))
        displayList.append("nameInNameSpace='%s'" % (nameInNameSpace))
        displayList.append("corbanameUrl='%s'" % (corbanameUrl))
        displayList.append("federatedContext='%s'" % (federatedContext))

      else:
          log.ERROR( "ERROR: No Type Binding Found")
      displayList.append("deleteIfExist=%s" % (deleteIfExist))
      void = display(displayList, f)
      f.close()
# end def


def launch(servers, nodes, clusters, cell):


    if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        NameSpaceBinding_list = AdminConfig.list("NameSpaceBinding", cell[0])
        listNameSpaceBinding(NameSpaceBinding_list, cell[0], cellName, "cells")
# List NamespaceBinding on Servers
    if len(servers) > 0:
       for server in servers:
         ServerName = getServerName(server)
         log.INFO("Retrieve NameSpaceBindings for server %s .. " % (ServerName))
         if checkIfIsServerTemplate(server) == False:
            NodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (NodeName, ServerName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer)
            if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
                NameSpaceBinding_list = AdminConfig.list("NameSpaceBinding", server)
                listNameSpaceBinding(NameSpaceBinding_list, server, ServerName, "servers")
    
    # List NamespaceBinding on Nodes
    if len(nodes) > 0:
       for node in nodes:
          NodeName = AdminConfig.showAttribute(node, 'name')
          log.INFO("Retrieve NameSpaceBinding per node %s .. " % NodeName)
          if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
             NameSpaceBinding_list = AdminConfig.list("NameSpaceBinding", node)
             listNameSpaceBinding(NameSpaceBinding_list, node, NodeName, 'nodes')
    
    # List NamespaceBinding on Cluster
    if len(clusters) > 0:
       for cluster in clusters:
          ClusterName = AdminConfig.showAttribute(cluster, 'name')
          log.INFO("Retrieve NameSpaceBinding per cluster %s .. " % ClusterName) 
          NameSpaceBinding_list = AdminConfig.list("NameSpaceBinding", cluster)
          listNameSpaceBinding(NameSpaceBinding_list, cluster, ClusterName, 'clusters')
# End Def
# inizialize parameter
cell = []
servers = []
nodes = []
clusters = []
if inputScopeName == 'ALL':
   cell = AdminConfig.list("Cell").splitlines()
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

