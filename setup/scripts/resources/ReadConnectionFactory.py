#! /usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.2.0          Corrected error into main
# 1.1.0          Add Read Resources at cell Level 
# 1.0.0          Starting version
# 2.0.0          Adding JMS Connection Factory createing
# 2.1.0          Disabled in this version cci connectionFctory

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))

global f, reportName
from string import replace
import java.lang.String as String



scopeName = ''       # mandatory, mandatory, the name of the scope resource (i.e: Telematico, DogTelProNode01, ...)
                     # Warning: if the scope is a server and its name is not unique on the cell
                     #          it must be used the form <Node>:<Server>
name =''
jndiName=''
authenticationAlias=''
xaRecoveryAuthAlias=''
busName=''
description=''
connectionInterface=''
host=''
qmgrType=''
queueManager=''
channel=''
port=''
provider=''
MQtransportType=''

deleteIfExist = 0    # 1 = delete the resource if exists


# Variables
scriptName = "ReadConnectionFactory.py"
version = "2.3.0"
log.setClass(scriptName)
log.TRACE( "%s V%s" % (scriptName, version))


# Command Line
argc = len(sys.argv)
if argc != 2:
   log.TRACE("Usage: %s <path output files> <scope> " % (scriptName))
   sys.exit(-1)

# Read target data file
log.TRACE( "Read target data file ...")
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

#log.TRACE( "outputPath = %s" %(outputPath)
#log.TRACE( "inputScopeName = %s" %(inputScopeName)

#check parameter
log.TRACE( "Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)


def listConnectionFactory(ConnectionFactory_list, scopeId,scName,scType):
   for ConnectionFactory in ConnectionFactory_list.splitlines():
      if not isObjectInScope(ConnectionFactory,scName,scType):
          continue
      sc=getScopeResources(ConnectionFactory)
      targetClient=''
      typeConnectionFactory=''
      connectionInterface =''
      BusName=''  
      connectionFactoryInterface=''
      rcStr = String(ConnectionFactory)
      idx = rcStr.indexOf('#CMPConnectorFactory')
      indx1 =rcStr.indexOf('#DataSource')
      if idx != -1 or indx1 != -1:
          continue
      else:
         log.INFO( "found ConnFactory = %s " % (ConnectionFactory) )
         typeConnectionFactory = getTypeName(ConnectionFactory)
         log.TRACE( "typeConnectionFactory == %s " %(typeConnectionFactory))
         if typeConnectionFactory == 'J2CConnectionFactory':
            targetClient='JMS'
            cnDef = AdminConfigShowAttribute(ConnectionFactory,'connectionDefinition')
            connectionFactoryInterface =  AdminConfigShowAttribute(cnDef,'connectionFactoryInterface')
            log.TRACE( " connectionFactoryInterface == %s for CF %s " %(connectionFactoryInterface, ConnectionFactory))
            if connectionFactoryInterface.find(".") !=-1: typeConnectionFactory = connectionFactoryInterface.split(".")[2]
            log.DEBUG( "connectionFactoryInterface = %s" %(connectionFactoryInterface))
         elif typeConnectionFactory == 'MQQueueConnectionFactory' or typeConnectionFactory == 'MQConnectionFactory':
             targetClient='MQ'
         else:
             continue
         if (connectionFactoryInterface!='javax.resource.cci.ConnectionFactory'):
             
             partName = AdminConfigShowAttribute(ConnectionFactory,'name')
             log.TRACE("%s NOT IS javax.resource.cci.ConnectionFactory " %partName)
             partName = replace(partName,"/",".")
             fileName = "%s/%s.%s.%s.py" %(outputPath,replace(partName," ","_"),replace(sc,":","_"),typeConnectionFactory)
             log.DEBUG( "filename = %s " %(fileName))
             displayList = []
             f = open(fileName,"w")
             #root properties
             propertySet = AdminConfig.showAttribute(ConnectionFactory, 'propertySet')
             #log.TRACE("propertySet = %s" % propertySet)
             if propertySet != None:
                resourceProperties = AdminConfig.showAttribute(propertySet, 'resourceProperties')[1:-1].split()
                log.TRACE("resourceProperties = %s" %resourceProperties)
                propSetMap = convertListToThreeItemHashMap(resourceProperties)
                optConfigurationParameters = "[ "
                for entry in propSetMap.entrySet():
                   entrKey=entry.key
                   entryValue=entry.value 
                   entryVal = entryValue.split("#")[0]
                   entryType = entryValue.split("#")[1]
                   if entrKey == 'BusName':
                       BusName = entryVal
                       log.DEBUG("BUS NAME == %s" % (BusName))
                   optConfigurationParameters += "['%s','%s','%s']," % (entrKey,entryType,entryVal) 
                optConfigurationParameters = optConfigurationParameters[:-1]
                optConfigurationParameters += " ] "
             else:
                optConfigurationParameters=[]
             
             #END IF PropertySet Cycle
             mapping = AdminConfigShowAttribute(ConnectionFactory,'mapping')
             authenticationAlias = AdminConfigShowAttribute(mapping,'authDataAlias')
             cp = AdminConfigShowAttribute(ConnectionFactory,'connectionPool')
             maxConnections = AdminConfigShowAttribute(cp,'maxConnections')
             minConnections = AdminConfigShowAttribute(cp,'minConnections')
             jndiName = AdminConfigShowAttribute(ConnectionFactory,'jndiName')
             name = AdminConfigShowAttribute(ConnectionFactory,'name')
             description = AdminConfigShowAttribute(ConnectionFactory,'description')  
             qmgrType = AdminConfigShowAttribute(ConnectionFactory,'qmgrType')
             host = AdminConfigShowAttribute(ConnectionFactory,'host')
             queueManager = AdminConfigShowAttribute(ConnectionFactory,'queueManager')
             channel = AdminConfigShowAttribute(ConnectionFactory,'channel')
             port = AdminConfigShowAttribute(ConnectionFactory,'port')
             provider = AdminConfigShowAttribute(ConnectionFactory,'provider')
             propSet = wsadminToList(AdminConfigShowAttribute(ConnectionFactory, 'propertySet'))
             MQtransportType=AdminConfigShowAttribute(ConnectionFactory,'transportType')
             connectionNameList = AdminConfigShowAttribute(ConnectionFactory,'connameList')
             print "1"
             xaRecoveryAuthAlias = AdminConfigShowAttribute(ConnectionFactory,'xaRecoveryAuthAlias')
             print "Check connectionDefinition"
             cnDef = AdminConfigShowAttribute(ConnectionFactory,'connectionDefinition')
             log.TRACE("connectionDefinition = %s" %cnDef)
             if len(cnDef.strip()) != 0:
                 connectionInterface =  AdminConfigShowAttribute(cnDef,'connectionInterface')
                 if connectionInterface == 'javax.jms.QueueConnection':
                    connectionInterface = 'queue'
                 elif connectionInterface == 'javax.jms.TopicConnection':
                    connectionInterface = 'topic'
                 elif connectionInterface == 'javax.jms.Connection':
                    connectionInterface = ''
             else:
                connectionInterface = ''
             displayList.append("scopeName='%s'" %(sc))
             displayList.append("name='%s'" % (name))
             displayList.append("jndiName='%s'" %(jndiName))
             displayList.append("authenticationAlias='%s'" %(authenticationAlias))
             displayList.append("xaRecoveryAuthAlias='%s'" %(xaRecoveryAuthAlias))
             displayList.append("JMSbusName='%s'" % (BusName))
             displayList.append("description='%s'" % (description))
             displayList.append("Type='%s'" %(connectionInterface))
             displayList.append("typeConnectionFactory='%s'" %(typeConnectionFactory))
             displayList.append("connectionNameList='%s'" %(connectionNameList))
             displayList.append("MQhostName='%s'" %(host))
             displayList.append("qmgrType='%s'" %(qmgrType))
             displayList.append("MQqueueManager='%s'" %(queueManager))
             displayList.append("MQchannel='%s'" %(channel))
             displayList.append("MQport='%s'" %(port))
             displayList.append("MQtransportType='%s'" %(MQtransportType))
             #displayList.append("provider='%s'" %(provider))
             displayList.append("targetClient='%s'" %(targetClient))
             displayList.append("optConfigurationParameters=%s" %(optConfigurationParameters))
             displayList.append("deleteIfExist=%s" % (deleteIfExist))
             void = display(displayList,f)
             f.close()
         else:
            log.WARNING( "ConnectionFactory %s skipped in this version" %(ConnectionFactory))
#end def

def launch(servers,nodes,clusters,cell):
     # List ConnectionFactory on CELL
    if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        ConnectionFactory_list = AdminConfig.list("ConnectionFactory", cell[0])
        listConnectionFactory(ConnectionFactory_list,cell[0], cellName,"cells")
    # List ConnectionFactory on Servers
    if len(servers) > 0:
       for server in servers:
          ServerName = getServerName(server)
          log.INFO( "Retrieve Connection Factory per server %s .. " % ServerName)
          if checkIfIsServerTemplate(server) == False:
             NodeName = getNodeNameForServer(server)
             NodeServer = "%s:%s" % (NodeName, ServerName)
             (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer)
             if getServerType(nodeName,serverName) != 'NODE_AGENT' and getServerType(nodeName,serverName) != 'WEB_SERVER': 
                ConnectionFactory_list = AdminConfig.list("ConnectionFactory", server)
                listConnectionFactory(ConnectionFactory_list, server, serverName,"servers")
    # List ConnectionFactory on Nodes
    if len(nodes) > 0:
       for node in nodes:
          NodeName = AdminConfigShowAttribute(node, 'name')
          log.INFO( "Retrieve ConnectionFactory for node %s .. " % NodeName)
          if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
             ConnectionFactory_list = AdminConfig.list('ConnectionFactory', node)
             listConnectionFactory(ConnectionFactory_list,node, NodeName,"nodes")
    # List ConnectionFactory on Cluster
    if len(clusters) > 0:
       for cluster in clusters:
          ClusterName = AdminConfigShowAttribute(cluster, 'name')
          log.INFO( "Retrieve ConnectionFactory per cluster %s .. " % ClusterName )
          ConnectionFactory_list = AdminConfig.list('ConnectionFactory',cluster)
          listConnectionFactory(ConnectionFactory_list, cluster,ClusterName,"clusters")
#End Def

# Inizialize parameter
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
elif scope =='Server':
    servers = [scopeid]
    launch(servers,nodes,clusters,cell)
elif scope =='Node':
    nodes = [scopeid]
    launch(servers,nodes,clusters,cell)
elif scope == 'ServerCluster':
    clusters = [scopeid]
    launch(servers,nodes,clusters,cell)

log.INFO( "%s V%s done" % (scriptName, version))
      
