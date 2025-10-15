#! /usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.1.0          Modify print function
# 1.0.0          Starting version


# Import

import java
from string import replace
global f, reportName


commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
deleteIfExist="0"
# Variables
scriptName = "ReadURL.py"
version = "1.1.0"

print "%s V%s" % (scriptName, version)

# Command Line
argc = len(sys.argv)
if argc != 2:
   print "Usage: <outputPath>  <inputScopeName> "
   sys.exit(-1)
   
print "Read target data file ..."
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

print "outputPath = %s" %(outputPath)
print "inputScopeName = %s" %(inputScopeName)

#check parameter
print "Check Parameter .... "
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

   
def listURL(URL_list, scopeId):
   configurationParameters = ""
   for URL in URL_list.splitlines():
      sc=getScopeResources(URL)
      print "   URL %s - ID %s" % (AdminConfig.showAttribute(URL, 'name'), URL) 
      partName = AdminConfig.showAttribute(URL, 'name')
      if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit",-1)
      fileName = "%s.%s.URL.py" % (replace(partName, " ", "_"), replace(sc, ":", "_"))
      print "Create File %s for URL %s " % (fileName, partName)
      fp = fileName
      displayList = []
      f = open(str(outputPath) + "/"+ str(fileName), "w")
      name = AdminConfig.showAttribute(URL, 'name')
      jndiName = AdminConfig.showAttribute(URL, 'jndiName')
      provider = AdminConfig.showAttribute(URL, 'provider')
      providerName = AdminConfig.showAttribute(provider, 'name')
      spec = AdminConfig.showAttribute(URL, 'spec')     
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("name='%s'" % (name))
      displayList.append("jndiName='%s'" % (jndiName))
      displayList.append("providerName='%s'" % (providerName))
      displayList.append("spec='%s'" % (spec))
      displayList.append("deleteIfExist=%s" % (deleteIfExist))
      void = display(displayList, f)
      f.close()
# end def

def launch(servers,nodes,clusters):
    # List Urls on Servers
    
    if len(servers) > 0:
       for server in servers:
         serverName = getServerName(server)
         print "Retrieve URLs per server %s .. " % serverName
         if checkIfIsServerTemplate(server) == False:
            NodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (NodeName, serverName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer) 
            if getServerType(nodeName,serverName) != 'NODE_AGENT' and getServerType(nodeName,serverName) != 'WEB_SERVER':
               Urls_list = AdminConfig.list("URL", server)
               listURL(Urls_list, server)
    
    # List Urls on Nodes
    if len(nodes) > 0:
       for node in nodes:
          NodeName = AdminConfig.showAttribute(node, 'name')
          print "Retrieve Urls per node %s .. " % NodeName
          if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
             Urls_list = AdminConfig.list("URL", node)
             listURL(Urls_list, node)
    
    # List Urls on Cluster
    if len(clusters) > 0:
       for cluster in clusters:
          ClusterName = AdminConfig.showAttribute(cluster, 'name')
          print "Retrieve Urls per cluster %s .. " % ClusterName 
          Urls_list = AdminConfig.list("URL", cluster)
          listURL(Urls_list, cluster)
#End Def
    
if inputScopeName == 'ALL':
   servers = AdminConfig.list('Server').splitlines()
   nodes = AdminConfig.list('Node').splitlines()
   clusters = AdminConfig.list('ServerCluster').splitlines()
   launch(servers,nodes,clusters)
elif scope =='Server':
    servers = [scopeid]
    nodes = []
    clusters = []
    launch(servers,nodes,clusters)
elif scope =='Node':
    servers = []
    nodes = [scopeid]
    clusters = []
    launch(servers,nodes,clusters)
elif scope == 'ServerCluster':
    servers = []
    nodes = []
    clusters = [scopeid]
    launch(servers,nodes,clusters)

print "%s V%s done" % (scriptName, version)
