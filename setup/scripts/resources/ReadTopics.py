# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version



from string import replace

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

global f, reportName


# Global variables
authors="Sergio Stinchi WebSphere Lab Services"
scriptName = "ReadTopics.py"
version = "2.5.0"
printBasicScriptInfo(authors,scriptName,version)
deleteIfExist="0"

def getJ2CAdminObjectType(obj):
   try:
      adminObject=AdminConfig.showAttribute((obj),'adminObject') 
      J2CAdminObjectType=AdminConfig.showAttribute(adminObject,'adminObjectInterface')
      log.INFO( "J2CAdminObjectType: %s " % (J2CAdminObjectType))
   except:        
      J2CAdminObjectType = ''  
   return J2CAdminObjectType




# Command Line
argc = len(sys.argv)
if argc != 2:
   log.INFO( "Usage: %s <path output files> <scope> " % (scriptName))
   sys.exit(-1)

# Read target data file
log.INFO( "Read target data file ...")
outputPath = sys.argv[0]
inputScopeName = sys.argv[1]

# log.INFO( "outputPath = %s" % (outputPath)
# log.INFO( "inputScopeName = %s" % (inputScopeName)

# check parameter
log.INFO( "Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)


def listSIBJMSTopic(JMSTopic_list, scopeId,scName,scType):  
   BusName = ""
   TopicName = ""
   for JMSTopic in JMSTopic_list.splitlines():
      if not isObjectInScope(JMSTopic,scName,scType):
         continue
      sc = getScopeResources(JMSTopic)
      BusName = ''
      partName = AdminConfigShowAttribute(JMSTopic, 'name')
      log.INFO( " JMSTopicID = %s " %JMSTopic)
      if getJ2CAdminObjectType(JMSTopic) == 'javax.jms.Topic':
         log.INFO( "     found JMSTopic = %s " % (partName))
      else:
         log.INFO( "     The object found = %s it is not a JMSTopic, SKIPPING" % (partName))
         continue
      out = getScopeResources(JMSTopic)
      # log.INFO( "out = %s" %(out)
      (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(out)
      if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit", -1)
      fileName = "%s/%s.%s.%s.py" % (outputPath, replace(partName, " ", "_"), replace(sc, ":", "_"), getTypeName(JMSTopic))
      fp = fileName
      displayList = []
      f = open(fileName, "w")
      name = AdminConfigShowAttribute(JMSTopic, 'name')
      jndiName = AdminConfigShowAttribute(JMSTopic, 'jndiName')
      description = AdminConfigShowAttribute(JMSTopic, 'description')
      propSet = wsadminToList(AdminConfigShowAttribute(JMSTopic, 'properties'))
      for prop in propSet:
         if AdminConfigShowAttribute(prop, 'name') == 'TopicName':
            TopicName = AdminConfigShowAttribute(prop, 'value')
         if AdminConfigShowAttribute(prop, 'name') == 'BusName':
            BusName = AdminConfigShowAttribute(prop, 'value')  
         if AdminConfigShowAttribute(prop, 'name') == 'TopicSpace':
            TopicSpace = AdminConfigShowAttribute(prop, 'value')  
         if AdminConfigShowAttribute(prop, 'name') == 'DeliveryMode':
            DeliveryMode = AdminConfigShowAttribute(prop, 'value')  
      # Common value for JMS and MQ
      displayList.append("scopeName='%s'" % (sc))
      displayList.append("name='%s'" % (name))
      displayList.append("jndiName='%s'" % (str(jndiName)))
      displayList.append("TopicName='%s'" % (TopicName))
      displayList.append("description='%s'" % (str(description)))
      displayList.append("targetClient='%s'" % ('JMS'))
      displayList.append("TopicSpace='%s'" % (TopicSpace))
      displayList.append("DeliveryMode='%s'" % (DeliveryMode))
      # Specific For JMS
      displayList.append("busName='%s'" % (BusName))
      displayList.append("deleteIfExist=%s" % (deleteIfExist))
      void = display(displayList, f)
      f.close()
# end def

def listMQTopic(MQTopic_list, scopeId,scName,scType):
   for MQTopic in MQTopic_list.splitlines():
        if not isObjectInScope(MQTopic,scName,scType):
          continue
        sc = getScopeResources(MQTopic)
        partName = AdminConfigShowAttribute(MQTopic, 'name')
        log.INFO( "     found MQTopic = %s " % (partName))
        log.INFO( " MQTopic = %s " %MQTopic)
        out = getScopeResources(MQTopic)
        (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(out)
        fileName = "%s/%s.%s.%s.py" % (outputPath, replace(partName, " ", "_"), replace(sc, ":", "_"), getTypeName(MQTopic))
        displayList = []
        f = open(fileName, "w")
        name=AdminConfigShowAttribute(MQTopic,"name")
        jndiName=AdminConfigShowAttribute(MQTopic,"jndiName")
        description=AdminConfigShowAttribute(MQTopic,"description")
        CCSID=AdminConfigShowAttribute(MQTopic,"CCSID")
        baseTopicName=AdminConfigShowAttribute(MQTopic,"baseTopicName")
        brokerCCDurSubQueue=AdminConfigShowAttribute(MQTopic,"brokerCCDurSubQueue")
        brokerDurSubQueue=AdminConfigShowAttribute(MQTopic,"brokerDurSubQueue")
        brokerPubQmgr=AdminConfigShowAttribute(MQTopic,"brokerPubQmgr")
        brokerVersion=AdminConfigShowAttribute(MQTopic,"brokerVersion")
        decimalEncoding=AdminConfigShowAttribute(MQTopic,"decimalEncoding")
        expiry=AdminConfigShowAttribute(MQTopic,"expiry")
        floatingPointEncoding=AdminConfigShowAttribute(MQTopic,"floatingPointEncoding")
        integerEncoding=AdminConfigShowAttribute(MQTopic,"integerEncoding")
        messageBody=AdminConfigShowAttribute(MQTopic,"messageBody")
        mqmdMessageContext=AdminConfigShowAttribute(MQTopic,"mqmdMessageContext")
        mqmdReadEnabled=AdminConfigShowAttribute(MQTopic,"mqmdReadEnabled")
        mqmdWriteEnabled=AdminConfigShowAttribute(MQTopic,"mqmdWriteEnabled")
        multicast=AdminConfigShowAttribute(MQTopic,"multicast")
        persistence=AdminConfigShowAttribute(MQTopic,"persistence")
        priority=AdminConfigShowAttribute(MQTopic,"priority")
        provider=AdminConfigShowAttribute(MQTopic,"provider")
        readAhead=AdminConfigShowAttribute(MQTopic,"readAhead")
        readAheadClose=AdminConfigShowAttribute(MQTopic,"readAheadClose")
        receiveCCSID=AdminConfigShowAttribute(MQTopic,"receiveCCSID")
        receiveConvert=AdminConfigShowAttribute(MQTopic,"receiveConvert")
        replyToStyle=AdminConfigShowAttribute(MQTopic,"replyToStyle")
        sendAsync=AdminConfigShowAttribute(MQTopic,"sendAsync")
        specifiedExpiry=AdminConfigShowAttribute(MQTopic,"specifiedExpiry")
        specifiedPriority=AdminConfigShowAttribute(MQTopic,"specifiedPriority")
        useNativeEncoding=AdminConfigShowAttribute(MQTopic,"useNativeEncoding")
        wildcardFormat=AdminConfigShowAttribute(MQTopic,"wildcardFormat")
      
      # Common value for JMS and MQ
        displayList.append("scopeName='%s'" % (sc))
        displayList.append("name='%s'" % (partName))
        displayList.append("jndiName='%s'" % (jndiName))
        displayList.append("description='%s'" % (description))
        displayList.append("targetClient='%s'" % ('MQ'))
        # Specific for MQ Topic
        displayList.append("CCSID='%s'" % (CCSID))
        displayList.append("baseTopicName='%s'" % (baseTopicName))
        displayList.append("brokerCCDurSubQueue='%s'" % (brokerCCDurSubQueue))
        displayList.append("brokerDurSubQueue='%s'" % (brokerDurSubQueue))
        displayList.append("brokerPubQmgr='%s'" % (brokerPubQmgr))
        displayList.append("brokerVersion='%s'" % (brokerVersion))
        displayList.append("decimalEncoding='%s'" % (decimalEncoding))
        displayList.append("expiry='%s'" % (expiry))
        displayList.append("floatingPointEncoding='%s'" % (floatingPointEncoding))
        displayList.append("integerEncoding='%s'" % (integerEncoding))
        displayList.append("messageBody='%s'" % (messageBody))
        displayList.append("mqmdMessageContext='%s'" % (mqmdMessageContext))
        displayList.append("mqmdReadEnabled='%s'" % (mqmdReadEnabled))
        displayList.append("mqmdWriteEnabled='%s'" % (mqmdWriteEnabled))
        displayList.append("multicast='%s'" % (multicast))
        displayList.append("persistence='%s'" % (persistence))
        displayList.append("priority='%s'" % (priority))
        displayList.append("provider='%s'" % (provider))
        displayList.append("readAhead='%s'" % (readAhead))
        displayList.append("readAheadClose='%s'" % (readAheadClose))
        displayList.append("receiveCCSID='%s'" % (receiveCCSID))
        displayList.append("receiveConvert='%s'" % (receiveConvert))
        displayList.append("replyToStyle='%s'" % (replyToStyle))
        displayList.append("sendAsync='%s'" % (sendAsync))
        displayList.append("specifiedExpiry='%s'" % (specifiedExpiry))
        displayList.append("specifiedPriority='%s'" % (specifiedPriority))
        displayList.append("useNativeEncoding='%s'" % (useNativeEncoding))
        displayList.append("wildcardFormat='%s'" % (wildcardFormat))
        displayList.append("deleteIfExist=%s" % (deleteIfExist))
        void = display(displayList, f)
        f.close()


# il nome del server quando è uguale al nome del cluster è di tipo serverTemplate
def launch(servers, nodes, clusters, cell):
   if len(cell) > 0:
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        JMSTopic_list = AdminConfig.list('J2CAdminObject', cell[0])
        listSIBJMSTopic(JMSTopic_list, cell[0], cellName, "cells")
        MQTopic_list = AdminConfig.list('MQTopic', cell[0])
        listMQTopic(MQTopic_list, cell[0], cellName, "cells")
   
   if len(servers) > 0:
      for server in servers:
         ServerName = getServerName(server)
         log.INFO( "Retrieve Topic for server %s .. " % (ServerName))
         if checkIfIsServerTemplate(server) == False:
            nodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (nodeName, ServerName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer)
            if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
               JMSTopic_list = AdminConfig.list('J2CAdminObject', server)
               listSIBJMSTopic(JMSTopic_list, server, serverName, 'servers')
               MQTopic_list = AdminConfig.list('MQTopic', server)
               listMQTopic(MQTopic_list, server, serverName, 'servers')
         else:
             log.INFO( " %s is a Dynamic Cluster Server Template " % (server))
   if len(nodes) > 0:
      for node in nodes:
         nodeName = AdminConfigShowAttribute(node, 'name')
         log.INFO( "Retrieve Topic for Node %s .. " % nodeName)
         if not nodeIsDmgr(nodeName) and not nodeIsIHS(nodeName):
            JMSTopic_list = AdminConfig.list('J2CAdminObject', node)
            listSIBJMSTopic(JMSTopic_list, node, nodeName, 'nodes')
            MQTopic_list = AdminConfig.list('MQTopic', node)
            listMQTopic(MQTopic_list, node, nodeName, 'nodes')
   if len(clusters) > 0:
      for cluster in clusters:
         ClusterName = AdminConfigShowAttribute(cluster, 'name')
         log.INFO( "Retrieve Topic for Cluster %s .. " % ClusterName)
         JMSTopic_list = AdminConfig.list('J2CAdminObject', cluster)
         listSIBJMSTopic(JMSTopic_list,cluster,ClusterName,'clusters')
         MQTopic_list = AdminConfig.list('MQTopic', cluster)
         listMQTopic(MQTopic_list,cluster,ClusterName,'clusters')

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
