# Authors: Sergio Stinchi, Lorenzo Monaco

# 1.1.0          Add System Logging
# 1.0.0          Starting version

import sys
import java
from string import replace

# Variables
scriptName = "AddCustomPropertiesAS.py"
version = "1.5.0"

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


print "%s V%s" % (scriptName, version)

# Data
#ASname=""
#inputScopeName="AppSrv01"
#customProperties=[ ['pippoAttr_50', 'java.lang.String', 'pippovalue30'],['pippoAttr2', 'java.lang.String', 'pippo_value20'] ]  # [ ['traceLevel', 'java.lang.Integer', '-1'] ] ]
ActivationSpecs_list=""

# Command Line
argc = len(sys.argv)
if argc != 5:
   log.INFO( "ERROR : Parameter inserted are Incorrect: ")
   sys.exit(-1)

inputScopeName=sys.argv[0]
ASname=sys.argv[1]
customProperties=[[sys.argv[2],sys.argv[3],sys.argv[4]]]
typeCP=sys.argv[3]

    
log.INFO( "Create Custom Property For AS")
log.INFO( "inputScopeName = %s" %(inputScopeName))
log.INFO( "AS Name = %s" %(ASname))
log.INFO( "CustomProperties = %s" %(customProperties))


if typeCP not in ['java.lang.String','java.lang.Integer','java.lang.Boolean']:
    print "ERRROR: THe TYpe must be only 'java.lang.String' OR'java.lang.Integer' OR 'java.lang.Boolean'"
    clearExit(-1)
    
# Check data read
log.INFO( "Check data read ...")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

def checkIfResourceExist(scopeid, resourceName, typeObject):
    log.DEBUG( "id = %s - Name = %s , typeObject %s " % (scopeid,resourceName, typeObject))
    resourceIds = AdminConfig.list(typeObject, scopeid) 
    if len(resourceIds) == 0: 
        return None ,None
    for resourceId in resourceIds.splitlines():
       log.DEBUG( "id = %s " % (resourceId))
       if resourceId.find(resourceName + '(') != -1:
          beg = resourceId.find(resourceName + '(')
          end = resourceId.find(')', beg) + 1
          log.DEBUG( "id = %s - Name = %s  " % (resourceId ,resourceId[beg:end]) )
          return resourceId , resourceId[beg:end]
       else:
          continue
    return None , None 

def changeCustomProperties(scopeid,ASname):
    log.INFO("Begin changeCustomProperties(%s,%s)" %(scopeid,ASname))
    (resourceId , resourceName) = checkIfResourceExist(scopeid, ASname, "J2CActivationSpec")
    if resourceId != None: 
       log.INFO("Modify Activation Specification %s " %(ASname))
       resourceProperties = AdminConfig.showAttribute(resourceId, 'resourceProperties')[1:-1].split()
       try:
          for property in customProperties:
             log.INFO("   Check the property  %s " %(property))
             modified = 0
             for resourceProperty in resourceProperties: 
                search = resourceProperty[0:resourceProperty.find('(')]         
                if property[0] == search: 
                   log.INFO("      Modify Custom Property %s " %(property[0]))
                   AdminConfig.modify(resourceProperty, "[ ['value' '" + property[2] + "'] ]")
                   modified = 1
                   log.INFO("OK")
                   continue
             #end for
             if modified == 0:
               log.INFO( "      Create Custom Property %s " %(property[0]))
               attr = [ ['name', property[0]], ['value', property[2]], ['type', property[1]], ['required', 'false'] ]
               AdminConfig.create('J2EEResourceProperty', resourceId, attr)      
               log.INFO( "OK" )
       except:
          log.ERROR( "KO" )
          type, value, traceback = sys.exc_info()
          log.ERROR( " %s (%s)" % (str(value), type))
          clearExit("   KO\nRollback and exit", -1)
    else:
        log.INFO( "Activation Specification %s doesn't exist " %(ASname))
        clearExit("KO\nRollback and exit", -1)

def launch(servers, nodes, clusters, cell):
    if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        if ASname == "ALL":
            J2CActivationSpec_list = AdminConfig.list("J2CActivationSpec", cell[0])
            log.INFO(J2CActivationSpec_list)
            for ActivationSpecs in J2CActivationSpec_list.splitlines():
                partName = AdminConfig.showAttribute(ActivationSpecs, 'name')
                log.INFO("Activation Spec present in scope %s are %s" %(cell[0],partName))
                changeCustomProperties(cell[0],partName)
        else:
            log.INFO("Cange Single AS %s" %(ASname))
            changeCustomProperties(scopeid,ASname)

    # change AS Custom Properties on Servers
    if len(servers) > 0:
       for server in servers:
         ServerName = getServerName(server)
         log.INFO("Retrieve AS for server %s .. " % (ServerName))
         if checkIfIsServerTemplate(server) == False:
            NodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (NodeName, ServerName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer)
            if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
                if ASname == "ALL":
                    J2CActivationSpec_list = AdminConfig.list("J2CActivationSpec", scopeid)
                    log.INFO(J2CActivationSpec_list)
                    for ActivationSpecs in J2CActivationSpec_list.splitlines():
                        partName = AdminConfig.showAttribute(ActivationSpecs, 'name')
                        log.INFO("Activation Spec present in scope %s are %s" %(scopeid,partName))
                        changeCustomProperties(scopeid,partName)
                else:
                    log.INFO("Cange Single AS %s" %(ASname))
                    changeCustomProperties(scopeid,ASname)
    
    # change AS Custom Properties on Nodes
    if len(nodes) > 0:
       for node in nodes:
            NodeName = AdminConfig.showAttribute(node, 'name')
            log.INFO("Change AS Custom Properties  per node %s .. " % NodeName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeName)
            if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
                if ASname == "ALL":
                    J2CActivationSpec_list = AdminConfig.list("J2CActivationSpec", scopeid)
                    log.INFO(J2CActivationSpec_list)
                    for ActivationSpecs in J2CActivationSpec_list.splitlines():
                        partName = AdminConfig.showAttribute(ActivationSpecs, 'name')
                        log.INFO("Activation Spec present in scope %s are %s" %(scopeid,partName))
                        changeCustomProperties(scopeid,partName)
                else:
                    log.INFO("Cange Single AS %s" %(ASname))
                    changeCustomProperties(scopeid,ASname)

    # change AS Custom Properties on Cluster
    if len(clusters) > 0:
        for cluster in clusters:
            ClusterName = AdminConfig.showAttribute(cluster, 'name')
            log.INFO("Change AS Custom Properties for cluster %s .. " % ClusterName) 
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(ClusterName)
            if ASname == "ALL":
                J2CActivationSpec_list = AdminConfig.list("J2CActivationSpec", scopeid)
                log.INFO(J2CActivationSpec_list)
                for ActivationSpecs in J2CActivationSpec_list.splitlines():
                    partName = AdminConfig.showAttribute(ActivationSpecs, 'name')
                    log.INFO("Activation Spec present in scope %s are %s" %(scopeid,partName))
                    changeCustomProperties(scopeid,partName)
            else:
                log.INFO("Cange Single AS %s" %(ASname))
                changeCustomProperties(scopeid,ASname)


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


syncEnvDelayed(AdminConfig.hasChanges(),5)  

# end def