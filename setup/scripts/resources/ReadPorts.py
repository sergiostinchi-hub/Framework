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
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))

# Variables
scriptName = "ReadPorts.py"
version = "1.1.0"
deleteIfExist = "0"

log.INFO("%s V%s" % (scriptName, version))
outputPath = "."
# Command Line
# check parameter
log.INFO( "Check Parameter .... ")

# Command Line
argc = len(sys.argv)
if argc != 2:
   log.INFO( "Usage: %s <path output files> <scope> " % (scriptName))
   sys.exit(-1)

# Read target data file
log.INFO( "Read target data file ...")
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

log.INFO( "outputPath = %s" % (outputPath))
log.INFO( "inputScopeName = %s"  % (inputScopeName))

#check parameter
log.INFO( "Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)
   
def listPorts(serverEntryId,nodeName):
          log.DEBUG( " serverEntryId = %s " %(serverEntryId))
          partName = serverEntryId.split( '(', 1 )[ 0 ]
          log.DEBUG(  "System information listPorts(): Server Name : " +  partName)
          if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit", -1)
          fileName = "%s/%s.%s_%s.%s.py" % (outputPath, replace(partName, " ", "_"), nodeName , partName ,'ports')
          displayList = []
          f = open(fileName, "w")
          log.DEBUG( "Create File %s for Servers ports %s " % (fileName, partName))
          displayList = []
          NamedEndPoints = AdminConfig.list('NamedEndPoint', serverEntryId).splitlines()
          log.DEBUG( " NamedEndPoints = %s " %(NamedEndPoints))
          ListPorts = ""
          displayList.append("scopeName='%s:%s'" % (nodeName,partName))
          for namedEndPoint in NamedEndPoints:
                endPointName = AdminConfig.showAttribute(namedEndPoint, "endPointName" )
                endPoint = AdminConfig.showAttribute(namedEndPoint, "endPoint" )
                host = AdminConfig.showAttribute(endPoint, "host" )
                port = AdminConfig.showAttribute(endPoint, "port" )
                ListPorts += "['%s','%s','%s']," % (endPointName, host, port)
          ListPorts = ListPorts[0:len(ListPorts)-1]
          displayList.append("endpoints=[%s]" % (ListPorts))
          displayList.append("deleteIfExist=%s" %(deleteIfExist))
          void = display(displayList, f)
          f.close()
# end def

# il nome del server quando è uguale al nome del cluster è di tipo serverTemplate
def launch(servers, nodes, clusters, cell):
   if len(servers) > 0:
      for server in servers:
         serverName = getServerName(server)
         nodeName = getNodeNameForServer(server)
         lista = [x for x in  AdminConfig.list('ServerEntry').splitlines() if AdminConfig.showAttribute(x,'serverName') == serverName]
         for seId in lista:
            listPorts(scopeid,scopeName)
         
   if len(nodes) > 0:
      for node in nodes:
         nodeName = AdminConfigShowAttribute(node, 'name')
         if not nodeIsIHS(nodeName):
             lst = listASByNodeName(nodeName)
             for server in lst:
                 serverName = AdminConfig.showAttribute(server,'name')
                 log.INFO( "Retrieve Ports for Servers %s in Node  %s .. " % (serverName,nodeName))
                 lista = [x for x in  AdminConfig.list('ServerEntry').splitlines() if AdminConfig.showAttribute(x,'serverName') == serverName]
                 for seId in lista:
                    listPorts(seId,nodeName)
   
   if len(clusters) > 0:
      for cluster in clusters:
         serversInCluster = AdminConfig.list('ClusterMember', cluster).splitlines()
         for serverInCluster in serversInCluster:
             serverClusterName = AdminConfig.showAttribute(serverInCluster, 'memberName')
             nodeName = AdminConfig.showAttribute(serverInCluster, 'nodeName')
             log.INFO( "Retrieve ports for servers %s in Cluster %s .. " % (serverInCluster, cluster))
             lista = [x for x in  AdminConfig.list('ServerEntry').splitlines() if AdminConfig.showAttribute(x,'serverName') == serverClusterName]
             for seId in lista:
                 listPorts(seId,nodeName)
             
# inizialize parameter    
cell=[]
servers = []
nodes = []
clusters = []
if inputScopeName == 'ALL':
   servers = AdminConfig.list('ServerEntry').splitlines()
   nodes = AdminConfig.list('Node').splitlines()
   clusters = AdminConfig.list('ServerCluster').splitlines()
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

print "%s V%s done" % (scriptName, version)

