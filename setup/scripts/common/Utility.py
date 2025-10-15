# Authors: Sergio Stinchi

# Version        Description

# 1.2.0          Modified def functions to check resources
# 1.1.0          Add Definition getProviderType()
# 1.0.0          Starting version
import os
import sys
from java.io import File
from time import sleep



commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))
execfile("%s/%s" % (commonPath, "wsadminlib.py"))


from java.util import Date
from java.lang import String as jString
from java.text import SimpleDateFormat
from java.util import Properties
from java.util import HashMap
import base64

# print (File(".").getCanonicalPath())


# Variables
scriptUtilityName = "Utility.py"
version = "1.5.7"
propertyPrefix = "com.ibm.adminapp"
log.setClass(scriptUtilityName)

#print "%s V%s" % (scriptUtilityName, version)

def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   log.INFO("%s done" % scriptUtilityName)
   sys.exit(status)
   return

#Given NodeName and Server Nme retrieve unique ID
def getIDServer(nodeName,serverName):
    cell = AdminConfig.list('Cell')
    cellName = AdminConfig.showAttribute(cell, 'name')
    str = "/Cell:%s/Node:%s/Server:%s/" %(cellName,nodeName,serverName)
    id = AdminConfig.getid(str)
    log.DEBUG("XXX - getIDServer = %s" %(id))
    return id

#Given NodeName retrieve unique ID
def getIDNode(nodeName):
    cell = AdminConfig.list('Cell')
    cellName = AdminConfig.showAttribute(cell, 'name')
    str = "/Cell:%s/Node:%s/" %(cellName,nodeName)
    id = AdminConfig.getid(str)
    #log.INFO("XXX - getIDNode = %s" %(id))
    return id


def doesNodeGroupExist(nodeGroupName):
   log.TRACE("<doesNodeGroupExist> Start")
   ngid = AdminConfig.getid("/NodeGroup:" + nodeGroupName)
   log.TRACE("<doesNodeGroupExist> var:ngid = %s" % ngid) 
   print "1"
   if (ngid != None and ngid != ""):
      return "true"
   else:
      return "false"
      
def doesDynamicClusterExist(clusterName):
   log.TRACE("<doesDynamicClusterExist> Start")
   dcid = AdminConfig.getid("/DynamicCluster:" + clusterName)
   log.TRACE("<doesDynamicClusterExist> var:dcid = %s" %dcid)
   if (dcid != None and dcid != ""):
      return "true"
   else:
      return "false"

def getApplicationServerIDbyName(serverName):
   log.TRACE("method:getApplicationServerIDbyName Start")	
   foundID=''
   ApllicationServerIDs = AdminConfig.list('ApplicationServer').splitlines()
   for ApllicationServerID in ApllicationServerIDs:
       log.TRACE("<getApplicationServerIDbyName> - %s" %ApllicationServerID)
       serverID = AdminConfig.showAttribute(ApllicationServerID,'server')
       name = AdminConfig.showAttribute(serverID, 'name')
       if serverName == name:
          foundID = ApllicationServerID
          break
   return foundID
      
def AdminConfigShowAttribute(obj, attrib):
   log.TRACE("method:AdminConfigShowAttribute Start")
   result=''
   try:
      log.TRACE("<AdminConfigShowAttribute> obj = %s" %obj)
      log.TRACE("<AdminConfigShowAttribute> attrib = %s " %attrib)
      result = str(AdminConfig.showAttribute(obj, attrib))
      log.TRACE("<AdminConfigShowAttribute> result = %s " %result)
      if result == 'None': result = ''
      return result
   except:
      type, value, traceback = sys.exc_info()
      log.ERROR("%s (%s)" % (str(value), type))
      return result



def wsadminToList(inStr):
    log.TRACE("method:wsadminToList Start")	
    inStr = inStr.rstrip();
    outList = []
    if (len(inStr) > 0 and inStr[0] == '[' and inStr[-1] == ']'):
       tmpList = inStr[1:-1].split(" ")
    else:
       tmpList = inStr.split("\n")  # splits for Windows or Linux
    for item in tmpList:
       item = item.rstrip();  # removes any Windows "\r"
       if (len(item) > 0):
              outList.append(item)
    return outList
# endDef

def syncEnv(hasChanges):
   if hasChanges == 1: 
      log.INFO("Save ...") 
      AdminConfig.save() 
      log.INFO("Save done") 
      log.INFO("Synchronization ...") 
      nodes = AdminControl.queryNames('type=NodeSync,*') 
      if len(nodes) > 0: 
         nodelist = nodes.splitlines()       
         for node in nodelist: 
            beg = node.find('node=') + 5 
            end = node.find(',', beg) 
            log.INFO("Synchronization for node \"" + node[beg:end] + "\" :",1)
            try: AdminControl.invoke(node, 'sync') 
            except: log.INFO("KO",2) 
            else: log.INFO("OK",2)
         log.INFO("Synchronization done")    
      else:
         log.INFO("No Nodeagent found ") 
   else: 
      log.INFO("No changes made syncronization skipped") 
# end def

def syncEnvDelayed(hasChanges,delay):
   if hasChanges == 1: 
      log.INFO("Save ...") 
      AdminConfig.save() 
      log.INFO("Save done") 
      log.INFO("Synchronization ...") 
      nodes = AdminControl.queryNames('type=NodeSync,*') 
      if len(nodes) > 0: 
         nodelist = nodes.splitlines()       
         for node in nodelist: 
            beg = node.find('node=') + 5 
            end = node.find(',', beg) 
            log.INFO("Synchronization for node \"" + node[beg:end] + "\" :",1)
            try: AdminControl.invoke(node, 'sync') 
            except: log.INFO("KO",2) 
            else: log.INFO("OK",2)
            log.INFO("Waiting for %s seconds" %delay)
            sleep(delay)
         log.INFO("Synchronization done")    
      else:
         log.INFO("No Nodeagent found ") 
   else: 
      log.INFO("No changes made syncronization skipped") 
# end def



def checkScopeName(scopeName):
    log.DEBUG(" #################### BEGIN checkScopeName %s ####################" %(scopeName))  
    scope = None 
    scopeid = None 
    nodeName = None 
    serverName = None 
    clusterName = None
    cells = AdminConfig.list('Cell') 
    nodes = AdminConfig.list('Node') 
    clusters = AdminConfig.list('ServerCluster') 
    servers = AdminConfig.list('Server') 
    if scopeName=="dmgr":
        dmgr = AdminControl.queryNames('WebSphere:name=dmgr,j2eeType=J2EEServer,*')
        nodeDmgr=getNodeNameForServer(dmgr)
        scopeName="%s:%s" %(nodeDmgr,scopeName)
    found=0
    for cell in cells.splitlines():
       if cell.find(scopeName + '(') == 0: 
          scope = 'Cell' 
          scopeid = cell 
          log.INFO("Found Scope: %s - id: %s" % (scope, scopeid) )
          found=1
    if found==0:
       for node in nodes.splitlines():
           if node.find(scopeName + '(') == 0: 
              scope = 'Node' 
              scopeid = node
              nodeName = scopeName
              log.INFO("Found  Scope: %s - id: %s" % (scope, scopeid)) 
              found=1
    if found==0:
        for cluster in clusters.splitlines():
           if cluster.find(scopeName + '(') == 0: 
              scope = 'ServerCluster' 
              scopeid = cluster 
              clusterName = scopeName
              log.INFO("Found  Scope: %s - id: %s" % (scope, scopeid)) 
              found=1
    if found==0:
        for server in servers.splitlines():
            if checkIfIsServerTemplate(server)==False:
               if server.find(scopeName + '(') == 0: 
                  scope = 'Server' 
                  scopeid = server
                  log.INFO("Found  ScopeName %s  - Scope: %s - id: %s" % (scopeName, scope, scopeid)) 
                  found=1
               if scopeName.find(':') != -1:
                  log.TRACE("<checkScopeName> scopeName = %s" %(scopeName)) 
                  scope = 'Server' 
                  colon = scopeName.find(':') 
                  nodeName = scopeName[:colon] 
                  serverName = scopeName[colon + 1:] 
                  log.TRACE("<checkScopeName> /Node:%s/Server:%s/"  %(nodeName,serverName))
                  scopeid = AdminConfig.getid('/Node:%s/Server:%s/'  %(nodeName,serverName))
                  if len(scopeid) == 0: 
                     log.INFO("checkScopeName ERROR: %s not found" % (scopeName)) 
                     log.INFO("%s done" % (scriptUtilityName)) 
                     sys.exit(-1) 
               else: 
                  log.INFO("checkScopeName ERROR: %s not found" % (scopeName)) 
                  log.INFO("%s done" % (scriptUtilityName)) 
                  sys.exit(-1)
    log.TRACE("<checkScopeName> output ")
    log.TRACE("<checkScopeName> Check scope %s done" % (scopeName))
    log.TRACE("<checkScopeName> scope= %s " %(scope))
    log.TRACE("<checkScopeName> scopeid= %s " %(scopeid))
    log.TRACE("<checkScopeName> scopeName= %s " %(scopeName))
    log.TRACE("<checkScopeName> nodeName= %s " %(nodeName))
    log.TRACE("<checkScopeName> serverName= %s " %(serverName))
    log.TRACE("<checkScopeName> clusterName= %s " %(clusterName))
    return scope , scopeid, scopeName, nodeName, serverName, clusterName

def checkIfDestinationExist(resourceName, busName): 
   sibDestinations = AdminTask.listSIBDestinations('[-bus ' + busName + ' ]') 
   if len(sibDestinations) == 0: return None 
   for sibDestination in sibDestinations.splitlines():
      identifier = AdminConfig.showAttribute(sibDestination, 'identifier')
      if identifier.find(resourceName) != -1: 
         return sibDestination 
   return None       

def getVersionInfo():
    try:
        serverVersion = AdminControl.getAttribute(AdminControl.queryNames('WebSphere:*,type=Server,j2eeType=J2EEServer,name=dmgr'), 'platformVersion')
        print "serverVersion = %s" %serverVersion
    except:
        try: 
            serverVersion = AdminControl.getAttribute(AdminControl.queryNames('WebSphere:*,type=Server,j2eeType=J2EEServer,name=*'), 'platformVersion')
            print "serverVersion_1 = %s" %serverVersion
        except: 
            clearExit("ERROR during retrieve version Info", "-1")
    if serverVersion < '6.1': clearExit("ERROR: Too old version of WAS.\nThe script is compatible with WAS 6.1 and later", -1)
    return serverVersion
    
    
# If the resource exist return id of resource , name of resources
def checkIfResourceExist(scopeid, resourceName, typeObject):
    # print "id = %s - Name = %s , typeObject %s " % (scopeid,resourceName, typeObject)
    resourceIds = AdminConfig.list(typeObject, scopeid) 
    if len(resourceIds) == 0: 
        return None , None
    for resourceId in resourceIds.splitlines():
       if resourceId.find(resourceName + '(') != -1:
          beg = resourceId.find(resourceName + '(')
          end = resourceId.find(')', beg) + 1
          return resourceId , resourceId[beg:end]
       else:
          continue
    return None , None 

#New Method (20-10-2018)
def checkIfResourceExistbyJndi(scopeid, resourceName,resourceJndi, typeObject):
    log.INFO("START checkIfResourceExistbyJndi(%s,%s,%s,%s)" %(scopeid, resourceName,jndiName, typeObject))
    # print "id = %s - Name = %s , typeObject %s " % (scopeid,resourceName, typeObject)
    resourceIds = AdminConfig.list(typeObject, scopeid) 
    if len(resourceIds) == 0: 
        return None , None
    for resourceId in resourceIds.splitlines():
       jndi=AdminConfigShowAttribute(resourceId, "jndiName")
       name=AdminConfigShowAttribute(resourceId, "name")
       log.INFO("checkIfResourceExistbyJndi > jndi = %s ## name= %s" %(jndi,name))
       if name==resourceName and jndi==resourceJndi:
          beg = resourceId.find(resourceName + '(')
          end = resourceId.find(')', beg) + 1
          return resourceId , resourceId[beg:end]
       else:
          continue
    return None , None 

def getNodeNameForServer(ServerID):
   beg = ServerID.find('/nodes/') + len('/nodes/')
   end = ServerID.find('/', beg)
   out = ServerID[beg:end]    
   return  out

def getServerName(ServerID):
   # print "ServerID == %s " % (SeverID)
   beg = ServerID.find('/servers/') + len('/servers/')
   end = ServerID.find('|', beg)
   app = ServerID[beg:end]
   return app

def getScopeResources(nmsp_id):
   #print "ID scope = %s " % (nmsp_id)
   beg = 0
   end = nmsp_id.find("(")
   nmSpace = nmsp_id[beg:end]
   name_cell = AdminConfig.showAttribute(AdminConfig.list('Cell'), 'name')
   if nmsp_id.find('/servers/') != -1:
      nmsp_id.find('/nodes/')
      beg = nmsp_id.find('/nodes/') + 1
      end = nmsp_id.find('|', beg)
      out = nmsp_id[beg:end]    
      str = "%s:%s" % (out.split('/')[1], out.split('/')[3])
     
      return  str
   elif nmsp_id.find('/clusters/') != -1:
      beg = nmsp_id.find('/clusters/') + 1
      end = nmsp_id.find('|', beg)
      out = nmsp_id[beg:end]    
      scope = out.split('/')[0]
      name_scope = out.split('/')[1]
      str = "%s" % (name_scope)
      
      return str
   elif nmsp_id.find('/nodes/') != -1:
      beg = nmsp_id.find('/nodes/') + len('/nodes/')
      end = nmsp_id.find('|', beg)
      str = nmsp_id[beg:end]
      
      return str
   elif nmsp_id.find('(cells/') != -1:
      beg = nmsp_id.find('(cells/') + len('(cells/')
      end = nmsp_id.find('|', beg)
      str = nmsp_id[beg:end]
     
      return str
   else:       
       return None

def getStringScopeForId(scope, scopeid, scopeName, nodeName, serverName, clusterName):
   cell = AdminConfig.list('Cell')
   cellName = AdminConfig.showAttribute(cell, 'name')
   if scope == 'Server':
       str = "/Cell:%s/Node:%s/Server:%s" % (cellName, nodeName, serverName)
   elif scope == 'Node':
       str = "/Cell:%s/Node:%s" % (cellName, nodeName)
   elif scope == 'ServerCluster':
       str = "/Cell:%s/ServerCluster:%s" % (cellName, clusterName)
   else:
       str = "/Cell:%s" % (cellName)
   
   log.TRACE("<getStringScopeForId> output = %s:%s " % (scopeName, str))
   return str
def adminConfigGetId(scopeId):
    (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeId)
    res=getStringScopeForId(scope , scopeid, scopeName, nodeName, serverName, clusterName)
    id= AdminConfig.getid(res)
    return id


def getSIBBUSTarget(BusName):
   BusId = AdminConfig.getid('/SIBus:' + BusName + '/')
   busMembers = _splitlist(AdminConfig.showAttribute(BusId, 'busMembers'))
   for busMember in busMembers:
      scopeDestName = AdminConfig.showAttribute(busMember, 'cluster')
      # print "scopeDestName per cluster = %s " % (scopeDestName)
   if  scopeDestName == None or len(scopeDestName) == 0:
      scopeDestNameNode = AdminConfig.showAttribute(busMember, 'node')
      scopeDestNameServer = AdminConfig.showAttribute(busMember, 'server')
      scopeDestName = "%s:%s" % (scopeDestNameNode, scopeDestNameServer)
   return scopeDestName
def getProviderType(provider):
   providerType= AdminConfigShowAttribute(provider, 'providerType'); 
   log.INFO("getProviderType for provider %s is %s" %(provider,providerType)) 
   esito = ""
   if providerType.find('DB2') != -1:
      log.DEBUG( "Type is DB2")
      esito = "DB2"
   elif providerType.find('Oracle') != -1:
      log.DEBUG( "Type is Oracle")
      esito = "Oracle"
   elif providerType.find('Derby') != -1:
      log.DEBUG( "Type is Derby")
      esito = "Derby"
   elif providerType.find('Informix') != 1:
      log.DEBUG( "Type is Informix")
      esito = "Informix"
   else:
      esito = None
   
   log.TRACE("<getProviderType> output = %s" %esito)
   
   return esito

def getDataBaseType(provider):
   return getProviderType(provider)

def listLibrariesREF(librariesRef):
    log.TRACE("<listLibrariesREF> start")
    log.TRACE("<listLibrariesREF> Input %s" %librariesRef)
    l = librariesRef[0]
    l = str(l)[1:-1]
    log.TRACE("<listLibrariesREF> Lista Pulita %s" %l)
    lst = l.split(" ")
    return lst


def convertListToHashMap(J2EEProperySetList):
        log.DEBUG("Begin convertListToHashMap")
        map = HashMap()
        if (len(J2EEProperySetList) == 0):return map
        propsetList = []
        try:
           for psItem in J2EEProperySetList:
              propname = AdminConfigShowAttribute(psItem, "name")
              propvalue = AdminConfigShowAttribute(psItem, "value")
              # print "--------------"
              # print "propname " + str(propname)
              # print "propvalue " + str(propvalue)
              # print "--------------"
              map.put(propname, propvalue)
           # end for
        except:
           log.INFO("KO")
           type, value, traceback = sys.exc_info()
           log.ERROR("%s (%s)" % (str(value), type))
           return map
        return map

def convertListToThreeItemHashMap(J2EEProperySetList):
        log.DEBUG("Begin convertListToThreeItemHashMap")
        map = HashMap()
        if (len(J2EEProperySetList) == 0):return map
        propsetList = []
        try:
           for psItem in J2EEProperySetList:
              propname = AdminConfigShowAttribute(psItem, "name")
              propvalue = AdminConfigShowAttribute(psItem, "value")
              proptype = AdminConfigShowAttribute(psItem, "type")
              log.DEBUG("--------------")
              log.DEBUG("propname " + str(propname))
              log.DEBUG("propvalue " + str(propvalue))
              log.DEBUG("proptype " + str(proptype))
              log.DEBUG("--------------")
              p = "%s#%s" %(propvalue,proptype)
              log.DEBUG(" HashMap row = %s:%s" %(propname,p))
              map.put(propname, p)
           # end for
        except:
           log.INFO("KO")
           type, value, traceback = sys.exc_info()
           log.ERROR("%s (%s)" % (str(value), type))
           return map
        return map



def display(lista, f1):
    for par in lista:
        print >> f1, par
# end def

def checkIfIsNone(str):
   if str == None:
      return ''
   else:
      return str

def getTypeName(id):
   ObjStr = str(id)
   beg = id.find('#') + 1
   end = id.find('_', beg)
   sType = id[beg:end]
   return sType
def checkIsNumber(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

def checkIfIsServerTemplate(ScopeId):
     if ScopeId.find('/dynamicclusters/') != -1:
         log.DEBUG("ScopeId %s is ServerTemplate " %(ScopeId)) 
         return True
     else:
         return False

def retrieveDsConfigurationParameter(ds):
   str = ""
   configurationParameters = ""
   value = ""
   print "DS = %s" % (ds)
   propsSet = AdminConfig.showAttribute(ds, 'propertySet')
   resourceProperties = AdminConfig.showAttribute(propsSet, 'resourceProperties')[1:-1].split()
   configurationParameters = "[ "
   for rsp in resourceProperties:
      name = AdminConfig.showAttribute(rsp, 'name')
      value = AdminConfig.showAttribute(rsp, 'value')
      if len(configurationParameters) > 2:
         configurationParameters += ","
      configurationParameters += " ['%s','%s','%s']  " % (AdminConfig.showAttribute(rsp, 'name'), AdminConfig.showAttribute(rsp, 'type'), AdminConfig.showAttribute(rsp, 'value')) 
   configurationParameters += " ]"
   return str , configurationParameters   
   
def isObjectInScope(ComponentId, scopeName, scopeType):
    # CellDS(cells/Was7Cell|resources.xml#DataSource_1412328773120)
    # ORACLE_DS_NODE(cells/Was7Cell/nodes/was7Node01|resources.xml#DataSource_1412085327141)
    # ORACLE_DS_SERVER(cells/Was7Cell/nodes/was7Node01/servers/pressass_entrate|resources.xml#DataSource_1412090969325)
    # ClusterDs(cells/Was7Cell/clusters/cls|resources.xml#DataSource_1412329699248)
    index = ComponentId.find(scopeType + "/" + scopeName + "|")
    if index != -1:
       return True
    else:  
       return False
    
    
    
def ApplySystemPropertyDmgr(name,value):
   print " -- ApplySystemPropertyDmgr -- "
   # Retrieve platformVersion
   try:
      (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName("dmgr")
      AdminTask.setJVMSystemProperties('[-serverName  '+serverName+' -nodeName '+ nodeName + ' -propertyName com.ibm.websphere.management.configservice.validateNames -propertyValue false]')
      AdminConfig.save()
   except: 
      pass
      print "Property settings done"
      
def readApplicationProperties(props):
   applicationProperties =[]
   appClassloader=''
   appEnvEntries=''
   applicationRoles=''
   contextRoots=''
   createNewServicePolicy=''
   drainageInterval=''
   edition=''
   editionDesc=''
   ejbAutoLink=''
   ejbBindings=''
   ejbEnvEntries=''
   ejbInterfaceBindings=''
   ejbReferences=''
   extraOptions=''
   forceHttpOnly=''
   forceHttpsCookies=''
   forceSecurityIntegration=''
   forceSessionPath=''
   forceUpdateOnly=''
   latestChangedFiles=''
   mdbBindings=''
   metadataComplete=''
   propagatePlugin=''
   resourceEnvReferences=''
   resourceReferences=''
   rolloutGroupSize=''
   rolloutResetStrategy=''
   rolloutStrategy=''
   scaEJBBindings=''
   scaModuleProperties=''
   scaSCABindings=''
   scaWSBindings=''
   servletInitParameters=''
   sharedLibraries=''
   startApplication=''
   startingWeight=''
   syncDelay=''
   targetObjects=''
   timeoutRollout=''
   virtualHosts=''
   updateContentType=''
   updateContentURI=''
   updateValidationDate=''
   warClassLoaderPolicy=''
   webEnvEntries=''
   wsPolicySets=''
   appName=''
   appLocation=''
   dummy = props.getProperty(propertyPrefix + ".app.name", "")
   if len(dummy) > 0: 
       appName = ['appName',dummy.strip()]
       applicationProperties.append(appName)
   
   dummy = props.getProperty(propertyPrefix + ".app.location", "")
   if len(dummy) > 0: 
       appLocation = ['appLocation',dummy.strip()]
       applicationProperties.append(appLocation)
   
   dummy = props.getProperty(propertyPrefix + ".app.classloader", "")
   if len(dummy) > 0: 
       appClassloader = ['appClassloader',dummy.strip()]
       applicationProperties.append(appClassloader)
   dummy = props.getProperty(propertyPrefix + ".app.env.entries", "")
   if len(dummy) > 0: 
       appEnvEntries = ['appEnvEntries', eval(dummy)]
       applicationProperties.append(appEnvEntries)
   dummy = props.getProperty(propertyPrefix + ".application.roles", "")
   if len(dummy) > 0: 
       applicationRoles = ['applicationRoles', eval(dummy)]
       applicationProperties.append(applicationRoles)
   
   dummy = props.getProperty(propertyPrefix + ".context.roots", "")
   if len(dummy) > 0: 
       contextRoots = ['contextRoots', eval(dummy)]
       applicationProperties.append(contextRoots)
   
   dummy = props.getProperty(propertyPrefix + ".create.new.service.policy", "")
   if len(dummy) > 0: 
       createNewServicePolicy = ['createNewServicePolicy', dummy.strip()]
       applicationProperties.append(createNewServicePolicy)
   
   dummy = props.getProperty(propertyPrefix + ".drainage.interval", "")
   if len(dummy) > 0: 
       drainageInterval = ['drainageInterval', int(dummy.strip())]
       applicationProperties.append(drainageInterval)

   dummy = props.getProperty(propertyPrefix + ".edition", "")
   if len(dummy) > 0: 
       edition = ['edition', dummy.strip()]
       applicationProperties.append(edition)
   
   dummy = props.getProperty(propertyPrefix + ".edition.desc", "")
   if len(dummy) > 0: 
       editionDesc = ['editionDesc', dummy.strip()]
       applicationProperties.append(editionDesc)
   
   dummy = props.getProperty(propertyPrefix + ".ejb.autolink", "")
   if len(dummy) > 0: 
       ejbAutoLink = ['ejbAutoLink', dummy.strip()]
       applicationProperties.append(ejbAutoLink)
   
   dummy = props.getProperty(propertyPrefix + ".ejb.bindings", "")
   if len(dummy) > 0: 
       ejbBindings = ['ejbBindings', eval(dummy)]
       applicationProperties.append(ejbBindings)
   
   dummy = props.getProperty(propertyPrefix + ".ejb.env.entries", "")
   if len(dummy) > 0: 
       ejbEnvEntries = ['ejbEnvEntries', eval(dummy)]
       applicationProperties.append(ejbEnvEntries)
   
   dummy = props.getProperty(propertyPrefix + ".ejb.interface.binding", "")
   if len(dummy) > 0: 
       ejbInterfaceBindings = ['ejbInterfaceBindings', eval(dummy)]
       applicationProperties.append(ejbInterfaceBindings)
   
   dummy = props.getProperty(propertyPrefix + ".ejb.references", "")
   if len(dummy) > 0: 
       ejbReferences = ['ejbReferences', eval(dummy)]
       applicationProperties.append(ejbReferences)
   
   dummy = props.getProperty(propertyPrefix + ".extra.options", "")
   if len(dummy) > 0: 
       extraOptions = ['extraOptions', eval(dummy)]
       applicationProperties.append(extraOptions)
   
   dummy = props.getProperty(propertyPrefix + ".force.http.only", "")
   if len(dummy) > 0: 
       forceHttpOnly = ['forceHttpOnly', dummy.strip()]
       applicationProperties.append(forceHttpOnly)
   
   dummy = props.getProperty(propertyPrefix + ".force.https.cookies", "")
   if len(dummy) > 0: 
       forceHttpsCookies = ['forceHttpsCookies', dummy.strip()]
       applicationProperties.append(forceHttpsCookies)
   
   dummy = props.getProperty(propertyPrefix + ".force.security.integration", "")
   if len(dummy) > 0: 
       forceSecurityItegration = ['forceSecurityItegration', dummy.strip()]
       applicationProperties.append(forceSecurityItegration)
   
   dummy = props.getProperty(propertyPrefix + ".force.session.path", "")
   if len(dummy) > 0: 
       forceSessionPath = ['forceSessionPath', dummy.strip()]
       applicationProperties.append(forceSessionPath)
   
   dummy = props.getProperty(propertyPrefix + ".force.update.only", "")
   if len(dummy) > 0: 
       forceUpdateOnly = ['forceUpdateOnly', dummy.strip()]
       applicationProperties.append(forceUpdateOnly)
   
   dummy = props.getProperty(propertyPrefix + ".latest.changed.files", "")
   if len(dummy) > 0: 
       latestChangedFiles = ['latestChangedFiles', eval(dummy)]
       applicationProperties.append(latestChangedFiles)
   
   dummy = props.getProperty(propertyPrefix + ".mdb.bindings", "")
   if len(dummy) > 0: 
       mdbBindings = ['mdbBindings', eval(dummy)]
       applicationProperties.append(mdbBindings)
   
   dummy = props.getProperty(propertyPrefix + ".metadata.complete", "")
   if len(dummy) > 0: 
       metadataComplete = ['metadataComplete', dummy.strip()]
       applicationProperties.append(metadataComplete)
   
   dummy = props.getProperty(propertyPrefix + ".propagate.plugin", "")
   if len(dummy) > 0: 
       propagatePlugin = ['propagatePlugin', dummy.strip()]
       applicationProperties.append(propagatePlugin)
   
   dummy = props.getProperty(propertyPrefix + ".resource.env.references", "")
   if len(dummy) > 0: 
       resourceEnvReferences = ['resourceEnvReferences', eval(dummy)]
       applicationProperties.append(resourceEnvReferences)
   
   dummy = props.getProperty(propertyPrefix + ".resource.references", "")
   if len(dummy) > 0: 
       resourceReferences = ['resourceReferences', eval(dummy)]
       applicationProperties.append(resourceReferences)
   
   dummy = props.getProperty(propertyPrefix + ".rollout.group.size", "")
   if len(dummy) > 0: 
       rolloutGroupSize = ['rolloutGroupSize', int(dummy.strip())]
       applicationProperties.append(rolloutGroupSize)
   
   dummy = props.getProperty(propertyPrefix + ".rollout.strategy", "")
   if len(dummy) > 0: 
       rolloutStrategy = ['rolloutStrategy', dummy.strip()]
       applicationProperties.append(rolloutStrategy)
   
   dummy = props.getProperty(propertyPrefix + ".rollout.reset.strategy", "")
   if len(dummy) > 0: 
       rolloutResetStrategy = ['rolloutResetStrategy', dummy.strip()]
       applicationProperties.append(rolloutResetStrategy)
   
   dummy = props.getProperty(propertyPrefix + ".sca.ejb.bindings", "")
   if len(dummy) > 0: 
       scaEJBBindings = ['scaEJBBindings', eval(dummy)]
       applicationProperties.append(scaEJBBindings)
   
   dummy = props.getProperty(propertyPrefix + ".sca.module.properties", "")
   if len(dummy) > 0: 
       scaModuleProperties = ['scaModuleProperties', eval(dummy)]
       applicationProperties.append(scaModuleProperties)
   
   dummy = props.getProperty(propertyPrefix + ".sca.sca.bindings", "")
   if len(dummy) > 0: 
       scaSCABindings = ['scaSCABindings', eval(dummy)]
       applicationProperties.append(scaSCABindings)
   
   dummy = props.getProperty(propertyPrefix + ".sca.ws.bindings", "")
   if len(dummy) > 0: 
       scaWSBindings = ['scaWSBindings', eval(dummy)]
       applicationProperties.append(scaWSBindings)
   
   dummy = props.getProperty(propertyPrefix + ".servlet.init.parameters", "")
   if len(dummy) > 0: 
       servletInitParameters = ['servletInitParameters', eval(dummy)]
       applicationProperties.append(servletInitParameters)
   
   dummy = props.getProperty(propertyPrefix + ".shared.libraries", "")
   if len(dummy) > 0: 
       sharedLibraries = ['sharedLibraries', eval(dummy)]
       applicationProperties.append(sharedLibraries)
   
   dummy = props.getProperty(propertyPrefix + ".start.application", "")
   if len(dummy) > 0: 
       startApplication = ['startApplication', dummy.strip()]
       applicationProperties.append(startApplication)
   
   dummy = props.getProperty(propertyPrefix + ".starting.weight", "")
   if len(dummy) > 0: 
       startingWeight = ['startingWeight', int(dummy.strip())]
       applicationProperties.append(startingWeight)
   
   dummy = props.getProperty(propertyPrefix + ".sync.delay", "")
   if len(dummy) > 0: 
       syncDelay = ['syncDelay', int(dummy.strip())]
       applicationProperties.append(syncDelay)
   
   dummy = props.getProperty(propertyPrefix + ".target.objects", "")
   if len(dummy) > 0: 
       targetObjects = ['targetObjects', eval(dummy)]
       applicationProperties.append(targetObjects)
   
   dummy = props.getProperty(propertyPrefix + ".timeout.rollout", "")
   if len(dummy) > 0: 
       timeoutRollout = ['timeoutRollout', int(dummy.strip())]
       applicationProperties.append(timeoutRollout)
   
   dummy = props.getProperty(propertyPrefix + ".virtual.hosts", "")
   if len(dummy) > 0:
        virtualHosts = ['virtualHosts', eval(dummy)]
        applicationProperties.append(virtualHosts)
   
   dummy = props.getProperty(propertyPrefix + ".update.content.type", "")
   if len(dummy) > 0: 
       updateContentType = ['updateContentType', dummy.strip()]
       applicationProperties.append(updateContentType)
   
   dummy = props.getProperty(propertyPrefix + ".update.content.uri", "")
   if len(dummy) > 0: 
       updateContentURI = ['updateContentURI', dummy.strip()]
       applicationProperties.append(updateContentURI)
   
   dummy = props.getProperty(propertyPrefix + ".update.validation.date", "")
   if len(dummy) > 0: 
       updateValidationDate = ['updateValidationDate', dummy.strip()]
       applicationProperties.append(updateValidationDate)
   
   dummy = props.getProperty(propertyPrefix + ".war.classloader.policy", "")
   if len(dummy) > 0: 
       warClassLoaderPolicy = ['warClassLoaderPolicy', dummy.strip()]
       applicationProperties.append(warClassLoaderPolicy)
   
   dummy = props.getProperty(propertyPrefix + ".web.env.entries", "")
   if len(dummy) > 0: 
       webEnvEntries = ['webEnvEntries', eval(dummy)]
       applicationProperties.append(webEnvEntries)
   
   dummy = props.getProperty(propertyPrefix + ".ws.policy.sets", "")
   if len(dummy) > 0: 
       wsPolicySets = ['wsPolicySets', eval(dummy)]
       applicationProperties.append(wsPolicySets)
   log.DEBUG("applicationProperties = %s" %(applicationProperties))
   return applicationProperties
   
    
def getListValue(list,name):
    ret=''
    for item in list:
       if item[0] == name:
          ret=item[1]
          log.DEBUG("Found value = %s" %(ret))
          break
       else:
          ret = "" 
    return ret

def getVersion(appName):
   try:
      output = AdminApp.view(appName, '-buildVersion')
      beg = output.find(':')
      if beg != -1: data = output[beg + 1:].strip()
      else: data = 'N/A'
   except: 
      data = 'N/A'
   return data

def checkifApplicationExist(AppName):
     if appName in AdminApp.list().splitlines():
        buildId = getVersion(appName) 
        log.DEBUG("Application %s already exists (buildId = %s)" % (appName, buildId))
        return True
     else:
        return False 

def nodeExist(nodeNm):
   log.DEBUG("nodeExist ?  %s" %nodeNm)
   nodes = AdminConfig.list('Node').splitlines()
   if len(nodes) > 0:
      for node in nodes:
         NodeName = AdminConfig.showAttribute(node, 'name')
         log.DEBUG("NodeName ?  %s" %NodeName)
         if nodeNm == NodeName:
            log.DEBUG(" %s exist" %nodeNm)
            return 1
   log.DEBUG(" %s doesnt exist" %nodeNm)
   return 0  

def listASByNodeName(nodeName):
    lista =[]
    servers = AdminConfig.list('Server').splitlines()
    lista = [x for x in servers if getNodeNameForServer(x) == nodeName]
    return lista
            
def applyApexTranslation(str):
    return str.replace('\'', '\\\'')        
    
def setupCustomProperty(resourceId,customProperties):
    log.DEBUG("<setupCustomProperty> START")
    log.TRACE("<setupCustomProperty> INPUT resourceId: %s" %resourceId)
    log.TRACE("<setupCustomProperty> INPUT customProperties: %s" %customProperties)
    resourcePropertiesSet=""
    propsCreated=0
    modified=0
    if resourceId != None: 
        properties=[]
        propertiesSetID = AdminConfigShowAttribute(resourceId, 'propertySet')
        if propertiesSetID=="":
            resourceProperties = AdminConfigShowAttribute(resourceId, 'resourceProperties')
            log.TRACE("AA - propertiesSetID IS NULL Use resourceProperties form resourceId")
        else:
            log.TRACE("AB - propertiesSetID IS NOT NULL Use resourceProperties form propertiesSetID")
            resourceProperties = AdminConfigShowAttribute(propertiesSetID, 'resourceProperties')
        log.TRACE("<setupCustomProperty> propertiesSetID == %s" % propertiesSetID)
        log.TRACE("<setupCustomProperty> resourceProperties == %s" % resourceProperties)
        log.TRACE("<setupCustomProperty> customProperties == %s" % customProperties) 
        resourcePropertiesSet = resourceProperties[1:-1].split()
        log.TRACE("<setupCustomProperty> resourcePropertiesSet == %s" % resourcePropertiesSet) 
        try:
            for property in customProperties:
                modified = 0
                log.INFO("<setupCustomProperty> Check the property  %s " %(property))
                log.TRACE("<setupCustomProperty> Name = %s" %(property[0]) )
                log.TRACE("<setupCustomProperty> Type = %s" %(property[1]) )
                log.TRACE("<setupCustomProperty> Value = %s" %(property[2]) )
                log.TRACE("<setupCustomProperty>  resourceProperties==%s" %resourceProperties)
                resourcePropertiesSet = resourceProperties[1:-1].split()
                log.TRACE("<setupCustomProperty>  resourcePropertiesSet==%s" %resourcePropertiesSet)
                inexistent=False
                if len(resourcePropertiesSet)==0:
             	    log.TRACE("<setupCustomProperty>  resourceProperties = 0")
             	    attributes='[ [name "%s"] [type "%s"] [value "%s"] [required "false"]]' %(property[0],property[1],property[2])
             	    log.INFO("Attributes = %s" %attributes)
             	    attr = [ ['name', property[0]],['type', property[1]],['value', property[2]] ]
                    log.INFO("Create Custom Property %s with value %s" %(property[0], property[2]),1)
                    AdminConfig.create('J2EEResourceProperty', propertiesSetID, attributes)      
                    log.INFO( " OK",2 )
                else:
                    for resourceProperty in resourcePropertiesSet: 
                        log.TRACE("<setupCustomProperty> ResourceProperty = %s "  % resourceProperty)
                        nameRP = resourceProperty[0:resourceProperty.find('(')]         
                        log.TRACE("<setupCustomProperty> Name of Resource Property= %s "  % nameRP)
                        log.TRACE("<setupCustomProperty> Compare RP:%s with input: %s" %(nameRP,property[0]))
                        if property[0] == nameRP: 
                            log.INFO("Modify Custom Property %s with value %s" %(property[0],property[2]),1)
                            AdminConfig.modify(resourceProperty, "[ ['value' '" + property[2] + "'] ]")
                            modified = 1
                            log.INFO(" OK ")
                            inexistent=False
                            break
                        else:
                            inexistent=True
                            log.TRACE("")      
                    if inexistent==True:
                        log.TRACE("Property named %s not Found CREATE IT" %property[0])
                        attr = [ ['name', property[0]],['type', property[1]],['value', property[2]] ]
                        attributes='[ [name "%s"] [type "%s"] [value "%s"] [required "false"]]' %(property[0],property[1],property[2])
                        log.TRACE("Attributes = %s" %attributes)
                        log.INFO("Create Custom Property %s with value %s" %(property[0], property[2]),1)
                        #log.TRACE( "AdminConfig.create('%s','%s','%s')" %('J2EEResourceProperty', propertiesSetID, attributes)) 
                        if propertiesSetID=='':
                            AdminConfig.create('J2EEResourceProperty', resourceId, attributes)
                        else:
                            AdminConfig.create('J2EEResourceProperty', propertiesSetID, attributes)
                        log.INFO( " OK",2 )   
     	        #end if
         #end for
	        propertiesSetID = AdminConfigShowAttribute(resourceId, 'propertySet')
            if propertiesSetID=='':
	            resourceProperties = AdminConfigShowAttribute(propertiesSetID, 'resourceProperties')
            else:
                resourceProperties = AdminConfigShowAttribute(propertiesSetID, 'resourceProperties')
	        #end if
            resourcePropertiesSet = resourceProperties[1:-1].split()
            for resourceProperty in resourcePropertiesSet: 
                log.TRACE("<setupCustomProperty> cycle ResourceProperty to find fake props")
                nameRP = resourceProperty[0:resourceProperty.find('(')]         
                log.TRACE("<setupCustomProperty> Name of Resource Property= %s "  % nameRP)
                if nameRP == "fakeprops":
	               log.TRACE("Found fakeprops -- Delete Custom Property fakeprops ",1)
	               AdminConfig.remove(resourceProperty)
	               log.INFO(" OK",2)
	               break 
        except:
            log.ERROR( "KO"  ,2)
            type, value, traceback = sys.exc_info()
            log.ERROR( " %s (%s)" % (str(value), type))
            clearExit("   KO\nRollback and exit", -1)
    else:
        log.INFO( "Resource %s doesn't exist " %(resourceId))
        clearExit("KO\nRollback and exit", -1)

def printBasicScriptInfo(authors,scriptName,scriptVersion):
    log.INFO("--------------------------------------- ")
    log.INFO(" Author:  %s" %(authors))
    log.INFO(" Script:  %s" %(scriptName))
    log.INFO(" Version: %s" %(scriptVersion))
    log.INFO("--------------------------------------- ")



def isIntelligentManagementEnabled(nodeName,serverName):
    cells=AdminConfig.list("Cell").splitlines()
    cellName = AdminConfig.showAttribute(cells[0], 'name')
    try:
       im = AdminTask.modifyIntelligentManagement(['-node', nodeName, '-webserver', serverName, '-retryInterval', '90'] )
    except:
        log.INFO(" Webserver %s isn't ODR'" %(serverName))
        imEnabled=0
        return imEnabled
        
    print "Intelligent Management object file= %s" %(im)
    val=AdminConfig.show(im)
    log.DEBUG( " Val = %s " %val)
    if val==None:
        log.INFO( "WebSphere is Under 8.5")
        imEnabled=0
    else:  
        properties = AdminConfig.show(im).splitlines()
        for prop in properties:
            prop=prop[1:-1].split()
            if prop[0] == "enabled":
               if prop[1] == "true":
                  imEnabled=1
               else:
                  imEnabled=0
    return imEnabled


def getTypeOfServer(nodename,servername):
    """Get the type of the given server.
    E.g. 'APPLICATION_SERVER' or 'PROXY_SERVER'."""
    node_id = getNodeId(nodename)
    serverEntries = _splitlines(AdminConfig.list( 'ServerEntry', node_id ))
    for serverEntry in serverEntries:
        sName = AdminConfig.showAttribute( serverEntry, "serverName" )
        if sName == servername:
            return AdminConfig.showAttribute( serverEntry, "serverType" )
    return None        


def listTypeOfCluster(lst, type):
   #########POSSIBLE VALUE OF TYPE [static; dinamic] #############
   log.DEBUG("#################### listTypeOfCluster Start for Type %s ####################" %type)
   lstFilterd =[]
   for element  in lst:	
      log.TRACE("lista NODE:SERVER  per cluster =  %s" %element)
      log.TRACE("Prima Coppia NODO:SERVER = %s" %element[0])
      (scope , scopeid, scopeName, nodeName, serverName, clusterName)  = checkScopeName(element[0])
      clusterName= AdminConfig.showAttribute(scopeid,"clusterName")
      log.TRACE("Cluster Name = %s for Server %s" %(clusterName,serverName))
      isDinamic=doesDynamicClusterExist(clusterName)
      log.DEBUG("This Cluser is Dinamic ? %s " %isDinamic)
      if type=="static":	
   	 if isDinamic=="false":
   	 	lstFilterd.append(element)
   	 	log.DEBUG("Lista FILTRATA di tipo %s = %s" %(type,lstFilterd))
      elif type=="dinamic":
      	 if isDinamic=="true":
   	 	lstFilterd.append(element)
   	 	log.DEBUG("Lista FILTRATA di tipo %s = %s" %(type,lstFilterd))
      else:
      	 print "NON SI DEVE VERIFICARE"
   return lstFilterd
      
   
   #return listFiltered
#def encodeXor(StringToEncode):    
#    ret = xor_crypt_string(StringToEncode,"1", encode=True)
#    return ret

#def decodeXor(StringToDencode):
#    ret=xor_crypt_string(StringToDencode,"1", decode=True)
#    return ret

#def xor_crypt_string(data, key, encode=False, decode=False):
#    from itertools import izip, cycle
#    import base64
#    if decode:
#        data = base64.decodestring(data)
#    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
#    if encode:
#        return base64.encodestring(xored).strip()
#    return xored    