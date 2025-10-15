#! /usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.5.0          Added logging 
# 1.4.0          Added WebSphere Variable Management
# 1.3.0          Managed provider type when it finishes with " XA)" in addition to " (XA)"
# 1.2.0          Add Read Resources at cell Level
# 1.1.0          Modify print function
# 1.0.0          Starting version


# Import

import java
from string import replace
import java.lang.String as String
global f, reportName


commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Variables
scriptName = "ReadJDBCProvider.py"
version = "1.5.0"
deleteIfExist="0"



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

#check parameter
log.INFO("Check Parameter .... ")
if inputScopeName != 'ALL':
   (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(inputScopeName)

# Auxiliary functions
def clearExit(text, status):
   if len(text): log.INFO(text)
   AdminConfig.reset()
   log.INFO("%s done" % scriptName)
   sys.exit(status)
   return

def listJDBCProvider(JDBCProv_list, scopeId,scName,scType):
   #FIX 1.5.
   variable=''
   configurationParameters = ""
   for JDBCProv in JDBCProv_list.splitlines():
      rcStr = String(JDBCProv)
      idx = rcStr.indexOf('#builtin_jdbcprovider')
      if idx != -1:
         # print "JDBC Provider %s not included" %(AdminConfigShowAttribute(JDBCProv, 'name'))
          continue
      else:
          if not isObjectInScope(JDBCProv,scName,scType):
             continue
          sc=getScopeResources(JDBCProv)
          log.INFO("Found JDBCProvider = %s " % (JDBCProv))
          partName = AdminConfigShowAttribute(JDBCProv, 'name')
          scopeName = AdminConfigShowAttribute(scopeId, 'name')    
          log.DEBUG("scopeName = %s " %(scopeName) )
          if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit",-1)
          pName = replace(partName, " ", "_")
          pName = replace(pName, "(", "")
          pName = replace(pName, ")", "")
          pScopeName =replace(sc, ":", "_")
          fileName = "%s.%s.JDBCProvider.py" % (pName, pScopeName)
          log.DEBUG("Create File %s for JDBCProv %s " % (fileName, partName))
          fp = fileName
          displayList = []
          f = open(str(outputPath) + "/"+ str(fileName), "w")
          classpath=AdminConfigShowAttribute(JDBCProv,'classpath')
          print "read classpath=%s" %(classpath)
          description=AdminConfigShowAttribute(JDBCProv,'description')
          implementationClassName=AdminConfigShowAttribute(JDBCProv,'implementationClassName')
          isolated=AdminConfigShowAttribute(JDBCProv,'isolatedClassLoader')
          name=AdminConfigShowAttribute(JDBCProv,'name')
          nativepath=AdminConfigShowAttribute(JDBCProv,'nativepath')
          providerType=AdminConfigShowAttribute(JDBCProv,'providerType')
          if providerType.find(" (XA)") !=-1: 
             providerType = providerType.split(" (XA)")[0]
          elif providerType.find(" XA)") !=-1: 
             providerType = providerType.split(" XA)")[0] + ")"
          xa=AdminConfigShowAttribute(JDBCProv,'xa')
          webSphereVars=[]
          databaseType = getProviderType(JDBCProv)     
          displayList.append("scopeName='%s'" % (sc))
          displayList.append("classpath='[%s]'" % (classpath))
          displayList.append("description='%s'" % (description))
          displayList.append("implementationClassName='%s'" % (implementationClassName))
          displayList.append("isolated='%s'" % (isolated))
          displayList.append("name='%s'" % (name))
          displayList.append("nativePath='%s'" % (nativepath))
          displayList.append("providerType='%s'" % (providerType))
          displayList.append("databaseType='%s'" % (databaseType))
          displayList.append("xa='%s'" % (xa))
          beg = classpath.find('${')
          if beg!=-1:
             end = classpath.find('}', beg)
             variable = classpath[beg:end + 1]
          WebSphereVarsList = AdminConfig.list('VariableSubstitutionEntry', scopeId)
          for var in WebSphereVarsList.splitlines():
              sn = AdminConfig.showAttribute(var,'symbolicName')
              variable = replace(variable, "${", "") 
              variable = replace(variable, "}", "")
              #print "sn  %s  > variable = %s" %(sn,variable)
              if  sn == variable:
                    value = AdminConfig.showAttribute(var,'value')
                    log.DEBUG("Variable found >> %s with value %s for scope %s" %(variable,value,scType + "/" + scName + "|"))
                    index = var.find(scType + "/" + scName + "|")
                    log.DEBUG("Index = %s " %(index))
                    if index!= -1:
                       lst=[]
                       lst.append(variable)
                       lst.append(value)
                       webSphereVars.append(lst)
          displayList.append("webSphereVars=%s " % (webSphereVars))
          displayList.append("deleteIfExist=%s" % (deleteIfExist))
          void = display(displayList, f)
          f.close()
# end def

def launch(servers,nodes,clusters,cells):
   if len(cells) > 0:
        log.INFO("Retrieve JDBC Provider per cell %s .. " % cells[0])
        cellName = AdminConfig.showAttribute(cells[0], 'name')
        JDBCProvs_list = AdminConfig.list("JDBCProvider", cells[0])
        listJDBCProvider(JDBCProvs_list,cells[0], cellName,"cells")
   # List JDBCProvider on Servers
   if len(servers) > 0:
      for server in servers:
        ServerName = getServerName(server)
        log.INFO("Retrieve JDBC Provider per server %s .. " % ServerName)
        if checkIfIsServerTemplate(server) == False:
           NodeName = getNodeNameForServer(server)
           NodeServer = "%s:%s" % (NodeName, ServerName)
           (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer) 
           if getServerType(nodeName,serverName) != 'NODE_AGENT' and getServerType(nodeName,serverName) != 'WEB_SERVER':
              JDBCProvs_list = AdminConfig.list("JDBCProvider", server)
              listJDBCProvider(JDBCProvs_list, server, ServerName,"servers")
   # List JDBCProvider on Nodes
   if len(nodes) > 0:
      for node in nodes:
         NodeName = AdminConfigShowAttribute(node, 'name')
         log.INFO("Retrieve JDBCProvider for node %s .. " % NodeName)
         if not nodeIsDmgr(NodeName) and not nodeIsIHS(NodeName):
            JDBCProvs_list = AdminConfig.list("JDBCProvider", node)
            listJDBCProvider(JDBCProvs_list, node,NodeName,'nodes')
   # List JDBCProvider on Cluster
   if len(clusters) > 0:
      for cluster in clusters:
         ClusterName = AdminConfigShowAttribute(cluster, 'name')
         log.INFO("Retrieve JDBCProvider for cluster %s .. " % ClusterName) 
         JDBCProvs_list = AdminConfig.list("JDBCProvider", cluster)
         listJDBCProvider(JDBCProvs_list, cluster,ClusterName,'clusters')
#End Def
#inizialize parameter
cells=[]
servers = []
nodes = []
clusters = []


if inputScopeName == 'ALL':
   cells=AdminConfig.list("Cell").splitlines()
   servers = AdminConfig.list('Server').splitlines()
   nodes = AdminConfig.list('Node').splitlines()
   clusters = AdminConfig.list('ServerCluster').splitlines()
   launch(servers,nodes,clusters,cells)
elif scope == 'Cell':
    cell=[scopeid]
    launch(servers, nodes, clusters,cells)
elif scope =='Server':
    servers = [scopeid]
    launch(servers, nodes, clusters,cells)
elif scope =='Node':
    nodes = [scopeid]
    launch(servers, nodes, clusters,cells)
elif scope == 'ServerCluster':
    clusters = [scopeid]
    launch(servers, nodes, clusters,cells)
      
log.INFO("%s V%s done" % (scriptName, version))
