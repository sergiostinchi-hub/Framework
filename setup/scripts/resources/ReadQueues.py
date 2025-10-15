# Authors: Sergio Stinchi

# Version        Description
# 2.2.0          Filtered Topic J2CAdminObjects
# 2.1.0          Add Read Resources at cell Level
# 2.0.0          Adding check for Dynamic Cluster
# 1.0.0          Starting version



from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

global f, reportName


scriptName = "ReadQueues.py"
version = "2.2.0"
deleteIfExist="0"
def getJ2CAdminObjectType(obj):
   try:
      adminObject=AdminConfig.showAttribute((obj),'adminObject') 
      J2CAdminObjectType=AdminConfig.showAttribute(adminObject,'adminObjectInterface')
      log.INFO( "J2CAdminObjectType: %s " % (J2CAdminObjectType))
   except:        
      J2CAdminObjectType = ''  
   return J2CAdminObjectType


log.INFO( "%s V%s" % (scriptName, version))

# Command Line
argc = len(sys.argv)
if argc != 2:
   log.INFO( "Usage: %s <path output files> <scope> " % (scriptName))
   sys.exit(-1)

# Read target data file
log.INFO( "Read target data ")
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

# print "outputPath = %s" % (outputPath)
# print "inputScopeName = %s" % (inputScopeName)

# check parameter
log.INFO( "Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)


def listSIBJMSQueue(JMSQueue_list, scopeId,scName,scType):  
   BusName = ""
   QueueName = ""
   for JMSQueue in JMSQueue_list.splitlines():
      if not isObjectInScope(JMSQueue,scName,scType):
         continue
      sc = getScopeResources(JMSQueue)
      BusName = ''
      partName = AdminConfigShowAttribute(JMSQueue, 'name')
      if getJ2CAdminObjectType(JMSQueue) == 'javax.jms.Queue':
         log.INFO( "     found JMSQueue = %s " % (partName))
      else:
         log.INFO( "     The object found = %s it is not a JMSQueue, SKIPPING" % (partName))
         continue
      out = getScopeResources(JMSQueue)
      # print "out = %s" %(out)
      (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(out)
      if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit", -1)
      fileName = "%s/%s.%s.%s.py" % (outputPath, replace(partName, " ", "_"), replace(sc, ":", "_"), getTypeName(JMSQueue))
      fp = fileName
      displayList = []
      f = open(fileName, "w")
      name = AdminConfigShowAttribute(JMSQueue, 'name')
      jndiName = AdminConfigShowAttribute(JMSQueue, 'jndiName')
      description = AdminConfigShowAttribute(JMSQueue, 'description')
      displayList.append("targetClient='%s'" % ('JMS'))
      scopeDestName = ''
      propSet = wsadminToList(AdminConfigShowAttribute(JMSQueue, 'properties'))
      for prop in propSet:
         if AdminConfigShowAttribute(prop, 'name') == 'QueueName':
            QueueName = AdminConfigShowAttribute(prop, 'value')
         if AdminConfigShowAttribute(prop, 'name') == 'BusName':
            BusName = AdminConfigShowAttribute(prop, 'value')  
      scopeDestName = getSIBBUSTarget(BusName)
      # Common value for JMS and MQ
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("name='%s'" % (name))
      displayList.append("jndiName='%s'" % (str(jndiName)))
      displayList.append("queueDestName='%s'" % (QueueName))
      displayList.append("description='%s'" % (str(description)))
      # Specific For JMS
      displayList.append("busName='%s'" % (BusName))
      displayList.append("scopeDestinationName='%s'" % (scopeDestName))
      displayList.append("deleteIfExist=%s" % (deleteIfExist))
      void = display(displayList, f)
      f.close()
# end def

def listMQQueue(MQQueue_list, scopeId,scName,scType):
   for MQQueue in MQQueue_list.splitlines():
      if not isObjectInScope(MQQueue,scName,scType):
         continue
      sc = getScopeResources(MQQueue)
      partName = AdminConfigShowAttribute(MQQueue, 'name')
      log.INFO( "     found MQQueue = %s " % (partName))
      out = getScopeResources(MQQueue)
      (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(out)
      fileName = "%s/%s.%s.%s.py" % (outputPath, replace(partName, " ", "_"), replace(sc, ":", "_"), getTypeName(MQQueue))
      displayList = []
      f = open(fileName, "w")
      queueName = AdminConfigShowAttribute(MQQueue, 'baseQueueName')
      jndiName = AdminConfigShowAttribute(MQQueue, 'jndiName')
      description = AdminConfigShowAttribute(MQQueue, 'description')
      persistence = AdminConfigShowAttribute(MQQueue, 'persistence')
      providerID = AdminConfigShowAttribute(MQQueue, 'provider')
      baseQueueManagerName = AdminConfigShowAttribute(MQQueue, 'baseQueueManagerName')
      queueManagerPort = AdminConfigShowAttribute(MQQueue, 'queueManagerPort')
      queueManagerHost = AdminConfigShowAttribute(MQQueue, 'queueManagerHost')
      serverConnectionChannelName = AdminConfigShowAttribute(MQQueue, 'serverConnectionChannelName')
      userName = AdminConfigShowAttribute(MQQueue, 'userName')
      password = AdminConfigShowAttribute(MQQueue, 'password')
      targetClient = AdminConfigShowAttribute(MQQueue, 'targetClient')
      # Common value for JMS and MQ
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("name='%s'" % (partName))
      displayList.append("jndiName='%s'" % (jndiName))
      displayList.append("targetClient='%s'" % ('MQ'))
      displayList.append("queueDestName='%s'" % (queueName))
      displayList.append("description='%s'" % (description))
      if (targetClient=='JMS'):
          displayList.append("useRFH2='true'")
      elif (targetClient=='MQ'):
          displayList.append("useRFH2='false'")
      # Specific for MQ Queue
      displayList.append("baseQueueManagerName='%s'" % (baseQueueManagerName))
      displayList.append("persistence='%s'" % (persistence))
      #displayList.append("providerID=%s" % (providerID))
      displayList.append("queueManagerHost ='%s'" % (queueManagerHost))
      displayList.append("queueManagerPort='%s'" % (queueManagerPort))
      displayList.append("serverConnectionChannelName='%s'" % (serverConnectionChannelName))
      displayList.append("userName='%s'" % (userName))
      displayList.append("deleteIfExist=%s" % (deleteIfExist))
      void = display(displayList, f)
      f.close()


# il nome del server quando è uguale al nome del cluster è di tipo serverTemplate
def launch(servers, nodes, clusters, cell):
   if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        JMSQueue_list = AdminConfig.list('J2CAdminObject', cell[0])
        listSIBJMSQueue(JMSQueue_list, cell[0], cellName, "cells")
        MQQueue_list = AdminConfig.list('MQQueue', cell[0])
        listMQQueue(MQQueue_list, cell[0], cellName, "cells")
   
   if len(servers) > 0:
      for server in servers:
         ServerName = getServerName(server)
         log.INFO("Retrieve Queue for server %s .. " % (ServerName))
         if checkIfIsServerTemplate(server) == False:
            nodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (nodeName, ServerName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer)
            if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
               JMSQueue_list = AdminConfig.list('J2CAdminObject', server)
               listSIBJMSQueue(JMSQueue_list, server, serverName, 'servers')
               MQQueue_list = AdminConfig.list('MQQueue', server)
               listMQQueue(MQQueue_list, server, serverName, 'servers')
         else:
             log.INFO(" %s is a Dynamic Cluster Server Template " % (server))
   if len(nodes) > 0:
      for node in nodes:
         nodeName = AdminConfigShowAttribute(node, 'name')
         log.INFO( "Retrieve Queue for Node %s .. " % nodeName)
         if not nodeIsDmgr(nodeName) and not nodeIsIHS(nodeName):
            JMSQueue_list = AdminConfig.list('J2CAdminObject', node)
            listSIBJMSQueue(JMSQueue_list, node, nodeName, 'nodes')
            MQQueue_list = AdminConfig.list('MQQueue', node)
            listMQQueue(MQQueue_list, node, nodeName, 'nodes')
   if len(clusters) > 0:
      for cluster in clusters:
         ClusterName = AdminConfigShowAttribute(cluster, 'name')
         log.INFO( "Retrieve Queue for Cluster %s .. " % ClusterName)
         JMSQueue_list = AdminConfig.list('J2CAdminObject', cluster)
         listSIBJMSQueue(JMSQueue_list,cluster,ClusterName,'clusters')
         MQQueue_list = AdminConfig.list('MQQueue', cluster)
         listMQQueue(MQQueue_list,cluster,ClusterName,'clusters')

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



log.INFO( "%s V%s done" % (scriptName, version))
