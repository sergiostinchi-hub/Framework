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
scriptName = "ListAllMembers.py"
version = "1.0.0"


log.INFO("%s V%s" % (scriptName, version))
def launch(servers, nodes, clusters, cell):
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        print "########  CELL ########## "
        print " %s " %cellName
        print "     "
        print "######## NODES ########## "
        for node in nodes:
            nodeName = AdminConfigShowAttribute(node, 'name')
            print "... %s" %nodeName
            
        print "    "
        
        print "######## CLUSTERS ####### "
        for cluster in clusters:
           clusterName = AdminConfigShowAttribute(cluster, 'name')
           print "... %s" %clusterName
           serverids = AdminConfig.list('ClusterMember', cluster).splitlines()
           for serverid in serverids:
              server = AdminConfig.showAttribute(serverid, 'memberName')
              print "...... %s" %server
        print "    "
        
        print "######## SINGLE SERVERS ######## "
        for server in servers:
            if (not checkIfIsServerTemplate(server)):
                nodeName = getNodeNameForServer(server)
                serverName = getServerName(server)
                clusterName = AdminConfig.showAttribute(server,'clusterName')
                if clusterName== None or len(clusterName) == 0:
                    print "... %s:%s  " %(nodeName,serverName)
        print "    "
        print " END Topopogy List"

# inizialize parameter    
cell=[]
servers = []
nodes = []
clusters = []
cell=AdminConfig.list("Cell").splitlines()
servers = AdminTask.listServers('[-serverType APPLICATION_SERVER ]').splitlines()
nodes = AdminConfig.list('Node').splitlines()
clusters = AdminConfig.list('ServerCluster').splitlines()
launch(servers, nodes, clusters, cell)   

print "%s V%s done" % (scriptName, version)

