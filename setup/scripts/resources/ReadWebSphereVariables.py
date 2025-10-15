#! /usr/bin/python
# Authors: Sergio Stinchi

import java
from string import replace
global f, reportName
commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
deleteIfExist="0"


# Global variables
authors="Sergio Stinchi WebSphere Lab Services"
scriptName = "ReadWebSphereVariables.py"
version = "1.0.0"
printBasicScriptInfo(authors,scriptName,version)

# Command Line
argc = len(sys.argv)
if argc != 2:
   log.INFO("Usage: <outputPath>  <inputScopeName> ")
   sys.exit(-1)
   
log.INFO("Read target data file ...")
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

log.INFO("outputPath = %s" %(outputPath))
log.INFO("inputScopeName = %s" %(inputScopeName))

#check parameter
log.INFO("Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

   
def listWebSphereVariables(Wvars_list, scopeId):
   configurationParameters = ""
   for WVar in Wvars_list.splitlines():
      sc=getScopeResources(WVar)
      #print "   WVar %s - ID %s" % (AdminConfig.showAttribute(WVar, 'symbolicName'), WVar) 
      partName = AdminConfig.showAttribute(WVar, 'symbolicName')
      if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit",-1)
      fileName = "%s.%s.WVar.py" % (replace(partName, " ", "_"), replace(sc, ":", "_"))
      log.INFO("Create File %s for WVar %s " % (fileName, partName))
      fp = fileName
      displayList = []
      f = open(str(outputPath) + "/"+ str(fileName), "w")
      symbolicName = AdminConfig.showAttribute(WVar, "symbolicName")
      description = AdminConfig.showAttribute(WVar, "description")
      vals = AdminConfig.showAttribute(WVar, "value")
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("symbolicName='%s'" % (symbolicName))
      displayList.append("description='%s'" % (description))
      displayList.append("value='%s'" % (vals))
      void = display(displayList, f)
      f.close()
# end def

def launch(servers,nodes,clusters):
    # List WebSphere Variables on Servers
    
    if len(servers) > 0:
       for server in servers:
         serverName = getServerName(server)
         log.LINEBREAK()
         log.INFO("#############################################################")
         log.INFO("Retrieve WebSphere Variables per server %s .. " % serverName)
         log.INFO("#############################################################")
         if checkIfIsServerTemplate(server) == False:
            NodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (NodeName, serverName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer) 
            if getServerType(nodeName,serverName) != 'NODE_AGENT' and getServerType(nodeName,serverName) != 'WEB_SERVER':
               Wvars_list = AdminConfig.list("VariableSubstitutionEntry", server)
               listWebSphereVariables(Wvars_list, server)
    
    # List WebSphere Variables on Nodes
    if len(nodes) > 0:
       for node in nodes:
          NodeName = AdminConfig.showAttribute(node, 'name')
          log.LINEBREAK()
          log.INFO("#############################################################")
          log.INFO("Retrieve WebSphere Variables  per node %s .. " % NodeName)
          log.INFO("#############################################################")
          if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
             Wvars_list = AdminConfig.list("VariableSubstitutionEntry", node)
             listWebSphereVariables(Wvars_list, node)
    
    # List WebSphere Variables on Cluster
    if len(clusters) > 0:
       for cluster in clusters:
          ClusterName = AdminConfig.showAttribute(cluster, 'name')
          log.LINEBREAK()
          log.INFO("#############################################################")
          log.INFO("Retrieve WebSphere Variables  per cluster %s .. " % ClusterName )
          log.INFO("#############################################################")
          Wvars_list = AdminConfig.list("VariableSubstitutionEntry", cluster)
          listWebSphereVariables(Wvars_list, cluster)
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
