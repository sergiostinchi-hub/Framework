#!/usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.3.5          Add read Optional Properties
# 1.3.0          Add Read Resources at cell Level
# 1.2.0          Modify Properties name File
# 1.1.0          Add CheckDataSOurces for Server
# 1.0.0          Starting version

# Import
import sys
import java
from string import replace
global f, reportName

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))
execfile("%s/%s" % (commonPath, "Utility.py"))


# Variables
scriptName = "ReadDataSources.py"
version = "1.3.5"

log.INFO( "%s V%s" % (scriptName, version))


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
log.INFO( "inputScopeName = %s" % (inputScopeName))
deleteIfExist="0"

# check parameter
log.INFO( "Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

   
def listDataSources(DS_list, scopeId,scName,scType):
   configurationParameters = ""
   containerManagedAlias=''
   mappingConfigAlias=''
   createAuthAlias='0'
   for DS in DS_list.splitlines():
      if not isObjectInScope(DS,scName,scType):
          continue
      category = AdminConfig.showAttribute(DS, 'category')
      name = AdminConfig.showAttribute(DS, 'name')
      if category == 'default':
          log.WARNING( "Default DataSource %s not included" % (name))
          continue
      sc=getScopeResources(DS)
      partName = AdminConfig.showAttribute(DS, 'name')
      fileName = "%s/%s.%s.DS.py" % (outputPath, replace(partName, " ", "_"), replace(sc, ":", "_"))
      log.INFO( "Create File %s for Datasource %s " % (fileName,partName))
      fp = fileName
      displayList = []
      log.DEBUG("Datasource %s" %(name))
      authDataAlias = AdminConfig.showAttribute(DS, 'authDataAlias')
      log.DEBUG("authDataAlias = %s" %(authDataAlias))
      xaRecoveryAuthAlias = AdminConfig.showAttribute(DS, 'xaRecoveryAuthAlias')
      mappingModules = AdminConfig.showAttribute(DS,'mapping')
      log.DEBUG("mappingModules = %s" %(mappingModules))
      if mappingModules!=None:
         containerManagedAlias = AdminConfig.showAttribute(mappingModules, 'authDataAlias')
         mappingConfigAlias = AdminConfig.showAttribute(mappingModules, 'mappingConfigAlias')
         log.INFO("containerManagedAlias= %s" %(containerManagedAlias))
         log.INFO("mappingConfigAlias= %s" %(mappingConfigAlias))
      else:
         log.INFO("No Mapping Modules Founds")
      if authDataAlias == None:authDataAlias = ''
      if xaRecoveryAuthAlias == None:xaRecoveryAuthAlias = ''
      authMechanismPreference = AdminConfig.showAttribute(DS, 'authMechanismPreference')
      if(1==2):
           log.DEBUG("--")
      else:
          log.INFO( "Found DataSource = %s " % (DS) )
          f = open(fileName, "w")
          datasourceHelperClassname = AdminConfig.showAttribute(DS, 'datasourceHelperClassname')
         
          provider = AdminConfig.showAttribute(DS, 'provider')
          providerName = AdminConfig.showAttribute(provider, 'name')
          description = AdminConfig.showAttribute(DS, 'description')
          jndiName = AdminConfig.showAttribute(DS, 'jndiName')
          statementCacheSize = AdminConfig.showAttribute(DS, 'statementCacheSize')
          authenticationUsername = "USER_TO_CHANGE"
          authenticationPassword = "PASSWORD_TO_CHANGEE"
          authenticationDescription = "Description Authentication to change"
          displayList.append("scopeName='%s'" %(sc))
          displayList.append("name='%s'" % (name))
          displayList.append("jndiName='%s'" % (jndiName))
          displayList.append("dataStoreHelperClassName='%s'" % (datasourceHelperClassname))
          #authDataAlias = replace(authDataAlias, getDmgrNodeName() + '/', '')
          displayList.append("authenticationAlias='%s'" % (authDataAlias))
          displayList.append("containerManagedAlias='%s'" % (containerManagedAlias))
          displayList.append("mappingConfigAlias='%s'" % (mappingConfigAlias))
          displayList.append("authMechanismPreference='%s'" % (authMechanismPreference))
          displayList.append("providerName='%s'" % (providerName))
          displayList.append("authenticationUsername='%s'" % (authenticationUsername))
          displayList.append("authenticationPassword='%s'" % (authenticationPassword))
          displayList.append("authenticationDescription='%s'" % (authenticationDescription))
          if category != None:displayList.append("category='%s'" % (category))
          #xaRecoveryAuthAlias = replace(xaRecoveryAuthAlias, getDmgrNodeName() + '/', '')
          displayList.append("xaRecoveryAuthAlias='%s'" % (xaRecoveryAuthAlias))
          displayList.append("containerManagedPersistence='%s'" % ('false'))
          if description != None:displayList.append("description='%s'" % (description))
          displayList.append("statementCacheSize='%s'" % (statementCacheSize))
          providerType = getProviderType(provider)
          propertySet = AdminConfig.showAttribute(DS, 'propertySet')
          resourceProperties = AdminConfig.showAttribute(propertySet, 'resourceProperties')[1:-1].split()
          propSetMap = convertListToThreeItemHashMap(resourceProperties)
          indx =datasourceHelperClassname.find('InformixDataStoreHelper')
          log.DEBUG("providerType = %s" %(providerType) )
          log.DEBUG("dataStoreHelperClassName='%s'" % (datasourceHelperClassname))
          log.DEBUG("indx='%s'" % (indx))
          log.DEBUG( "Leggo  custom property  per DS %s " % (DS) )
          optConfigurationParameters = " [ "
          for entry in propSetMap.entrySet():
            entrKey=entry.key
            entryValue=entry.value 
            entryVal = entryValue.split("#")[0]
            entryType = entryValue.split("#")[1]
            optConfigurationParameters += " ['%s','%s','%s' ]  ," % (entrKey,entryType , entryVal) 
          optConfigurationParameters = optConfigurationParameters[0:len(optConfigurationParameters)-1]
          optConfigurationParameters += " ] "
          displayList.append("optConfigurationParameters=%s" % (optConfigurationParameters)) 
          if (providerType == 'Informix' and indx != -1):
             log.INFO("Provider di tipo INFORMIX");
             serverName = propSetMap.get('serverName').split("#")[0]
             databaseName = propSetMap.get('databaseName').split("#")[0]
             portNumber = propSetMap.get('portNumber').split("#")[0]
             ifxIFXHOST = propSetMap.get('ifxIFXHOST').split("#")[0]
             informixLockModeWait=propSetMap.get('informixLockModeWait').split("#")[0]
             configurationParameters = " [ "
             configurationParameters += " ['%s','%s','%s']  " % ("databaseName", "java.lang.String", databaseName) 
             configurationParameters += ", ['%s','%s','%s']  " % ("serverName", "java.lang.String", serverName)
             configurationParameters += ", ['%s','%s','%s']  " % ("portNumber", "java.lang.Integer", portNumber) 
             configurationParameters += ", ['%s','%s','%s']  " % ("ifxIFXHOST", "java.lang.String", ifxIFXHOST)
             configurationParameters += ", ['%s','%s','%s']  " % ("informixLockModeWait", "java.lang.Integer", informixLockModeWait)
             configurationParameters += " ] " 
             displayList.append("configurationParameters=%s" % (configurationParameters)) 
             log.DEBUG("configurationParameters=%s" % (configurationParameters));
          if (providerType == 'DB2'):
             driverType = propSetMap.get('driverType').split("#")[0]
             databaseName = propSetMap.get('databaseName').split("#")[0] 
             serverName = propSetMap.get('serverName').split("#")[0] 
             portNumber = propSetMap.get('portNumber').split("#")[0]
             configurationParameters = " [ "
             configurationParameters += " ['%s','%s','%s']  " % ("databaseName", "java.lang.String", databaseName) 
             configurationParameters += ", ['%s','%s','%s']  " % ("serverName", "java.lang.String", serverName)
             configurationParameters += ", ['%s','%s','%s']  " % ("portNumber", "java.lang.Integer", portNumber) 
             configurationParameters += ", ['%s','%s','%s']  " % ("driverType", "java.lang.Integer", driverType)
             configurationParameters += " ] " 
             displayList.append("configurationParameters=%s" % (configurationParameters)) 
          elif (providerType == 'Oracle'):
             URL = propSetMap.get('URL').split("#")[0]
             configurationParameters = "[ ['%s','%s','%s'] ] " % ("URL", "java.lang.String", URL) 
             displayList.append("configurationParameters=%s" % (configurationParameters)) 
          elif (providerType == 'Derby' and indx==-1):
             databaseName = propSetMap.get('databaseName').split("#")[0] 
             configurationParameters = "[ ['%s','%s','%s'] ] " % ("databaseName", "java.lang.String", databaseName) 
             displayList.append("configurationParameters=%s" % (configurationParameters)) 
          connectionPool = AdminConfig.showAttribute(DS, 'connectionPool')
          agedTimeout = AdminConfig.showAttribute(connectionPool, 'agedTimeout')
          connectionTimeout = AdminConfig.showAttribute(connectionPool, 'connectionTimeout')
          maxConnections = AdminConfig.showAttribute(connectionPool, 'maxConnections')
          minConnections = AdminConfig.showAttribute(connectionPool, 'minConnections')
          purgePolicy = AdminConfig.showAttribute(connectionPool, 'purgePolicy')
          reapTime = AdminConfig.showAttribute(connectionPool, 'reapTime')
          unusedTimeout = AdminConfig.showAttribute(connectionPool, 'unusedTimeout')
          displayList.append("agedTimeout='%s'" % (agedTimeout))
          displayList.append("connectionTimeout='%s'" % (connectionTimeout))
          displayList.append("maxConnections='%s'" % (maxConnections))
          displayList.append("minConnections='%s'" % (minConnections))
          displayList.append("purgePolicy='%s'" % (purgePolicy))
          displayList.append("reapTime='%s'" % (reapTime))
          displayList.append("unusedTimeout='%s'" % (unusedTimeout))
          displayList.append("deleteIfExist=%s" % (deleteIfExist))
          displayList.append("createAuthAlias=%s" % (createAuthAlias))
          void = display(displayList, f)
          f.close()
# end def



def launch(servers, nodes, clusters,cell):
    # List DataSource on CELL
    if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        DS_list = AdminConfig.list("DataSource", cell[0])
        listDataSources(DS_list, cell[0], cellName,"cells")

    # List DataSource on Servers
    if len(servers) > 0:
       for server in servers:
          serverName = getServerName(server)
          log.DEBUG( "Retrieve DataSources per server %s .. " % serverName)
          if checkIfIsServerTemplate(server) == False:
             NodeName = getNodeNameForServer(server)
             NodeServer = "%s:%s" % (NodeName, serverName)
             (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer) 
             if getServerType(nodeName,serverName) != 'NODE_AGENT' and getServerType(nodeName,serverName) != 'WEB_SERVER':
                DS_list = AdminConfig.list("DataSource", server)
                listDataSources(DS_list, server, serverName,"servers")
    
    # List DataSource on Nodes
    if len(nodes) > 0:
       for node in nodes:
          NodeName = AdminConfig.showAttribute(node, 'name')
          log.DEBUG( "Retrieve DataSource for node %s .. " % NodeName)
          if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
             DS_list = AdminConfig.list("DataSource", node)
             listDataSources(DS_list, node, NodeName,"nodes")
    
    
    # List DataSource on Cluster
    if len(clusters) > 0:
       for cluster in clusters:
          ClusterName = AdminConfig.showAttribute(cluster, 'name')
          log.DEBUG( "Retrieve DataSource for cluster %s .. " % ClusterName )
          DS_list = AdminConfig.list("DataSource", cluster)
          listDataSources(DS_list, cluster,ClusterName,"clusters")
# End Def
#inizialize parameter 
cell=[]
servers = []
nodes = []
clusters = []
if inputScopeName == 'ALL':
   cell=AdminConfig.list("Cell").splitlines()
   servers = AdminConfig.list('Server').splitlines()
   nodes = AdminConfig.list('Node').splitlines()
   clusters = AdminConfig.list('ServerCluster').splitlines()
   launch(servers, nodes, clusters,cell)
elif scope == 'Cell':
    cell=[scopeid]
    launch(servers, nodes, clusters,cell)
elif scope == 'Server':
    servers = [scopeid]
    launch(servers, nodes, clusters,cell)
elif scope == 'Node':
    nodes = [scopeid]
    launch(servers, nodes, clusters,cell)
elif scope == 'ServerCluster':
    clusters = [scopeid]
    launch(servers, nodes, clusters,cell)

log.INFO( "%s V%s done" % (scriptName, version))
