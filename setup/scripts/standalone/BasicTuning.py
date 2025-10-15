                # Author: Stinchi Sergio

# Version        Description
# 1.0.0          Starting version

# Import
import sys
import java

# Global variables
scriptName = "BasicTuning.py"
version = "1.0.0"

# Start
#print "%s V%s" % (scriptName, version)

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Command Line
argc = len(sys.argv)
if argc < 1:
   print "Usage: %s <choose> [optional JDK_VERSION ] " % (scriptName)
   sys.exit(-1)
else:
    choose = sys.argv[0]
    print "choose = %s" %(choose)
    if argc > 1: 
        if argc != 2 :
            print "Usage: %s <choose> [optional JDK_VERSION ] " % (scriptName)
            sys.exit(-1)
        else: 
            jdkChoose = sys.argv[1]
            print "JDK Choosed = %s" %(jdkChoose)

def getIDServer(nodeName,serverName):
    cell = AdminConfig.list('Cell')
    cellName = AdminConfig.showAttribute(cell, 'name')
    str = "/Cell:%s/Node:%s/Server:%s/" %(cellName,nodeName,serverName)
    id = AdminConfig.getid(str)
    log.DEBUG("XXX - getIDServer = %s" %(id))
    return id

def disableEmbeddedConfiguration():
   print " -- DisableEmbeddedConfiguration -- "
   # Retrieve platformVersion
   try:
      dmgr = AdminControl.queryNames('WebSphere:name=dmgr,j2eeType=J2EEServer,*')
      platformVersion = AdminControl.getAttribute(dmgr, 'platformVersion')
      print "platformVersion = %s" % platformVersion
   except: 
      pass
   # Data
   properties = [ ['com.ibm.websphere.management.processEmbeddedConfigGlobal', 'false']]
   # Print read data
   print "properties = %s" % (properties)
   print "Print properties data done"
   # Property settings
   print "Property settings ..."
   dmgr = AdminConfig.getid('/Server:dmgr/')
   if len(dmgr) == 0:
      clearExit("No Dmgr found", 0)
   jvm = AdminConfig.list('JavaVirtualMachine', dmgr)
   for property in properties:
      print '   name = %s, value = %s:' % (property[0], property[1]) ,
      name = property[0]
      value = property[1]
      jvmprop = [ ["name", name], ["value", "" + value], ["required", "false"] ]
      sysprops = ["systemProperties", [jvmprop]]      
      found = 0
      curr = AdminConfig.showAttribute(jvm, "systemProperties")
      if len(curr) > 0: propslist = curr[1:-1].split()
      else: propslist = []
      for prop in propslist:
         if name == AdminConfig.showAttribute(prop, 'name'):
            if value == AdminConfig.showAttribute(prop, 'value'):
               print "OK (property already set)"
               found = 1
               break
            else:
               try: 
                  AdminConfig.modify(prop, jvmprop)
                  print "OK (property updated)"
               except:                  
                  type, value, traceback = sys.exc_info()
                  print "KO (ERROR: %s (%s))" % (str(value), type)
                  clearExit("Rollback and exit", -1)
               found = 1
               break                  
      if found == 0:
         try: 
            AdminConfig.modify(jvm, [sysprops])
            print "OK (property added)"
         except:                  
            type, value, traceback = sys.exc_info()
            print "KO (ERROR: %s (%s))" % (str(value), type)
            clearExit("Rollback and exit", -1)
   print "Property settings done"
   syncEnv(AdminConfig.hasChanges()) 


def disableIPV6():
   # Retrieve platformVersion
   try:
      dmgr = AdminControl.queryNames('WebSphere:name=dmgr,j2eeType=J2EEServer,*')
      platformVersion = AdminControl.getAttribute(dmgr, 'platformVersion')
      print "platformVersion = %s" % platformVersion
   except: 
      pass
   # Data
   properties = [ ['com.ibm.cacheLocalHost', 'true'], ['java.net.preferIPv4Stack', 'true'] ]
   # Print read data
   print "Print properties data ..."
   print "properties = %s" % (properties)
   print "Print properties data done"
   # Retrieve all servers IDs
   print "Retrieve all server IDs ..."
   serverids = AdminConfig.list('Server').split(lineSeparator)
   print "Found %d server(s)" % (len(serverids))
   print "Retrieve all server IDs done"
   # Property settings
   print "Property settings ..."
   for serverid in serverids:
      jvm = AdminConfig.list('JavaVirtualMachine', serverid)
      server = AdminConfig.showAttribute(serverid, 'name')
      beg = serverid.find('/nodes/')
      if beg != -1:
         beg += len('/nodes/')
         end = serverid.find('/', beg)
         node = serverid[beg:end]
         print "Node: %s, Server: %s" % (node, server)
      else:
         print "Dynamic Cluster: %s" % (server)
      if len(jvm) == 0: 
          print " Property not in scope"
          continue   
      for property in properties:
         print '   name = %s, value = %s:' % (property[0], property[1]) ,
         name = property[0]
         value = property[1]
         jvmprop = [ ["name", name], ["value", "" + value], ["required", "false"] ]
         sysprops = ["systemProperties", [jvmprop]]      
         found = 0
         curr = AdminConfig.showAttribute(jvm, "systemProperties")
         if len(curr) > 0: propslist = curr[1:-1].split()
         else: propslist = []
         for prop in propslist:
            if name == AdminConfig.showAttribute(prop, 'name'):
               if value == AdminConfig.showAttribute(prop, 'value'):
                  print "OK (property already set)"
                  found = 1
                  break
               else:
                  try: 
                     AdminConfig.modify(prop, jvmprop)
                     print "OK (property updated)"
                  except:                  
                     type, value, traceback = sys.exc_info()
                     print "KO (ERROR: %s (%s))" % (str(value), type)
                     clearExit("Rollback and exit", -1)
                  found = 1
                  break                  
         if found == 0:
            try: 
               AdminConfig.modify(jvm, [sysprops])
               print "OK (property added)"
            except:                  
               type, value, traceback = sys.exc_info()
               print "KO (ERROR: %s (%s))" % (str(value), type)
               clearExit("Rollback and exit", -1)
   syncEnv(1)
   print "##### DisableIPV6 Finished #####"
# END DEF disableIPV6


def setExecutionOwnerWasup():
   # Retrieve platformVersion
   try:
      dmgr = AdminControl.queryNames('WebSphere:name=dmgr,j2eeType=J2EEServer,*')
      platformVersion = AdminControl.getAttribute(dmgr, 'platformVersion')
      print "platformVersion = %s" % platformVersion
   except:
      pass
   # Data
   serverids = AdminConfig.list('Server').split(lineSeparator)
   # Property settings
   for serverid in serverids:
      jpdef = AdminConfig.list('JavaProcessDef', serverid)
      if jpdef: # found Java ProcessDef
        processExecution = AdminConfig.showAttribute(jpdef, 'execution')
        params = [['runAsUser',"wasup"], ['runAsGroup',"wasup"], ['runInProcessGroup', "0"], ['processPriority', "20"], ['umask', "022"]]
        AdminConfig.modify(processExecution,params)
        ServerName = AdminConfig.showAttribute(serverid, "name")
        print "Set Execution Owner wasup for server %s "  %(ServerName)
        print "Task Completed"
   print "##### setExecutionOwner Finished #####"
# END DEF setExecutionOwnerWasup()



def applyEnableSecurityServiceCheck():
     found = 0
     serverids = AdminConfig.list('Server').split(lineSeparator)
     for serverid in serverids:
         sType = AdminConfig.showAttribute(serverid, "serverType")
         if sType == "NODE_AGENT":
             ORBobjs = AdminConfig.list('ObjectRequestBroker', serverid).splitlines()
             # print "ORBobjs = %s" %(ORBobjs)
             for orbobj in ORBobjs:
                 # print "orbobj = %s " %(orbobj)
                 properties = AdminConfig.list('Property', orbobj).splitlines()
                 for prop in properties:
                    # print "prop = %s" %(prop)
                    # print "prop name = %s " %(AdminConfig.showAttribute(prop, 'name'))
                    if "com.ibm.ws.orb.services.lsd.EnableSecurityServiceCheck" == AdminConfig.showAttribute(prop, 'name'):
                       print "name = com.ibm.ws.orb.services.lsd.EnableSecurityServiceCheck, value = true: OK (property already set)"
                       found = 1
                       break
                 if found == 0:
                    print "create property com.ibm.ws.orb.services.lsd.EnableSecurityServiceCheck = true"
                    AdminConfig.create('Property', orbobj, '[[validationExpression ""] [name "com.ibm.ws.orb.services.lsd.EnableSecurityServiceCheck"] [description "PMR 66194"] [value "true"] [required "false"]]')
     syncEnv(1)
# end def


def applyScriptingPatch():
   print " -- applyScriptingPath -- "
   # Retrieve platformVersion
   try:
      dmgr = AdminControl.queryNames('WebSphere:name=dmgr,j2eeType=J2EEServer,*')
      platformVersion = AdminControl.getAttribute(dmgr, 'platformVersion')
      print "platformVersion = %s" % platformVersion
   except: 
      pass
   # Data
   properties = [ ['com.ibm.websphere.management.configservice.validateNames', 'false']]
   # Print read data
   print "properties = %s" % (properties)
   print "Print properties data done"
   # Property settings
   print "Property settings ..."
   dmgr = AdminConfig.getid('/Server:dmgr/')
   if len(dmgr) == 0:
      clearExit("No Dmgr found", 0)
   jvm = AdminConfig.list('JavaVirtualMachine', dmgr)
   for property in properties:
      print '   name = %s, value = %s:' % (property[0], property[1]) ,
      name = property[0]
      value = property[1]
      jvmprop = [ ["name", name], ["value", "" + value], ["required", "false"] ]
      sysprops = ["systemProperties", [jvmprop]]      
      found = 0
      curr = AdminConfig.showAttribute(jvm, "systemProperties")
      if len(curr) > 0: propslist = curr[1:-1].split()
      else: propslist = []
      for prop in propslist:
         if name == AdminConfig.showAttribute(prop, 'name'):
            if value == AdminConfig.showAttribute(prop, 'value'):
               print "OK (property already set)"
               found = 1
               break
            else:
               try: 
                  AdminConfig.modify(prop, jvmprop)
                  print "OK (property updated)"
               except:                  
                  type, value, traceback = sys.exc_info()
                  print "KO (ERROR: %s (%s))" % (str(value), type)
                  clearExit("Rollback and exit", -1)
               found = 1
               break                  
      if found == 0:
         try: 
            AdminConfig.modify(jvm, [sysprops])
            print "OK (property added)"
         except:                  
            type, value, traceback = sys.exc_info()
            print "KO (ERROR: %s (%s))" % (str(value), type)
            clearExit("Rollback and exit", -1)
   syncEnv(1)
   print "Property settings done"# end def

def readJDKVersion():
    nodeids = AdminConfig.list('Node').split(lineSeparator)
    nodeName= AdminConfig.showAttribute(nodeids[0],'name')
    lst = AdminTask.getAvailableSDKsOnNode('[-nodeName %s]' %(nodeName)).splitlines()
    str=""
    print "JDK AVAIABLE:"
    for item in lst:
        print " JDK  %s [%s] " %(item,item) 
    print str


def applyJdkVersion():
     nodeids = AdminConfig.list('Node').split(lineSeparator)
     for nodeid in nodeids:
         nodeName= AdminConfig.showAttribute(nodeid,'name')
         serverids = AdminConfig.list('Server',nodeid).split(lineSeparator)
         for serverid in serverids:
             if serverid != '':
                sType = AdminConfig.showAttribute(serverid, "serverType")
                serverName= AdminConfig.showAttribute(serverid,'name')
                if sType == "WEB_SERVER":
                    print "serverName = %s is WebServer " %(serverName)
                if sType == "NODE_AGENT":
                   print "Apply JDK %s to Server %s on Node %s" % (jdkChoose,serverName,nodeName) 
                   AdminTask.setServerSDK('[-nodeName %s -serverName %s -sdkName %s]' % (nodeName,serverName,jdkChoose))
                if sType == "DEPLOYMENT_MANAGER":
                   print "Apply JDK %s to Server %s on Node %s" % (jdkChoose,serverName,nodeName)
                   AdminTask.setServerSDK('[-nodeName %s -serverName %s -sdkName %s]' % (nodeName,serverName,jdkChoose))
                if sType == "APPLICATION_SERVER":
                   print "Apply JDK %s to Server %s on Node %s" % (jdkChoose,serverName,nodeName)
                   AdminTask.setServerSDK('[-nodeName %s -serverName %s -sdkName %s]' % (nodeName,serverName,jdkChoose))
     syncEnv(AdminConfig.hasChanges()) 
# end def


def setupHTTPOnlyCookiesProp(propname, propvalue):
    servers = AdminConfig.list('Server').splitlines()
    for server in servers:
        serverName = getServerName(server)
        if checkIfIsServerTemplate(server) == False:
            NodeName = getNodeNameForServer(server)
            NodeServer = "%s:%s" % (NodeName, serverName)
            (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(NodeServer) 
            if getServerType(nodeName, serverName) != 'NODE_AGENT' and getServerType(nodeName, serverName) != 'WEB_SERVER':
                    log.INFO( "Apply WebContainer properties for server %s .. " % serverName)
                    webcontainer_id = AdminConfig.list('WebContainer', scopeid)
                    setCustomPropertyOnObject(webcontainer_id, propname, propvalue)
    syncEnv(AdminConfig.hasChanges()) 

def setupHTTPOnlyCookiesProps():
    print "Apply Wc com.ibm.ws.webcontainer.HTTPOnlyCookies=*"
    setupHTTPOnlyCookiesProp("com.ibm.ws.webcontainer.HTTPOnlyCookies", "*")

if choose == 'DisableEmbedded':
    disableEmbeddedConfiguration()
    
if choose == 'DisableIPV6':
    disableIPV6()

if choose == 'ApplyEnableSecurityServiceCheck':
    applyEnableSecurityServiceCheck()
    
if choose == 'applyScriptingPatch':
    applyScriptingPatch()
    
if choose == 'applyJdkVersion':
    applyJdkVersion()
    
if choose == 'readJDKVersion':
    readJDKVersion()

if choose == 'setupHTTPOnlyCookiesProps':
    setupHTTPOnlyCookiesProps()
    syncEnv(AdminConfig.hasChanges()) 

if choose == 'setExecutionOwnerWasup':
   setExecutionOwnerWasup()
   syncEnv(AdminConfig.hasChanges())
    
    
    
