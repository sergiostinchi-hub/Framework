# Author:         Andrea Minuto (IBM WebSphere Lab Services)

# Version         Description
#                 Commented line 2146 manageSession for deploy application (target module not corrected)
# 1.3.7           Corrected the retrieve functions when it is present a Description field
# 1.3.6           Corrected the option MapResRefToEJB
#                 Corrected the option BindJndiForEJBBusiness
#                 Corrected the option BindJndiForEJBNonMessageBinding
#                 Corrected the option BindJndiForEJBMessageBinding
#                 Corrected the option MapEJBRefToEJB
#                 Corrected the option CtxRootForWebMod
#                 Corrected the option MapSharedLibForMod
#                 Corrected the option ModuleBuildID
#                 Corrected the option MapModulesToServers
#                 Corrected the option MapEnvEntryForEJBMod
#                 Corrected the option MapEnvEntryForWebMod
#                 Corrected the option MapEnvEntryForApp
#                 Corrected the option MapInitParamForServlet
#                 Corrected the virtualHosts variable syntax
#                 Now it is possible to use .* also when there are more than one web module
#                 Added the option -installed.ear.destination ${APP_INSTALL_ROOT}/${CELL} on INSTALL action
#                 Changed the option metadataComplete meaning and default
#                 Added the variable forceHttpOnly
#                 Added the variable forceSecurityIntegration
#                 Added the variable forceHttpsCookies
# 1.3.5           Modified the UPDATE action syntax
#                 Added the management of pre 3.0 EJB modules
#                 Corrected start application management
#                 Corrected the forceSessionPath configuration
#                 Simplified the INSTALL action syntax
# 1.3.4           Corrected the check of the variable virtualHosts
#                 Added the retrieve of the server version
#                 Added the compatibility with the WebSphere Application Server V6.1.x
#                 Modified the meaning of the variable syncDelay (added the value -1)
#                 Corrected the management of the STANDALONE environment with a web server
#                 Added the -nosave option to run an action without saving
#                 Added the variable servletInitParameters
#                 Corrected the retrieving of web server whose need the plugin generation and propagation
# 1.3.3           Modified the variable resourceReferences syntax
#                 Modified the variable resourceEnvReferences syntax
# 1.3.2           Added the command status to the MANAGE action
# 1.3.1           Added the variable forceUpdateOnly
#                 Added the variable latestChangedFiles
#                 Corrected the check for the file existence
#                 Added variable ejbEnvEntries
#                 Added variable webEnvEntries
#                 Added variable ejbInterfacesBindings
#                 Added variable ejbBindings
#                 Added variable mdbBindings
#                 Added variable ejbReferences
#                 Added variable appEnvEntries
#                 Added variable ejbAutoLink
#                 Enhanced printTargetServers function
#                 Added variable forceSessionPath
# 1.3.0           Added the variable syncDelay
#                 Deleted the variable virtualHost
#                 Added the variable virtualHosts
#                 Added the variable updateContentType
#                 Added the variable updateContentURI
#                 Added REMOVE action
#                 Enhanced the UPDATE action to allow the update of a single file, module o partial applicazion file
#                 Added MANAGE action in order to start, stop or restart an application to specific targets
#                 Added variable startingWeight
#                 Added variable warClassLoaderPolicy
#                 Added variable createNewServicePolicy
#                 Added the variable targetObjects
#                 Deleted the variable targetClusters
#                 Deleted the variable targetServers
#                 Deleted the variable targetWebServers
#                 Enhanced the STANDALONE management
#                 Enhanced reading of configuration variables from Java property files
#                 Enhanced and corrected starting of applications after first installation
#                 Added tha action UNINSTALL for the variable propagationPlugin
# 1.2.6           Added Web Application (WAR) management
#                 Added shared library management
#                 Corrected some checks for the EDIT action
#                 Enhanced the check of the variable applicationRoles
#                 Added the variable sharedLibraries
# 1.2.5           Added the variable appClassloader
#                 Corrected the command line check
# 1.2.4           Modified the ROLLOUT action to allow the configuration file management
#                 Added the -long options for the VERSION action
# 1.2.3           Added the variable drainageInterval
#                 Changed the method time.time() with the more precise time.clock()
#                 Corrected the WebServer management for the EDIT action
# 1.2.2           Added the variable scaSCABindings and relative management
#                 Added the variable scaEJBBindings and relative management
# 1.2.1           Added EDIT action
#                 Corrected mapping modules to servers for the actions INSTALL and UPDATE
#                 Corrected Plug-in Propagation
# 1.2.0           Modified and strongly simplified the variable resourceReferences
#                 Modified and strongly simplified the variable resourceEnvReferences
#                 Modified and simplified the variable contextRoots
#                 Added AdminApp.isAppReady(appName) check before trying to start an application
# 1.1.2           Added variable scaModuleProperties and relative management
#                 Corrected resource references and resource environment references settings
# 1.1.0           Changed script name from installApp to adminApp
#                 Added EDITION, VERSION and ROLLOUTEDITION actions
#                 Added extraOptions variable
# 1.0.8           Added ACTIVATE and DEACTIVATE command for action
# 1.0.7           Added support to EJB classes inside a WAR file
# 1.0.6           Added elapsed time management
#                 Added simplified application edition management
#                 Modified command line parameters
#                 Added Resource Environment References management
#                 Added Resource References Management
# 1.0.5           Added Business Process and Human Task management
#                 Added update of validFrom attribute during installation or update
#                 Added Policy Set Attachment and Binding management
# 1.0.4           Added profile management and acknowledgement
#                 Added build version
#                 Added generation and propagation plug-in management
#                 Added Java property files management
# 1.0.3           Added more installation and update options
# 1.0.2           Added start application management
# 1.0.1           Added SCA Modules management
# 1.0.0           Starting version

# Import
import sys
import os
import time
from java.io import FileInputStream
from java.util import Properties
from java.lang import System



# VERSION
version = "1.3.7-2"

# Script variables
propertyPrefix = "com.ibm.adminapp"
scriptName = "adminApp.py"

# Auxiliary Variables
needPropagation = 'false'
postSaveActions = 'false'
targetModules = []
allModules = []
virtualHostsActual = []
contextRootsActual = []
sharedLibrariesActual = []
resourceRefActual = []
resourceEnvRefActual = []
ejbEnvEntriesActual = []
webEnvEntriesActual = []
ejbInterfaceBindingsActual = []
ejbBindingsActual = []
mdbBindingsActual = []
ejbReferencesActual = []
appEnvEntriesActual = []
autoLinkActual = []
servletInitParametersActual = []

# Configuration Variables (alphabetical order)
appClassloader = 'PARENT_FIRST'     # Optional: The caluse must be 'PARENT_FIRST' or 'PARENT_LAST' (INSTALL, UPDATE, EDIT, ROLLOUT) - Default = 'PARENT_FIRST'
appEnvEntries = []                  # Optional: List of [<entry name>, <value>] (INSTALL, UPDATE, EDIT, ROLLOUT)
applicationRoles = []               # Optional: list of [<role name> <Everyone ['Yes', 'No']> <All Authenticated ['Yes', 'No']> <users>, <groups>] (INSTALL, UPDATE, EDIT, ROLLOUT)
contextRoots = []                   # Optional: List of [<web module name>|.*, <context root>] (INSTALL, UPDATE, EDIT, ROLLOUT)
createNewServicePolicy = 'false'    # Optional: Create a new service policy associated to the application and set the Default_HTTP_WC to this new service policy (Virtual Enterprise or Intelligent Management) (INSTALL)
drainageInterval = 30               # Optional: Rollout Drainage Interval (Virtual Enterprise or Intelligent Management) - The valid range is: [1, 300] (ROLLOUTEDITION)
edition = ''                        # Optional: Application Edition (Virtual Enterprise or Intelligent Management) (INSTALL, UPDATE, UNINSTALL, EDIT, ROLLOUT, REMOVE) - Mandatory: (ACTIVATE, DEACTIVATE, ROLLOUTEDITION)
editionDesc = ''                    # Optional: Application Edition Description (Virtual Enterprise or Intelligent Management) (INSTALL)
ejbAutoLink = 'true'                # Optional: Flag to specify whether to automatically resolve Enterprise JavaBeans (EJB) references from EJB module (INSTALL, UPDATE, EDIT, ROLLOUT)
ejbBindings = []                    # Optional: List of [<module>, <ejb name>, <target jndi name>, <local home jndi>, <remote home jndi>] (INSTALL, UPDATE, EDIT, ROLLOUT)
ejbEnvEntries = []                  # Optional: List of [<module>, <ejb name>, <entry name>, <value>] (INSTALL, UPDATE, EDIT, ROLLOUT)
ejbInterfaceBindings = []           # Optional: List of [<module>, <ejb name>, <business interface>, <jndi name>] (INSTALL, UPDATE, EDIT, ROLLOUT)
ejbReferences = []                  # Optional: List of [<ejb reference>, <jndi>] (INSTALL, UPDATE, EDIT, ROLLOUT)
extraOptions = []                   # Optional: Extra Parameters following the AdminApp.install() rules (INSTALL, UPDATE, EDIT, ROLLOUT)
forceHttpOnly = 'true'              # Optional: Flag to force the JSESSIONID HTTPOnly cookie attribute for the application and all the application web modules (INSTALL, UPDATE, EDIT, ROLLOUT)
forceHttpsCookies = 'false'         # Optional: Flag to force the cookies to be set only when in HTTPS for the application and all the application web modules (INSTALL, UPDATE, EDIT, ROLLOUT)
forceSecurityIntegration = 'false'  # Optional: Flag to force the session security integration for the application and all the application web modules (INSTALL, UPDATE, EDIT, ROLLOUT)
forceSessionPath = 'false'          # Optional: Flag to force the JSESSIONID cookie path to the context root of all the application web modules (INSTALL, UPDATE, EDIT, ROLLOUT)
forceUpdateOnly = 'false'           # Optional: Flag to force only a resource updating. Useful only when updateContentType != 'app'. (UPDATE)
latestChangedFiles = []             # Optional: List of [<resource uri>, <file path>] (INSTALL, UPDATE, EDIT, ROLLOUT)
mdbBindings = []                    # Optional: List of [<module>, <mdb name>, <activation specification jndi>] (INSTALL, UPDATE, EDIT, ROLLOUT)
metadataComplete = 'true'           # Optional: (INSTALL, UPDATE, EDIT, ROLLOUT)
propagatePlugin = 'false'           # Optional: (INSTALL, UPDATE, EDIT, ROLLOUT, REMOVE, UNINSTALL)
resourceEnvReferences = []          # Optional: List of [<reference jndi>|[<session bean>|<war name>, <reference jndi>], <target jndi>] (INSTALL, UPDATE, EDIT, ROLLOUT)
resourceReferences = []             # Optional: List of [<reference jndi>|[<session bean>|<war name>, <reference jndi>], <target jndi>] (INSTALL, UPDATE, EDIT, ROLLOUT)
rolloutGroupSize = 1                # Optional: Rollout Edition Group Size (Virtual Enterprise or Intelligent Management) (ROLLOUTEDITION)
rolloutResetStrategy = 'hard'       # Optional: Rollout Edition Reset Strategy (Virtual Enterprise or Intelligent Management) - The valid values are: 'hard', 'soft' (ROLLOUTEDITION)
rolloutStrategy = 'grouped'         # Optional: Rollout Edition Strategy (Virtual Enterprise or Intelligent Management) - The valid values are: 'grouped', 'atomic' (ROLLOUTEDITION)
scaEJBBindings = []                 # Optional: List of [<module name>, <import name>, <target jndi name>] (Business Process Management, Enterprise Service Bus) (INSTALL, UPDATE, EDIT, ROLLOUT)
scaModuleProperties = []            # Optoinal: List of [<module name>, <property name>, <group name>|'', <value>] (Business Process Management, Enterprise Service Bus) (INSTALL, UPDATE, EDIT, ROLLOUT)
scaSCABindings = []                 # Optional: List of [<module name>, <import name>, <target module name> <target export name>, <target application name>|'']
                                    #          (Business Process Management, Enterprise Service Bus) (INSTALL, UPDATE, EDIT, ROLLOUT)
scaWSBindings = []                  # Optional: List of [<module name>, <import name>, <target endpoint>] (Business Process Management, Enterprise Service Bus) (INSTALL, UPDATE, EDIT, ROLLOUT)
servletInitParameters = []          # Optional: List of [<web module>, <servlet name>, <init parameter name>, <value>] (INSTALL, UPDATE, EDIT, ROLLOUT)
sharedLibraries = []                # Optional: List of [<module name>|.*, <shared library name>] (INSTALL, UPDATE, EDIT, ROLLOUT)
startApplication = 'false'          # Optional: (INSTALL)
startingWeight = 1                  # Optional: Specifies the order in which applications are started when the server starts. The application with the lowest starting weight is started first (INSTALL, UPDATE, EDIT, ROLLOUT)
syncDelay = 0                       # Optional: Delay in seconds between two node synchronizations - The valid range is [-1, 20] and only for DISTRIBUTED environments (INSTALL, UPDATE, EDIT, REMOVE)
targetObjects = []                  # Mandatory: DISTRIBUTED - List of <target> (INSTALL, UPDATE, EDIT, ROLLOUT)
                                    #            <target> :: = <server>|<cluster>|<webserver>|list of <module> and list of <server>|<cluster>|<webserver>
                                    #            <server> :: = [<node name>:]<server name>
                                    #            <webserver> :: = [<node name>:]<web server name>
                                    #            Sample: [ 'Server1', [ ['Module1', 'Module2'], ['Cluster1', 'Server2', 'WebServer1'] ], 'Cluster2', [ ['Module3', 'Module4'], ['WebServer2'] ] ]
                                    # Optional: STANDALONE
timeoutRollout = 100                # Optional: (ROLLOUT)
virtualHosts = []                   # Optional: List of [<web module name>|.*, <virtual host>] (INSTALL, UPDATE, EDIT, ROLLOUT)
updateContentType = 'app'           # Optional: The kind of file passed - The valid values are ['app', 'file', 'modulefile', 'partialapp'] (UPDATE) - Mandatory: The valid values are ['file', 'modulefile'] (REMOVE)
updateContentURI = ''               # Optional: The URI of the file that you are updating or removing from an application (UPDATE, REMOVE)
                                    # Mandatory: (UPDATE when updateConentType != 'app', REMOVE when updateConentType in ['file', 'modulefile'])
updateValidationDate = 'false'      # Optional: 'true' = update validation date for the business processes and human tasks (Business Process Management) (INSTALL, UPDATE, EDIT, ROLLOUT)
warClassLoaderPolicy = 'MULTIPLE'   # Optional: Specifies whether to use a single class loader to load all WAR files of the application or to use a different class loader for each WAR file.
                                    #           The valid values are: 'MULTIPLE', 'SINGLE' (INSTALL, UPDATE, EDIT, ROLLOUT)
webEnvEntries = []                  # Optional: List of [<web module>, <entry name>, <value>] (INSTALL, UPDATE, EDIT, ROLLOUT)
wsPolicySets = []                   # Optional: List of [<attachment type ['provider', 'client']>, <policy set name>, <binding name>|'', <resources>] (INSTALL, UPDATE, EDIT, ROLLOUT)

# Start Execution
startt = time.clock()

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   print "Elapsed Time: %.3f s" % (time.clock() - startt)
   print "%s done" % scriptName
   sys.exit(status)
   return

def clearAppAndExit(appName):
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   print "Uninstallation ot the application %s ..." % appName
   try: 
      AdminApp.uninstall(appName)
      AdminConfig.save()
      print "SUCCESS: Uninstallation ot the application %s completed successfully" % appName
   except:
      print "ERROR: Uninstallation ot the application %s failed" % appName
      print "WARNING: The application %s needs to be manually uninstalled" % appName

   print "Elapsed Time: %.3f s" % (time.clock() - startt)
   print "%s done" % scriptName
   sys.exit(-1)
   return

def getVersion(appName):
   try:
      output = AdminApp.view(appName, '-buildVersion')
      beg = output.find(':')
      if beg != -1: data = output[beg + 1:].strip()
      else: data = 'N/A'
   except: 
      data = 'N/A'
   return data

def prepareClusters(clusters):
   cellName = AdminConfig.showAttribute(AdminConfig.getid('/Cell:/'), 'name')
   data = ''
   for cluster in clusters:
     if len(data) > 0: data += '+'
     data += 'WebSphere:cell=%s,cluster=%s' % (cellName, cluster)
   return data

def prepareServers(servers):
   cellName = AdminConfig.showAttribute(AdminConfig.getid('/Cell:/'), 'name')
   data = ''
   for server in servers:
      beg = server.find(':')
      if beg != -1:
         appserver = server[beg + 1:]
         node = server[:beg]
         if len(data) > 0: data += '+'
         data += 'WebSphere:cell=%s,node=%s,server=%s' % (cellName, node, appserver)
      else:
         ids = AdminConfig.getid('/Server:%s/' % server).splitlines()
         for id in ids:
            appserver = server
            beg = id.find('/nodes/') + len('/nodes/')
            end = id.find('/', beg)
            node = id[beg:end]
            if len(data) > 0: data += '+'
            data += 'WebSphere:cell=%s,node=%s,server=%s' % (cellName, node, appserver)
   return data

def hasBPELComponents(appName):
   try:
      # Business Processes
      if len(AdminConfig.types('ProcessComponent')) > 0:
         bpels = AdminConfig.list('ProcessComponent').splitlines()
         for bpel in bpels: 
            if bpel.find('/%s|' % appName) != -1:
               return 'true'
         
      # Human Tasks
      if len(AdminConfig.types('TaskComponent')) > 0:
         htasks = AdminConfig.list('TaskComponent').splitlines()
         for htask in htasks: 
            if htask.find('/%s|' % appName) != -1:
               return 'true'
   
   # Capability not present
   except: pass
   
   # No BPEL Components
   return 'false'

def updateBPELValidationDate(appName):
   # Timestamp
   current = System.currentTimeMillis()
   
   # Business Processes
   bpels = AdminConfig.list('ProcessComponent').splitlines()
   for bpel in bpels: 
      if bpel.find('/%s|' % appName) != -1:
         AdminConfig.modify(bpel, [ ['validFrom', str(current)] ])
   
   # Human Tasks
   htasks = AdminConfig.list('TaskComponent').splitlines()
   for htask in htasks: 
      if htask.find('/%s|' % appName) != -1: 
         AdminConfig.modify(htask, [ ['validFrom', current] ])

def getTargets(appName):
   ret = []
   targets = AdminApp.view(appName, '[-MapModulesToServers]')
   beg = 0
   while (1):
      pos = targets.find('Server:', beg)
      if pos == -1: break
      pos += len('Server:')
      end = targets.find(lineSeparator, pos)
      if end != -1: target = targets[pos:end].strip()
      else: target = targets[pos:].strip()
      beg = end
      pos = 0
      while (1):
         end = target.find('+', pos)
         if end != -1:
            item = target[pos:end]
            pos = end + 1
            if item not in ret: ret.append(item)
            continue
         else:
            item = target[pos:]
            if item not in ret: ret.append(item)
            break
   i = 0
   while i < len(ret):
      item = ret[i]
      if item.find(',server=') != -1:
         beg = item.find(',node=') + len(',node=')
         end = item.find(',', beg)
         node = item[beg:end]
         server = item[item.find(',server=') + len(',server='):]
         id = AdminConfig.getid('/Node:' + node + '/Server:' + server + '/')
         if AdminConfig.showAttribute(id, 'serverType') == 'WEB_SERVER': ret.remove(item)
         else: i += 1
      else: i += 1
   return ret

def retrieveReferences(appLocation, action, env):
   ret = []
   if action == 'EDIT':
      if env == 'true': taskInfo = AdminApp.view(appLocation, ['-MapResEnvRefToRes'])
      else: taskInfo = AdminApp.view(appLocation, ['-MapResRefToEJB'])
   else:
      if env == 'true': taskInfo = AdminApp.taskInfo(appLocation, 'MapResEnvRefToRes')
      else: taskInfo = AdminApp.taskInfo(appLocation, 'MapResRefToEJB')
   pos = taskInfo.find('Module:')
   while (pos != -1):
      pos += len('Module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # Bean or EJB
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      bean = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(':', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Resource Reference
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      resref = taskInfo[pos:end].strip()
      
      # Resource type
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      restype = taskInfo[pos:end].strip()
      
      # Target Resource JNDI Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      resjndi = taskInfo[pos:end].strip()
      
      # Append
      if env == 'true': ret.append([ module, bean, uri, resref, restype, resjndi])
      else: ret.append([module, bean, uri, resref, restype, resjndi, '', '', ''])
      pos = taskInfo.find('Module:', end)
      
   return ret

def retrieveVirtualHosts(appLocation, action):
   ret = retrieveContextRoots(appLocation, action)
   return ret

def retrieveContextRoots(appLocation, action):
   ret = []
   if action == 'EDIT': taskInfo = AdminApp.view(appLocation, ['-CtxRootForWebMod'])
   else: taskInfo = AdminApp.taskInfo(appLocation, 'CtxRootForWebMod')
   pos = taskInfo.find('Web module:')
   while (pos != -1):
      pos += len('Web module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Context Root
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      if end != -1: context = taskInfo[pos:end].strip()
      else: context = taskInfo[pos:].strip()
      
      # Append
      ret.append([module, uri, context])
      pos = taskInfo.find('Web module:', end)
   
   return ret

def retrieveSharedLibraries(appLocation, action):
   ret = []
   if action == 'EDIT': taskInfo = AdminApp.view(appLocation, ['-MapSharedLibForMod'])
   else: taskInfo = AdminApp.taskInfo(appLocation, 'MapSharedLibForMod')
   pos = taskInfo.find('Module:')
   while (pos != -1):
      pos += len('Module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Append
      ret.append([module, uri, ''])
      pos = taskInfo.find('Module:', end)
   
   return ret

def retrieveRoles(appLocation, action):
   ret = []
   if action == 'EDIT': taskInfo = AdminApp.view(appLocation, ['-MapRolesToUsers'])
   else: taskInfo = AdminApp.taskInfo(appLocation, 'MapRolesToUsers')
   pos = taskInfo.find('Role:')
   while (pos != -1):
      pos += len('Role:')
      end = taskInfo.find(lineSeparator, pos)
      role = taskInfo[pos:end].strip()
      ret.append(role)
      pos = taskInfo.find('Role:', end)
   return ret

def separeTargets(targets):
   ret = []
   pos = 0
   while (1):
      end = targets.find('+', pos)
      if end != -1:
         item = targets[pos:end]
         pos = end + 1
         if item not in ret: ret.append(item)
         continue
      else:
         item = targets[pos:]
         if item not in ret: ret.append(item)
         break
   return ret

def retrieveBuildId(appName):
   ret = []
   taskInfo = AdminApp.view(appName, ['-ModuleBuildID'])
   pos = taskInfo.find('Module:')
   while (pos != -1):
      pos += len('Module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Build ID
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)      
      if end != -1: buildId = taskInfo[pos:end].strip()
      else: buildId = taskInfo[pos:].strip()
      
      # Append
      ret.append([ module, uri, buildId])
      pos = taskInfo.find('Module:', end)
   
   return ret

def printTargetServers(appName):
   try: buildIds = retrieveBuildId(appName)
   except: buildIds = []
   output = AdminApp.view(appName, ['-MapModulesToServers'])
   beg = output.find('Module:')
   if beg == -1:
      print "No modules found in the application %s" % appName
      return
   while beg != -1:
      beg += len('Module:')
      end = output.find(lineSeparator, beg)
      if end != -1: module = output[beg:end].strip()
      else: module = output[beg:].strip()
      beg = output.find('URI:', end)
      beg += len('URI:')
      end = output.find(lineSeparator, beg)
      if end != -1: uri = output[beg:end].strip()
      else: uri = output[beg:].strip()
      if uri.endswith('web.xml') == 1: mtype = 'WAR'
      elif uri.endswith('ejb-jar.xml') == 1: mtype = 'EJB'
      else: mtype = 'N/A'
      beg = output.find('Server:', end)
      if beg == -1: continue
      end = output.find(lineSeparator, beg)
      if end != -1: targets = output[beg:end].strip()
      else: targets = output[beg:].strip()
      if len(targets) == 0: continue
      listTarget = separeTargets(targets)
      first = 1
      data = '%s (%s): ' % (module, mtype)
      for buildId in buildIds:
         if buildId[0] == module and \
            len(buildId[2]) > 0:
            data += '%s (Build Id)' % buildId[2]
            first = 0
      for target in listTarget:
         #print "1 - Target == %s " %(target)
         if first == 1: first = 0
         else: data += ', '
         if target.find(',server=') != -1:
            begl = target.find(',node=') + len(',node=')
            endl = target.find(',', begl)
            node = target[begl:endl]
            server = target[target.find(',server=') + len(',server='):]
            id = AdminConfig.getid('/Node:' + node + '/Server:' + server + '/')
            if AdminConfig.showAttribute(id, 'serverType') == 'WEB_SERVER':
               data += '%s/%s (WebServer)' % (node, server)
            else:
               data += '%s/%s (Application Server)' % (node, server)
         elif target.find(',cluster=') != -1:
            print "Target Cluster== %s " %(target)
            #listStr = str(target).split(",")
            #for dummy in listStr:
                #print dummy
            #    if dummy.find("cluster=")!=-1:
            #        cluster = dummy
            #        break
            cluster = target[target.find(',cluster=') + len(',cluster:'):]
            data += '%s (Cluster)' % cluster
         else: nop
      print data
      beg = output.find('Module:', end)

def setAppClassLoader(appName, mode):
   dep = AdminConfig.getid('/Deployment:%s/' % appName)
   if len(dep) == 0: return
   depObject = AdminConfig.showAttribute(dep, 'deployedObject')
   if len(depObject) == 0: return
   classloader = AdminConfig.showAttribute(depObject, 'classloader')
   AdminConfig.modify(classloader, [ ['mode', mode] ])

def getApplicationDeployment(appName, edition):
   tempName = appName
   if len(edition) > 0: tempName += '-edition%s' % edition
   appdepids = AdminConfig.list('ApplicationDeployment').splitlines()
   for appdepid in appdepids:
      if appdepid.find('/%s|' % tempName) != -1:
         return appdepid
   return ''

def createServicePolicy(appName, edition):
   spid = AdminConfig.getid('/ServiceClass:%s_SP/' % appName)
   if len(spid) == 0:
      cellid = AdminConfig.list("Cell")
      spid = AdminConfig.create('ServiceClass', cellid, [ ['name', '%s_SP' % appName], ['description', 'Service Policy for application %s' % appName] ])
      scid = AdminConfig.create('DiscretionaryGoal', spid, [ ['importance' , 1] ], 'ServiceClassGoal')
   tempName = appName
   if len(edition) > 0: tempName += '-edition%s' % edition
   wcids = AdminConfig.getid('/WorkClass:Default_HTTP_WC/').splitlines()
   for wcid in wcids:
      if wcid.find('/%s/' % tempName) != -1:
         AdminConfig.modify(wcid, [ ['matchAction', 'Default_TC_%s_SP' % appName] ])
         break

def removeServicePolicy(appName):
   try: spid = AdminConfig.getid('/ServiceClass:%s_SP/' % appName)
   except: return
   if len(spid) > 0: 
      wcids = AdminConfig.getid('/WorkClass:Default_HTTP_WC/').splitlines()
      for wcid in wcids: 
         if wcid.find('/%s-edition' % appName) != -1: return
      AdminConfig.remove(spid)

def retrieveModules(appLocation, action):
   ret = []
   modules = []
   if action == 'EDIT': taskInfo = AdminApp.view(appLocation, ['-MapModulesToServers'])
   else: taskInfo = AdminApp.taskInfo(appLocation, 'MapModulesToServers')
   pos = taskInfo.find('Module:')
   while (pos != -1):
      pos += len('Module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)      
      uri = taskInfo[pos:end].strip()
      
      if action == 'EDIT':
         pos = taskInfo.find('Server:', end)
         pos += len('Server:')
         end = taskInfo.find(lineSeparator, pos)
         if end == -1: server = taskInfo[pos:].strip()
         else: server = taskInfo[pos:end].strip()
         ret.append([module, uri, server])
      else:
         ret.append([module, uri, ''])
      
      # Append
      modules.append(module)
      if end == -1: break;
      pos = taskInfo.find('Module:', end)
   
   return (ret, modules)

def findTarget(target):
   print " findTarget = %s " %(target)
   target = target.strip()
   if target.find(':') != -1:
      sep = target.find(':')
      node = target[:sep]
      server = target[sep + 1:]
      serverid = AdminConfig.getid('/Node:%s/Server:%s' % (node, server))
      if len(serverid) == 0: return 'E', "The target %s doesn't exist" % target
   else:
      clusterid = AdminConfig.getid('/ServerCluster:%s/' % target)
      print "clusterid ! = %s" %(clusterid)
      if len(clusterid) > 0:
         data = prepareClusters([target])
         return 'C', data
      serverids = AdminConfig.getid('/Server:%s/' % target).splitlines()
      if len(serverids) == 0: return 'E', "The target %s doesn't exist" % target
      if len(serverids) > 1: return 'E', "The target %s is ambiguous cause there are %d objects with the same name" % (target, len(serverids))
      serverid = serverids[0]
   serverType = AdminConfig.showAttribute(serverid, 'serverType')
   if serverType == 'WEB_SERVER':
      data = prepareServers([target])
      return 'W', data
   elif serverType == 'APPLICATION_SERVER':
      try: 
         clusterName = AdminConfig.showAttribute(serverid, 'clusterName')
         if clusterName != None: return 'E', "The target %s is a member of the cluster %s and cannot be a standalone target" % (target, clusterName)
      except: pass
      data = prepareServers([target])
      return 'A', data
   else: return 'E', "The target %s cannot be used as a target for the application" % target

def addTarget(modules, ttype, target, onlymodules):
   for module in modules:
      if len(onlymodules) > 0 and module[0] not in onlymodules: continue
      if module[1].find('/web.xml') == -1 and ttype == 'W': continue
      if module[2].find(target) > 0: return
      if len(module[2]) > 0: module[2] += '+%s' % target
      else: module[2] = target

def findModule(module, targetModules):
   for tmodule in targetModules:
      if module == tmodule[0]: return 1
   return 0

def hasServers(targets):
   ltargets = targets.split('+')
   for target in ltargets:
      if target.find('cluster=') != -1: return 1
      beg = target.find('node=') + len('node=')
      end = target.find(',', beg)
      node = target[beg:end]
      server = target[target.find('server=') + len('server='):]
      serverid = AdminConfig.getid('/Node:%s/Server:%s' % (node, server))
      serverType = AdminConfig.showAttribute(serverid, 'serverType')
      if serverType == 'APPLICATION_SERVER': return 1
   return 0

def hasWebServers(targets):
   ltargets = targets.split('+')
   for target in ltargets:
      if target.find('cluster=') != -1: return 1
      beg = target.find('node=') + len('node=')
      end = target.find(',', beg)
      node = target[beg:end]
      server = target[target.find('server=') + len('server='):]
      serverid = AdminConfig.getid('/Node:%s/Server:%s' % (node, server))
      serverType = AdminConfig.showAttribute(serverid, 'serverType')
      if serverType == 'WEB_SERVER': return 1
   return 0

def getWebServers(modules):
   ret = []
   for module in modules:
      if module[1].find('/web.xml') == -1: continue
      targets = module[2].split('+')
      for target in targets:
         if target.find('cluster=') != -1: continue
         beg = target.find('node=') + len('node=')
         end = target.find(',', beg)
         node = target[beg:end]
         server = target[target.find('server=') + len('server='):]
         serverid = AdminConfig.getid('/Node:%s/Server:%s' % (node, server))
         serverType = AdminConfig.showAttribute(serverid, 'serverType')
         if serverType == 'WEB_SERVER' and [node, server] not in ret: ret.append([node, server])
   return ret

def getSingleList(aList, index):
   ret = []
   for item in aList: ret.append(item[index])
   return ret

def getTuple(aList, iList):
   ret = []
   for item in aList:
      sitem = []
      for i in iList: sitem.append(item[i])
      ret.append(sitem)
   return ret

def retrieveEJBEnvEntries(appLocation, action):
   ret = []
   if action == 'EDIT':
      taskInfo = AdminApp.view(appLocation, ['-MapEnvEntryForEJBMod'])
   else:
      taskInfo = AdminApp.taskInfo(appLocation, 'MapEnvEntryForEJBMod')
   pos = taskInfo.find('Module:')
   while (pos != -1):
      pos += len('Module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Bean
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      bean = taskInfo[pos:end].strip()
      
      # Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      name = taskInfo[pos:end].strip()
      
      # Type
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      envtype = taskInfo[pos:end].strip()
      
      # Description
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find('Value: ', pos)
      description = taskInfo[pos:end - len(lineSeparator)].strip()
      
      # Value
      pos = taskInfo.find('Value: ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      if end != -1: value = taskInfo[pos:end].strip()
      else: value = taskInfo[pos:].strip()
      
      # Append
      ret.append([ module, uri, bean, name, envtype, description, value])
      if end == -1: break;
      pos = taskInfo.find('Module:', end)
   
   return ret

def retrieveWebEnvEntries(appLocation, action):
   ret = []
   if action == 'EDIT':
      taskInfo = AdminApp.view(appLocation, ['-MapEnvEntryForWebMod'])
   else:
      taskInfo = AdminApp.taskInfo(appLocation, 'MapEnvEntryForWebMod')
   pos = taskInfo.find('Web module:')
   while (pos != -1):
      pos += len('Web module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      name = taskInfo[pos:end].strip()
      
      # Type
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      envtype = taskInfo[pos:end].strip()
      
      # Description
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find('Value: ', pos)
      description = taskInfo[pos:end - len(lineSeparator)].strip()
      
      # Value
      pos = taskInfo.find('Value: ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      if end != -1: value = taskInfo[pos:end].strip()
      else: value = taskInfo[pos:].strip()
      
      # Append
      ret.append([ module, uri, name, envtype, description, value])
      if end == -1: break;
      pos = taskInfo.find('Web module:', end)
   
   return ret

def retrieveEJBInterfaces(appLocation, action):
   ret = []
   if action == 'EDIT': taskInfo = AdminApp.view(appLocation, ['-BindJndiForEJBBusiness'])
   else: taskInfo = AdminApp.taskInfo(appLocation, 'BindJndiForEJBBusiness')
   pos = taskInfo.find('Module:')
   while (pos != -1):
      pos += len('Module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # Bean or EJB
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      bean = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Business interface
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      interface = taskInfo[pos:end].strip()
      
      # JNDI Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      if end != -1: jndi = taskInfo[pos:end].strip()
      else: jndi = taskInfo[pos:].strip()
      
      # Append
      ret.append([ module, bean, uri, interface, jndi])
      if end == -1: break
      pos = taskInfo.find('Module:', end)
   
   return ret

def retrieveEJBs(appLocation, action):
   ret = []
   if action == 'EDIT':
      taskInfo = AdminApp.view(appLocation, ['-BindJndiForEJBNonMessageBinding'])
   else:
      taskInfo = AdminApp.taskInfo(appLocation, 'BindJndiForEJBNonMessageBinding')
   pos = taskInfo.find('EJBModule:')
   while (pos != -1):
      pos += len('EJBModule:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # EJB or Bean
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      bean = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Target Resource JNDI Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      target = taskInfo[pos:end].strip()
      
      # Local Home JNDI Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      local = taskInfo[pos:end].strip()
      
      # Remote Home JNDI Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      if end != -1: remote = taskInfo[pos:end].strip()
      else: remote = taskInfo[pos:].strip()
      
      # Append
      ret.append([ module, bean, uri, target, local, remote])
      if end == -1: break;
      pos = taskInfo.find('EJBModule:', end)
   
   return ret

def retrieveMDBs(appLocation, action):
   ret = []
   if action == 'EDIT':
      taskInfo = AdminApp.view(appLocation, ['-BindJndiForEJBMessageBinding'])
   else:
      taskInfo = AdminApp.taskInfo(appLocation, 'BindJndiForEJBMessageBinding')
   pos = taskInfo.find('EJBModule:')
   while (pos != -1):
      pos += len('EJBModule:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # EJB or Bean
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      bean = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Listener port
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      listener = taskInfo[pos:end].strip()
      
      # JNDI Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      name = taskInfo[pos:end].strip()
      
      # Destination JNDI Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      destination = taskInfo[pos:end].strip()
      
      # ActivationSpec Authentication Alias
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      if end != -1: activation = taskInfo[pos:end].strip()
      else: activation = taskInfo[pos:].strip()
      
      # Append
      ret.append([ module, bean, uri, listener, name, destination, activation])
      if end == -1: break;
      pos = taskInfo.find('EJBModule:', end)
   
   return ret

def retrieveEJBReferences(appLocation, action):
   ret = []
   if action == 'EDIT':
      taskInfo = AdminApp.view(appLocation, ['-MapEJBRefToEJB'])
   else:
      taskInfo = AdminApp.taskInfo(appLocation, 'MapEJBRefToEJB')
   pos = taskInfo.find('Module:')
   while (pos != -1):
      pos += len('Module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # Bean or EJB
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      bean = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Resource Reference
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      reference = taskInfo[pos:end].strip()
      
      # Class
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      classname = taskInfo[pos:end].strip()
      
      # Target Resource JNDI Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      if end != -1: target = taskInfo[pos:end].strip()
      else: target = taskInfo[pos:].strip()
      
      # Append
      ret.append([ module, bean, uri, reference, classname, target])
      if end == -1: break;
      pos = taskInfo.find('Module:', end)
   
   return ret

def retrieveAppEnvEntries(appLocation, action):
   ret = []
   if action == 'EDIT':
      taskInfo = AdminApp.view(appLocation, ['-MapEnvEntryForApp'])
   else:
      taskInfo = AdminApp.taskInfo(appLocation, 'MapEnvEntryForApp')
   pos = taskInfo.find('Name:')
   while (pos != -1):
      pos += len('Name:')
      end = taskInfo.find(lineSeparator, pos)
      name = taskInfo[pos:end].strip()
      
      # Type
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      typename = taskInfo[pos:end].strip()
      
      # Description
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find('Value: ', pos)
      description = taskInfo[pos:end - len(lineSeparator)].strip()
      
      # Value
      pos = taskInfo.find('Value: ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      if end != -1: value = taskInfo[pos:end].strip()
      else: value = taskInfo[pos:].strip()
      
      # Append
      ret.append([ name, typename, description, value])
      if end == -1: break;
      pos = taskInfo.find('Name:', end)
   
   return ret

def retrieveServletInitParameters(appLocation, action):
   ret = []
   if action == 'EDIT':
      taskInfo = AdminApp.view(appLocation, ['-MapInitParamForServlet'])
   else:
      taskInfo = AdminApp.taskInfo(appLocation, 'MapInitParamForServlet')
   pos = taskInfo.find('Web module:')
   while (pos != -1):
      pos += len('Web module:')
      end = taskInfo.find(lineSeparator, pos)
      module = taskInfo[pos:end].strip()
      
      # URI
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      uri = taskInfo[pos:end].strip()
      
      # Servlet
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      servlet = taskInfo[pos:end].strip()
      
      # Name
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find(lineSeparator, pos)
      name = taskInfo[pos:end].strip()
      
      # Description
      pos = taskInfo.find(': ', end)
      if pos == -1: return []
      else: pos += 2
      end = taskInfo.find('Value: ', pos)
      description = taskInfo[pos:end - len(lineSeparator)].strip()
      
      # Value
      pos = taskInfo.find('Value: ', end)
      if pos == -1: return []
      else: pos += 7
      end = taskInfo.find(lineSeparator, pos)
      if end != -1: value = taskInfo[pos:end].strip()
      else: value = taskInfo[pos:].strip()
      
      # Append
      ret.append([ module, uri, servlet, name, description, value])
      if end == -1: break;
      pos = taskInfo.find('Web module:', end)
   
   return ret

def findTargetSessionManager(appName, module):
   modules = AdminApp.view(appName, '-MapModulesToServers')
   if len(modules) == 0: return ''
   start = modules.find(' %s' % module)
   if start == -1: return ''
   beg = modules.find('Server:', start) + len('Server:')
   end = modules.find(lineSeparator, beg)
   targets = modules[beg:end].strip().split('+')
   if len(targets) == 0: return ''
   for target in targets:
      s1 = target.find('server=')
      if s1 != -1:
         server = target[s1 + 7:]
         n1 = target.find('node=')
         node = target[n1 + 5 : s1 - 1]
         serverid = AdminConfig.getid('/Node:%s/Server:%s/' % (node, server))
         if len(serverid) == 0: continue
         serverType = AdminConfig.showAttribute(serverid, 'serverType')
         if serverType != 'APPLICATION_SERVER': continue
         return AdminConfig.list('SessionManager', serverid)
      c1 = target.find('cluster=')
      if c1 != -1:
         cluster = target[c1 + 8:]
         clusterid = AdminConfig.getid('/ServerCluster:%s/' % cluster)
         if len(clusterid) > 0:
            serverType = AdminConfig.showAttribute(clusterid, 'serverType')
            if serverType != 'APPLICATION_SERVER': continue
            members = AdminConfig.showAttribute(clusterid, 'members')[1:-1]
            if len(members) == 0: continue
            first = members.split()[0]
            node = AdminConfig.showAttribute(first, 'nodeName')
            server = AdminConfig.showAttribute(first, 'memberName')
            serverid = AdminConfig.getid('/Node:%s/Server:%s/' % (node, server))
            if len(serverid) == 0: continue
            return AdminConfig.list('SessionManager', serverid)         
         clusterid = AdminConfig.getid('/DynamicCluster:%s/' % cluster)
         if len(clusterid) > 0:
            serverType = AdminConfig.showAttribute(clusterid, 'serverType')
            if serverType != 'APPLICATION_SERVER': continue
            serverid = AdminConfig.getid('/ApplicationServer:%s/' % cluster)
            if len(serverid) == 0: continue
            return AdminConfig.list('SessionManager', serverid)
   return ''

def sessionString(appSession):
   ret = AdminConfig.showall(appSession)
   ret = ret.replace(lineSeparator,' ')
   if ret.find('datasourceJNDIName') == -1:
      beg = ret.find('db2RowSize')
      beg = ret.find(']', beg) + 1
      first = ret[:beg]
      second = ' [datasourceJNDIName none]'
      third = ret[beg:]
      ret = first + second + third
   if ret.find('[context') != -1:
      beg = ret.find('[context')
      first = ret[:beg]
      end = ret.find('] ', beg)
      second = ret[end + 2:]
      ret = first + second
   return ret

def manageSession(appName, forceHttpOnly, forceHttpsCookies, forceSecurityIntegration, forceSessionPath):
   contexts = retrieveContextRoots(appName, 'EDIT')
   if len(contexts) == 0: return
   applicationDeployment = AdminConfig.getid('/Deployment:%s/' % appName)
   if len(applicationDeployment) == 0: raise RuntimeError('Not found the deployment manager for the application %s' % appName)
   deployedObject = AdminConfig.showAttribute(applicationDeployment, 'deployedObject')
   if len(deployedObject) == 0: raise RuntimeError('Not found the deployed object for the application %s' % appName)
   webModuleDeploymentList = AdminConfig.list('WebModuleDeployment', deployedObject).split(lineSeparator)
   if len(webModuleDeploymentList) == 0: raise RuntimeError('Not found any webmodule deployments for the application %s' % appName)
   applicationConfig = AdminConfig.list('ApplicationConfig', deployedObject)
   if len(applicationConfig) == 0:
      data = '[ [enableSFSBFailover false] [overrideDefaultDRSSettings false] ]'
      applicationConfig = AdminConfig.create('ApplicationConfig', deployedObject, data)
      AdminConfig.create('SessionManager', applicationConfig, '[]')      
   if len(applicationConfig) > 0:
      sessionManager = AdminConfig.list('SessionManager', applicationConfig)
      if len(sessionManager) > 0: enabled = AdminConfig.showAttribute(sessionManager, 'enable')
      else: enabled = 'false'
   else: enabled = 'false'
   for context in contexts:
      webModuleDeployment = None
      for webModuleDeploymentItem in webModuleDeploymentList:
         uri = AdminConfig.showAttribute(webModuleDeploymentItem, 'uri')
         if context[1].startswith(uri):
            webModuleDeployment = webModuleDeploymentItem
            break
      if webModuleDeployment == None: continue
      targetMappings = AdminConfig.showAttribute(webModuleDeployment, 'targetMappings')[1:-1].split()
      if enabled == 'false':
         targetSession = findTargetSessionManager(appName, context[0])
         if len(targetSession) > 0:
            sessionManager = targetSession
            enabled = 'true'
      if len(sessionManager) > 0:
         AdminConfig.modify(sessionManager, '[ [enable true] [enableSecurityIntegration %s] ]' % forceSecurityIntegration)
         defaultCookieSettings = AdminConfig.showAttribute(sessionManager, 'defaultCookieSettings')
         if defaultCookieSettings == None or len(defaultCookieSettings) == 0: 
            defaultCookieSettings = AdminConfig.create('Cookie', sessionManager, '[ [name JSESSIONID] ]')
         if forceSessionPath == 'true':
            show = AdminConfig.show(defaultCookieSettings)
            if show.find('useContextRootAsPath') != -1: 
               AdminConfig.modify(defaultCookieSettings, '[ [useContextRootAsPath true] [path /] ]')
            else: 
               AdminConfig.modify(defaultCookieSettings, '[ [path %s] ]' % context[2])
         AdminConfig.modify(defaultCookieSettings, '[ [secure %s] [httpOnly %s] ]' % (forceHttpsCookies, forceHttpOnly))
         AdminConfig.unsetAttributes(defaultCookieSettings, 'domain')
      webconfig = AdminConfig.list('WebModuleConfig', webModuleDeployment)
      if len(webconfig) == 0: webconfig = AdminConfig.create('WebModuleConfig', webModuleDeployment, '[]')
      for targetMapping in targetMappings: AdminConfig.modify(targetMapping, [ ['config', '%s' % webconfig] ])
      session = AdminConfig.list('SessionManager', webModuleDeployment)
      if len(session) == 0: 
         if enabled == 'false': 
            session = AdminConfig.create('SessionManager', webconfig, '[]')
            tuningParams = AdminConfig.create('TuningParams', session, '[]')
            AdminConfig.create('InvalidationSchedule', tuningParams, '[]')
            AdminConfig.create('DRSSettings', session, '[]')
         else:
            sessionData = '[ %s ]' % sessionString(sessionManager)
            session = AdminConfig.create('SessionManager', webconfig, '[]')
            AdminConfig.modify(session, sessionData)
      AdminConfig.modify(session, '[ [enable true] [enableSecurityIntegration %s] ]' % forceSecurityIntegration)
      defaultCookieSettings = AdminConfig.showAttribute(session, 'defaultCookieSettings')
      if defaultCookieSettings == None or len(defaultCookieSettings) == 0: 
         defaultCookieSettings = AdminConfig.create('Cookie', session, '[ [name JSESSIONID] ]')
      if forceSessionPath == 'true':
         show = AdminConfig.show(defaultCookieSettings)
         if show.find('useContextRootAsPath') != -1: 
            AdminConfig.modify(defaultCookieSettings, '[ [useContextRootAsPath true] [path /] ]')
         else: 
            AdminConfig.modify(defaultCookieSettings, '[ [path %s] ]' % context[2])
      AdminConfig.modify(defaultCookieSettings, '[ [secure %s] [httpOnly %s] ]' % (forceHttpsCookies, forceHttpOnly))
      AdminConfig.unsetAttributes(defaultCookieSettings, 'domain')

def attachPolicySets(appName, wsPolicySets):
   for policy in wsPolicySets:
      apps = AdminTask.listAttachmentsForPolicySet(['-policySet', policy[1], '-attachmentType', policy[0]])
      if apps.find(appName) != -1:
         print "The Web Service Policy Set %s is already attached to the application" % policy[1]
         return
      command = ['-applicationName', appName, '-attachmentType', policy[0], '-policySet', policy[1], '-resources', [policy[3]] ]
      policySetId = AdminTask.createPolicySetAttachment(command)
      if policySetId > 0:
         if len(policy[2]) > 0:
            AdminTask.setBinding(['-bindingScope', 'domain', '-bindingName', policy[2], '-attachmentType', policy[0], '-bindingLocation', [ ['application', appName], ['attachmentId', policySetId] ] ])
         else:
            print "WARNING: No binding specified for the policy %s, it will be used the default one" % policy[1]
      else:
         print "ERROR: Failed to create the WSPolicySet %s" % (policy[0])
         print "%s done" % scriptName
         clearExit("Rollback and exit", -1)
   print "Web Service Policy Set(s) modified successfully: %d" % len(wsPolicySets)

def isEJBDeployable(appLocation):
   taskInfo = AdminApp.taskInfo(appLocation, 'EJBDeployOptions')
   if taskInfo.find('The EJB deploy option is not enabled') == -1: return 1
   else: return 0

def readProperties(props):
   global appClassloader
   global appEnvEntries
   global applicationRoles
   global contextRoots
   global createNewServicePolicy
   global drainageInterval
   global edition
   global editionDesc
   global ejbAutoLink
   global ejbBindings
   global ejbEnvEntries
   global ejbInterfaceBindings
   global ejbReferences
   global extraOptions
   global forceHttpOnly
   global forceHttpsCookies
   global forceSecurityIntegration
   global forceSessionPath
   global forceUpdateOnly
   global latestChangedFiles
   global mdbBindings
   global metadataComplete
   global propagatePlugin
   global resourceEnvReferences
   global resourceReferences
   global rolloutGroupSize
   global rolloutResetStrategy
   global rolloutStrategy
   global scaEJBBindings
   global scaModuleProperties
   global scaSCABindings
   global scaWSBindings
   global servletInitParameters
   global sharedLibraries
   global startApplication
   global startingWeight
   global syncDelay
   global targetObjects
   global timeoutRollout
   global virtualHosts
   global updateContentType
   global updateContentURI
   global updateValidationDate
   global warClassLoaderPolicy
   global webEnvEntries
   global wsPolicySets
   
   dummy = props.getProperty(propertyPrefix + ".app.classloader", "")
   if len(dummy) > 0: appClassloader = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".app.env.entries", "")
   if len(dummy) > 0: appEnvEntries = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".application.roles", "")
   if len(dummy) > 0: applicationRoles = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".context.roots", "")
   if len(dummy) > 0: contextRoots = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".create.new.service.policy", "")
   if len(dummy) > 0: createNewServicePolicy = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".drainage.interval", "")
   if len(dummy) > 0: drainageInterval = int(dummy.strip())
   dummy = props.getProperty(propertyPrefix + ".edition", "")
   if len(dummy) > 0: edition = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".edition.desc", "")
   if len(dummy) > 0: editionDesc = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".ejb.autolink", "")
   if len(dummy) > 0: ejbAutoLink = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".ejb.bindings", "")
   if len(dummy) > 0: ejbBindings = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".ejb.env.entries", "")
   if len(dummy) > 0: ejbEnvEntries = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".ejb.interface.binding", "")
   if len(dummy) > 0: ejbInterfaceBindings = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".ejb.references", "")
   if len(dummy) > 0: ejbReferences = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".extra.options", "")
   if len(dummy) > 0: extraOptions = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".force.http.only", "")
   if len(dummy) > 0: forceHttpOnly = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".force.https.cookies", "")
   if len(dummy) > 0: forceHttpsCookies = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".force.security.integration", "")
   if len(dummy) > 0: forceSecurityItegration = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".force.session.path", "")
   if len(dummy) > 0: forceSessionPath = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".force.update.only", "")
   if len(dummy) > 0: forceUpdateOnly = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".latest.changed.files", "")
   if len(dummy) > 0: latestChangedFiles = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".mdb.bindings", "")
   if len(dummy) > 0: mdbBindings = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".metadata.complete", "")
   if len(dummy) > 0: metadataComplete = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".propagate.plugin", "")
   if len(dummy) > 0: propagatePlugin = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".resource.env.references", "")
   if len(dummy) > 0: resourceEnvReferences = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".resource.references", "")
   if len(dummy) > 0: resourceReferences = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".rollout.group.size", "")
   if len(dummy) > 0: rolloutGroupSize = int(dummy.strip())
   dummy = props.getProperty(propertyPrefix + ".rollout.strategy", "")
   if len(dummy) > 0: rolloutStrategy = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".rollout.reset.strategy", "")
   if len(dummy) > 0: rolloutResetStrategy = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".sca.ejb.bindings", "")
   if len(dummy) > 0: scaEJBBindings = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".sca.module.properties", "")
   if len(dummy) > 0: scaModuleProperties = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".sca.sca.bindings", "")
   if len(dummy) > 0: scaSCABindings = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".sca.ws.bindings", "")
   if len(dummy) > 0: scaWSBindings = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".servlet.init.parameters", "")
   if len(dummy) > 0: servletInitParameters = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".shared.libraries", "")
   if len(dummy) > 0: sharedLibraries = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".start.application", "")
   if len(dummy) > 0: startApplication = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".starting.weight", "")
   if len(dummy) > 0: startingWeight = int(dummy.strip())
   dummy = props.getProperty(propertyPrefix + ".sync.delay", "")
   if len(dummy) > 0: syncDelay = int(dummy.strip())
   dummy = props.getProperty(propertyPrefix + ".target.objects", "")
   if len(dummy) > 0: targetObjects = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".timeout.rollout", "")
   if len(dummy) > 0: timeoutRollout = int(dummy.strip())
   dummy = props.getProperty(propertyPrefix + ".virtual.hosts", "")
   if len(dummy) > 0: virtualHosts = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".update.content.type", "")
   if len(dummy) > 0: updateContentType = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".update.content.uri", "")
   if len(dummy) > 0: updateContentURI = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".update.validation.date", "")
   if len(dummy) > 0: updateValidationDate = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".war.classloader.policy", "")
   if len(dummy) > 0: warClassLoaderPolicy = dummy.strip()
   dummy = props.getProperty(propertyPrefix + ".web.env.entries", "")
   if len(dummy) > 0: webEnvEntries = eval(dummy)
   dummy = props.getProperty(propertyPrefix + ".ws.policy.sets", "")
   if len(dummy) > 0: wsPolicySets = eval(dummy)

def checkAllParameters(numfile):
   global appClassloader
   global appEnvEntries
   global applicationRoles
   global contextRoots
   global createNewServicePolicy
   global drainageInterval
   global edition
   global editionDesc
   global ejbAutoLink
   global ejbBindings
   global ejbEnvEntries
   global ejbInterfaceBindings
   global ejbReferences
   global extraOptions
   global forceHttpOnly
   global forceHttpsCookies
   global forceSecurityIntegration
   global forceSessionPath
   global forceUpdateOnly
   global latestChangedFiles
   global mdbBindings
   global metadataComplete
   global propagatePlugin
   global resourceEnvReferences
   global resourceReferences
   global rolloutGroupSize
   global rolloutResetStrategy
   global rolloutStrategy
   global scaEJBBindings
   global scaModuleProperties
   global scaSCABindings
   global scaWSBindings
   global servletInitParameters
   global sharedLibraries
   global startApplication
   global startingWeight
   global syncDelay
   global targetObjects
   global timeoutRollout
   global virtualHosts
   global updateContentType
   global updateContentURI
   global updateValidationDate
   global warClassLoaderPolicy
   global webEnvEntries
   global wsPolicySets
   
   global needPropagation
   global postSaveActions
   global targetModules
   global allModules
   global virtualHostsActual
   global contextRootsActual
   global sharedLibrariesActual
   global sharedLibrariesFinal
   global resourceRefActual
   global resourceEnvRefActual
   global ejbEnvEntriesActual
   global webEnvEntriesActual
   global ejbInterfaceBindingsActual
   global ejbBindingsActual
   global mdbBindingsActual
   global ejbReferencesActual
   global appEnvEntriesActual
   global servletInitParametersActual
   global autoLinkActual
   global cellType
   global appName
   global appLocation

   
   
   if cellType == 'STANDALONE':
      standaloneServer = ''
      listServers = AdminConfig.list('Server').splitlines()
      for dummy in listServers:
         dtype = AdminConfig.showAttribute(dummy, 'serverType')
         if dtype == 'APPLICATION_SERVER':
            standaloneServer = AdminConfig.showAttribute(dummy, 'name')
            break
      if standaloneServer == '': clearExit('ERROR: Environment not correct', -1)
      standaloneNode = AdminControl.getNode()
      targetObjects = ['%s:%s' % (standaloneNode, standaloneServer)]
      webservers = AdminConfig.list('WebServer').splitlines()
      if len(webservers) > 0:
         for webserver in webservers:
            name = AdminConfig.showAttribute(webserver, 'name')
            beg = webserver.find('/nodes/') + len('/nodes/')
            end = webserver.find('/', beg)
            node = webserver[beg:end]
            targetObjects.append('%s:%s' % (node, name))

   if len(appName) == 0 and action != 'VERSION':
      clearExit("ERROR: The variable appName is mandatory", -1)

   if action in ['INSTALL', 'UPDATE', 'ROLLOUT']:
      if len(appLocation) == 0:
         clearExit("ERROR: The variable appLocation is mandatory", -1)
      if os.path.exists(appLocation) == 0:
         clearExit("ERROR: The %s file doesn't exist" % (appLocation), -1)
      
      if action == 'UPDATE':
         if updateContentType not in ['app', 'file', 'modulefile', 'partialapp']:
            clearExit("ERROR: The variable updateContentType must be ['app', 'file', 'modulefile', 'partialapp']", -1)
         if updateContentType in ['file', 'modulefile', 'partialapp']:
            if len(updateContentURI) == 0:
               clearExit("ERROR: The variable updateContentURI is mandatory and cannot be empty", -1)
      
   if action == 'EDIT': 
      temp = appName
      if len(edition) > 0: temp += '-edition' + edition
      targetModules, allModules = retrieveModules(temp, action)
      if len(targetModules) == 0:
         clearExit("ERROR: No module found in the application %s" % (appName), -1)
   elif action in ['INSTALL', 'UPDATE', 'ROLLOUT'] and updateContentType not in ['file', 'partialapp']:
      targetModules, allModules = retrieveModules(appLocation, action)
      if len(targetModules) == 0:
         clearExit("ERROR: No module found in the application %s" % (appName), -1)

   if action in ['INSTALL', 'UPDATE', 'EDIT', 'ROLLOUT', 'UNINSTALL', 'REMOVE']:
      if updateContentType not in ['file', 'partialapp']: 
         if propagatePlugin not in ['true', 'false']:
            clearExit("ERROR: The variable propagatePlugin must be boolean", -1)

   if action in ['INSTALL', 'EDIT', 'ROLLOUT'] or (action in ['UPDATE'] and updateContentType not in ['file', 'partialapp'] and numfile > 0):
         if isinstance(targetObjects, type([])) == 0:
            clearExit("ERROR: The variable targetObjects must be a list", -1)
         for dummy in targetObjects:
            if isinstance(dummy, type('')) == 1:
               ttype, target = findTarget(dummy)
               if ttype == 'E': clearExit("ERROR: %s" % target, -1)
               else: addTarget(targetModules, ttype, target, allModules)
            elif isinstance(dummy, type([])) == 1 and len(dummy) == 2:
               dummy0 = dummy[0]
               dummy1 = dummy[1]
               if isinstance(dummy0, type([])) == 1 and isinstance(dummy1, type([])) == 1:
                  for module in dummy0:
                     if findModule(module, targetModules) == 0:
                        if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                           clearExit("ERROR: The module %s doesn't exist in the file %s\nThe available modules are: %s" % (module, appLocation, allModules), -1)
                        else:
                           clearExit("ERROR: The module %s doesn't exist in the application %s\nThe available modules are: %s" % (module, appName, allModules), -1)
                  for dtarget in dummy1:
                     ttype, target = findTarget(dtarget)
                     if ttype == 'E': clearExit("ERROR: %s" % target, -1)
                     addTarget(targetModules, ttype, target, dummy0)
               else:
                  clearExit("ERROR: Each object of the variable targetObjects must be a not empty string or a list of two lists", -1)
            else:
               clearExit("ERROR: Each object of the variable targetObjects must be a not empty string or a list of two lists", -1)
         if len(targetObjects) == 0:
            clearExit("The variable targetObjects must be a not empty list", -1)
         for module in targetModules:
            if len(module[2]) == 0:
               clearExit("ERROR: The module %s has not target objects associated" % module[0], -1)
            if hasServers(module[2]) == 0:
               clearExit("ERROR: The module %s has no application servers or clusters associated" % module[0], -1)
            if hasWebServers(module[2]) == 1:
               if propagatePlugin == 'true': needPropagation = 'true'
         
         if isinstance(virtualHosts, type([])) == 0:
            clearExit("ERROR: The variable virtualHosts must be a list", -1)
         for dummy in virtualHosts:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 2:
               clearExit("ERROR: Each object of the variable virtualHosts must be list of two strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each item of an object of the variable virtualHosts must be a not empty string", -1)
         numVHs = len(virtualHosts)
         if numVHs > 0:
            all = 0
            for vHost in virtualHosts:
               if vHost[0] == '.*': all = 1
            if all == 1 and numVHs > 1:
               clearExit("ERROR: It is not possible to supply more than one row in input when at least one is using the .* value as <Web Module Name> item for the variable virtualHosts", -1)
            if action == 'EDIT': 
               temp = appName
               if len(edition) > 0: temp += '-edition' + edition
               virtualHostsActual = retrieveVirtualHosts(temp, action)
            else:
               virtualHostsActual = retrieveVirtualHosts(appLocation, action)
            numVHsA = len(virtualHostsActual)
            if numVHs > numVHsA:
               if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                  clearExit("ERROR: It is not possible to supply more rows for the variable virtualHosts than the number of web modules in the file %s" % appLocation, -1)
               else:
                  clearExit("ERROR: It is not possible to supply more rows for the variable virtualHosts than the number of web modules in the application %s" % appName, -1)
            if all == 1:
               for vHostA in virtualHostsActual:
                  vHostA[2] = virtualHosts[0][1]
            else:
               for vHost in virtualHosts:
                  found = 0
                  id = AdminConfig.getid('/VirtualHost:' + vHost[1] + '/')
                  if len(id) == 0:
                     clearExit("ERROR: The virtual host %s doesn't exist" % (vHost[1]), -1)
                  for vHostA in virtualHostsActual:
                     if vHost[0] == vHostA[0]:
                        vHostA[2] = vHost[1]
                        found = 1
                        break
                  if found == 0:
                     if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                        clearExit("ERROR: The Web Module %s is not present in the file %s\nThe available modules are: %s" % (vHost[0], appLocation, getSingleList(virtualHostsActual, 0)), -1)
                     else:
                        clearExit("ERROR: The Web Module %s is not present in the application %s\nThe available modules are: %s" % (vHost[0], appName, getSingleList(virtualHostsActual, 0)), -1)
         
         if isinstance(contextRoots, type([])) == 0:
            clearExit("ERROR: The variable contextRoots must be a list", -1)
         for dummy in contextRoots:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 2:
               clearExit("ERROR: Each object of the variable contextRoots must be list of two strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each item of an object of the variable contextRoots must be a not empty string", -1)
         numCRs = len(contextRoots)
         if numCRs > 0:
            all = 0
            for context in contextRoots:
               if context[0] == '.*': all = 1
            if all == 1 and numCRs > 1:
               clearExit("ERROR: It is not possible to supply more than one row using the .* value as <Web Module Name> item for the variable contextRoots", -1)
            if action == 'EDIT': 
               temp = appName
               if len(edition) > 0: temp += '-edition' + edition
               contextRootsActual = retrieveContextRoots(temp, action)
            else:
               contextRootsActual = retrieveContextRoots(appLocation, action)
            numCRsA = len(contextRootsActual)
            if numCRs > numCRsA:
               if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                  clearExit("ERROR: It is not possible to supply more rows for the variable contextRoots than the number of web modules in the file %s" % appLocation, -1)
               else:
                  clearExit("ERROR: It is not possible to supply more rows for the variable contextRoots than the number of web modules in the application %s" % appName, -1)
            if all == 1 and numCRsA > 1:
               if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                  clearExit("ERROR: It is not possible to supply the .* value as <Web Module Name> item for the variable contextRoots when the file %s has more than one web module" % appLocation, -1)
               else:
                  clearExit("ERROR: It is not possible to supply the .* value as <Web Module Name> item for the variable contextRoots when the application %s has more than one web module" % appName, -1)
            for context in contextRoots:
               found = 0
               for contextA in contextRootsActual:
                  if context[0] == contextA[0] or context[0] == '.*':
                     contextA[2] = context[1]
                     found = 1
                     break
               if found == 0:
                  if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                     clearExit("ERROR: The Web Module %s is not present in the file %s\nThe available modules are: %s" % (context[0], appLocation, getSingleList(contextRootsActual, 0)), -1)
                  else:
                     clearExit("ERROR: The Web Module %s is not present in the application %s\nThe available modules are: %s" % (context[0], appName, getSingleList(contextRootsActual, 0)), -1)
         
         if isinstance(sharedLibraries, type([])) == 0:
            clearExit("ERROR: The variable sharedLibraries must be a list", -1)
         for dummy in sharedLibraries:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 2:
               clearExit("ERROR: Each object of the variable sharedLibraries must be list of two strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each item of an object of the variable sharedLibraries must be a not empty string", -1)
         numSVs = len(sharedLibraries)
         if numSVs > 0:
            if action == 'EDIT': 
               temp = appName
               if len(edition) > 0: temp += '-edition' + edition
               sharedLibrariesActual = retrieveSharedLibraries(appName, action)
            else:
               sharedLibrariesActual = retrieveSharedLibraries(appLocation, action)
            numSVsA = len(sharedLibrariesActual)
            if numSVs > numSVsA:
               if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                  clearExit("ERROR: It is not possible to supply more rows for the variable sharedLibraries than the number of modules in the file %s" % appLocation, -1)
               else:
                  clearExit("ERROR: It is not possible to supply more rows for the variable sharedLibraries than the number of modules in the application %s" % appName, -1)
            sharedLibrariesFinal = []
            for context in sharedLibraries:
               found = 0
               for contextA in sharedLibrariesActual:
                  if context[0] == contextA[0]:
                     found = 1
                     sharedLibrariesFinal.append([context[0], contextA[1], context[1]])
                     break
                  elif context[0] == '.*':
                     sharedLibrariesFinal.append([context[0], '.*', context[1]])
                     found = 1
                     break
                  elif context[0] == appName or context[0] == '#APPNAME#':
                     sharedLibrariesFinal.append([appName, 'META-INF/application.xml', context[1]])
                     found = 1
                     break
               if found == 0:
                  if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                     clearExit("ERROR: The Module %s is not present in the file %s.\nThe available modules are: %s" % (context[0], appLocation, allModules), -1)
                  else:
                     clearExit("ERROR: The Module %s is not present in the application %s.\nThe available modules are: %s" % (context[0], appName, allModules), -1)
         
         if metadataComplete not in ['true', 'false']:
            clearExit("ERROR: The variable metadataComplete must be boolean", -1)
            
         if isinstance(resourceReferences, type([])) == 0:
            clearExit("ERROR: The variable resourceReferences must be a list", -1)
         for dummy in resourceReferences:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 2:
               clearExit("ERROR: The variable resourceReferences must be in the form [<reference jndi>|[<session bean>|<war name>, <reference jndi>], <target jndi>]", -1)
            if isinstance(dummy[0], type([])) == 1:
               if len(dummy[0]) != 2:
                  clearExit("ERROR: The first item of the variable resourceReferences must be a string or a list of two not empty strings", -1)
               for dummy2 in dummy[0]:
                  if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                     clearExit("ERROR: The first item of the variable resourceReferences must be a string or a list of two not empty strings", -1)
            elif isinstance(dummy[0], type('')) == 1:
               if len(dummy[0]) == 0:
                  clearExit("ERROR: The first item of the variable resourceReferences must be a string or a list of two not empty strings", -1)
            else: clearExit("ERROR: The first item of the variable resourceReferences must be a string or a list of two not empty strings", -1)
            if isinstance(dummy[1], type('')) == 0 or len(dummy[1]) == 0:
                  clearExit("ERROR: The item target jndi of the variable resourceReferences must be a not empty string", -1)
         if metadataComplete == 'true' or action == 'EDIT':
            if len(resourceReferences) > 0:
               if action == 'EDIT': 
                  temp = appName
                  if len(edition) > 0: temp += '-edition' + edition
                  resourceRefActual = retrieveReferences(appName, action, 'false')
               else:
                  resourceRefActual = retrieveReferences(appLocation, action, 'false')
               for ref in resourceReferences:
                  found = 0
                  for refActual in resourceRefActual:
                     if isinstance(ref[0], type('')) == 1:
                        if ref[0] == refActual[3]:
                           refActual[5] = ref[1]
                           found = 1
                     elif isinstance(ref[0], type([])) == 1:
                        if ref[0][1] == refActual[3]:
                           if (len(refActual[1]) == 0 and refActual[0] == ref[0][0]) or (len(refActual[1]) > 0 and refActual[1] == ref[0][0]):
                              refActual[5] = ref[1]
                              found = 1
                              break
                  if found == 0:
                     if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                        clearExit("ERROR: The Resource Reference %s is not present in the file %s.\nThe available resource references are: %s" % (ref[0], appLocation, getSingleList(resourceRefActual, 3)), -1)
                     else:
                        clearExit("ERROR: The Resource Reference %s is not present in the application %s.\nThe available resource references are: %s" % (ref[0], appName, getSingleList(resourceRefActual, 3)), -1)
         
         if isinstance(resourceEnvReferences, type([])) == 0:
            clearExit("ERROR: The variable resourceEnvReferences must be a list", -1)
         for dummy in resourceEnvReferences:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 2:
               clearExit("ERROR: Each object of the variable resourceEnvReferences must be in the form [<reference jndi>|[<session bean>|<war name>, <reference jndi>], <target jndi>]", -1)
            if isinstance(dummy[0], type([])) == 1:
               if len(dummy[0]) != 2:
                  clearExit("ERROR: The first item of the variable resourceEnvReferences must be a string or a list of two not empty strings", -1)
               for dummy2 in dummy[0]:
                  if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                     clearExit("ERROR: The first item of the variable resourceEnvReferences must be a string or a list of two not empty strings", -1)
            elif isinstance(dummy[0], type('')) == 1:
               if len(dummy[0]) == 0:
                  clearExit("ERROR: The first item of the variable resourceEnvReferences must be a string or a list of two not empty strings", -1)
            else: clearExit("ERROR: The first item of the variable resourceEnvReferences must be a string or a list of two not empty strings", -1)
            if isinstance(dummy[1], type('')) == 0 or len(dummy[1]) == 0:
                  clearExit("ERROR: The item target jndi of the variable resourceEnvReferences must be a not empty string", -1)
         if len(resourceEnvReferences) > 0:
            if action == 'EDIT': 
               temp = appName
               if len(edition) > 0: temp += '-edition' + edition
               resourceEnvRefActual = retrieveReferences(appName, action, 'true')
            else:
               resourceEnvRefActual = retrieveReferences(appLocation, action, 'true')
            for ref in resourceEnvReferences:
               found = 0
               for refActual in resourceEnvRefActual:
                  if isinstance(ref[0], type('')) == 1:
                     if ref[0] == refActual[3]:
                        refActual[5] = ref[1]
                        found = 1
                  elif isinstance(ref[0], type([])) == 1:
                     if ref[0][1] == refActual[3]:
                        if (len(refActual[1]) == 0 and refActual[0] == ref[0][0]) or (len(refActual[1]) > 0 and refActual[1] == ref[0][0]):
                           refActual[5] = ref[1]
                           found = 1
                           break
               if found == 0:
                  if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                     clearExit("ERROR: The Resource Environment Reference %s is not present in the file %s.\nThe available resource env references are: %s" % (ref[0], appLocation, getSingleList(resourceEnvRefActual, 3)), -1)
                  else:
                     clearExit("ERROR: The Resource Environment Reference %s is not present in the application %s.\nThe available resource env references are: %s" % (ref[0], appName, getSingleList(resourceEnvRefActual, 3)), -1)
         
         if isinstance(applicationRoles, type([])) == 0:
            clearExit("ERROR: The variable applicationRoles must be a list", -1)
         for dummy in applicationRoles:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 5:
               clearExit("ERROR: Each object of the variable applicationRoles must be a list of five strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0:
                  clearExit("ERROR: Each item of an object of the variable applicationRoles must be a string", -1)
            if len(dummy[0]) == 0:
               clearExit("ERROR: The item <Role> in %s cannot be an empty string" % dummy, -1)
            if dummy[1] not in ['Yes', 'No']:
               clearExit("ERROR: The item <Everyone> in %s must be 'Yes' or 'No'" % dummy, -1)
            if dummy[2] not in ['Yes', 'No']:
               clearExit("ERROR: The item <All Authenticated> in %s must be 'Yes' or 'No'" % dummy, -1)
         if metadataComplete == 'true' or action == 'EDIT':
            if len(applicationRoles) > 0:
               if action == 'EDIT':
                  temp = appName
                  if len(edition) > 0: temp += '-edition' + edition
                  roles = retrieveRoles(appName, action)
               else:
                  roles = retrieveRoles(appLocation, action)
            for role in applicationRoles:
               if role[0] not in roles:
                  if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                     clearExit("ERROR: The role %s is not present in the file %s\nThe available roles are: %s" % (role[0], appLocation, roles), -1)
                  else:
                     clearExit("ERROR: The role %s is not present in the application %s\nThe available roles are: %s" % (role[0], appName, roles), -1)
         
         if isinstance(wsPolicySets, type([])) == 0:
            clearExit("ERROR: The variable wsPolicySets must be a list", -1)
         for dummy in wsPolicySets:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 4:
               clearExit("ERROR: Each object of the variable wsPolicySets must be a list of four strings", -1)
            if isinstance(dummy[0], type('')) == 0 or dummy[0] not in ['client', 'provider']:
               clearExit("ERROR: The item AttachmentType in %s must be either 'client' or 'provider'" % dummy, -1)
            if isinstance(dummy[1], type('')) == 0 or len(dummy[1]) == 0:
               clearExit("ERROR: The item Policy Set Name in %s must be a not empty string" % dummy, -1)
            if isinstance(dummy[2], type('')) == 0:
               clearExit("ERROR: The item Binding Name in %s must be a string" % dummy, -1)
            if isinstance(dummy[3], type('')) == 0 or len(dummy[3]) == 0:
               clearExit("ERROR: The item Resources in %s must be a not empty string" % dummy, -1)
         
         if isinstance(scaWSBindings, type([])) == 0:
            clearExit("ERROR: The variable scaWSBindings must be a list", -1)
         for dummy in scaWSBindings:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 3:
               clearExit("ERROR: Each object of the variable scaWSBindings must be a list of three strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each item of an object of the variable scaWSBindings must be a not empty string", -1)
         
         if isinstance(scaSCABindings, type([])) == 0:
            clearExit("ERROR: The variable scaSCABindings must be a list", -1)
         for dummy in scaSCABindings:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 5:
               clearExit("ERROR: Each object of the variable scaSCABindings must be a list of five strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0:
                  clearExit("ERROR: Each item of an object of the variable scaSCABindings must be a string", -1)
            if len(dummy[0]) == 0 or len(dummy[1]) == 0 or len(dummy[2]) == 0 or len(dummy[3]) == 0:
               clearExit("ERROR: Each item except <Target Application Name> of an object of the variable scaSCABindings must be a not empty string", -1)
         
         if isinstance(scaEJBBindings, type([])) == 0:
            clearExit("ERROR: The variable scaEJBBindings must be a list", -1)
         for dummy in scaEJBBindings:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 3:
               clearExit("ERROR: Each object of the variable scaEJBBindings must be a list of three strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each item of an object of the variable scaEJBBindings must be a not empty string", -1)
         
         if isinstance(scaModuleProperties, type([])) == 0:
            clearExit("ERROR: The variable scaModuleProperties must be a list", -1)
         for dummy in scaModuleProperties:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 4:
               clearExit("ERROR: Each object of the variable scaModuleProperties must be a list of three strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0:
                  clearExit("ERROR: Each item of an object of the variable scaModuleProperties must be a string", -1)
            if len(dummy[0]) == 0:
               clearExit("ERROR: The item <module name> in %s cannot be an empty string" % dummy, -1)
            if len(dummy[1]) == 0:
               clearExit("ERROR: The item <property name> in %s cannot be an empty string" % dummy, -1)
            if len(dummy[3]) == 0:
               clearExit("ERROR: The item <value> in %s cannot be an empty string" % dummy, -1)
         
         if isinstance(extraOptions, type([])) == 0:
            clearExit("ERROR: The variable extraOptions must be a list", -1)
            
         if appClassloader not in ['PARENT_FIRST', 'PARENT_LAST']:
            clearExit("ERROR: The variable appClassloader must be either 'PARENT_FIRST' or 'PARENT_LAST'", -1)
         
         if isinstance(startingWeight, type(1)) == 0:
            clearExit("ERROR: The variable startingWeight must be an integer", -1)
         if startingWeight < 1:
            clearExit("ERROR: The variable startingWeight must be a positive number", -1)
         
         if warClassLoaderPolicy not in ['SINGLE', 'MULTIPLE']:
            clearExit("ERROR: The variable warClassLoaderPolicy only valid values are 'SINGLE', 'MULTIPLE'", -1)
         
         if isinstance(ejbEnvEntries, type([])) == 0:
            clearExit("ERROR: The variable ejbEnvEntries must be a list", -1)
         for dummy in ejbEnvEntries:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 4:
               clearExit("ERROR: Each object of the variable ejbEnvEntries must be a list of four strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each object of the variable ejbEnvEntries must be a not empty string", -1)
         if metadataComplete == 'true' or action == 'EDIT':
            if len(ejbEnvEntries) > 0:
               if action == 'EDIT': 
                  temp = appName
                  if len(edition) > 0: temp += '-edition' + edition
                  ejbEnvEntriesActual = retrieveEJBEnvEntries(appName, action)
               else:
                  ejbEnvEntriesActual = retrieveEJBEnvEntries(appLocation, action)
               for entry in ejbEnvEntries:
                  found = 0
                  for entryActual in ejbEnvEntriesActual:
                     if entry[0] == entryActual[0] and \
                        entry[1] == entryActual[2] and \
                        entry[2] == entryActual[3]:
                        entryActual[6] = entry[3]
                        found = 1
                        break
                  if found == 0:
                     if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                        clearExit("ERROR: The EJB Environment Entry %s/%s/%s is not present in the file %s.\nThe available EJB env entries are: %s" % \
                                 (entry[0], entry[1], entry[2], appLocation, getTuple(ejbEnvEntriesActual, [0, 2, 3])), -1)
                     else:
                        clearExit("ERROR: The EJB Environment Entry %s/%s/%s is not present in the application %s.\nThe available EJB env entries are: %s" % \
                                 (entry[0], entry[1], entry[2], appName, getTuple(ejbEnvEntriesActual, [0, 2, 3])), -1)
         
         if isinstance(webEnvEntries, type([])) == 0:
            clearExit("ERROR: The variable webEnvEntries must be a list", -1)
         for dummy in webEnvEntries:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 3:
               clearExit("ERROR: Each object of the variable webEnvEntries must be a list of three strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each object of the variable webEnvEntries must be a not empty string", -1)
         if metadataComplete == 'true' or action == 'EDIT':
            if len(webEnvEntries) > 0:
               if action == 'EDIT': 
                  temp = appName
                  if len(edition) > 0: temp += '-edition' + edition
                  webEnvEntriesActual = retrieveWebEnvEntries(appName, action)
               else:
                  webEnvEntriesActual = retrieveWebEnvEntries(appLocation, action)
               for entry in webEnvEntries:
                  found = 0
                  for entryActual in webEnvEntriesActual:
                     if entry[0] == entryActual[0] and \
                        entry[1] == entryActual[2]:
                        entryActual[5] = entry[2]
                        found = 1
                        break
                  if found == 0:
                     if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                        clearExit("ERROR: The WEB Environment Entry %s/%s is not present in the file %s.\nThe available WEB env entries are: %s" % (entry[0], entry[1], appLocation, getTuple(webEnvEntriesActual, [0, 2])), -1)
                     else:
                        clearExit("ERROR: The WEB Environment Entry %s/%s is not present in the application %s.\nThe available WEB env entries are: %s" % \
                                  (entry[0], entry[1], appName, getTuple(webEnvEntriesActual, [0, 2])), -1)
          
         if isinstance(servletInitParameters, type([])) == 0:
            clearExit("ERROR: The variable servletInitParameters must be a list", -1)
         for dummy in servletInitParameters:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 4:
               clearExit("ERROR: Each object of the variable servletInitParameters must be a list of four strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each object of the variable servletInitParameters must be a not empty string", -1)
         if metadataComplete == 'true' or action == 'EDIT':
            if len(servletInitParameters) > 0:
               if action == 'EDIT': 
                  temp = appName
                  if len(edition) > 0: temp += '-edition' + edition
                  servletInitParametersActual = retrieveServletInitParameters(appName, action)
               else:
                  servletInitParametersActual = retrieveServletInitParameters(appLocation, action)
               for entry in servletInitParameters:
                  found = 0
                  for entryActual in servletInitParametersActual:
                     if entry[0] == entryActual[0] and \
                        entry[1] == entryActual[2] and \
                        entry[2] == entryActual[3]:
                        entryActual[5] = entry[3]
                        found = 1
                        break
                  if found == 0:
                     if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                        clearExit("ERROR: The Servlet Init Parameter %s/%s/%s is not present in the file %s.\nThe available Servlet Init Parameters are: %s" % (entry[0], entry[1], entry[2], appLocation, getTuple(servletInitParametersActual, [0, 2, 3])), -1)
                     else:
                        clearExit("ERROR: The Servlet Init Parameter %s/%s/%s is not present in the application %s.\nThe available Servlet Init Parameters are: %s" % \
                                  (entry[0], entry[1], entry[2], appName, getTuple(servletInitParametersActual, [0, 2, 3])), -1)
         
         if isinstance(ejbInterfaceBindings, type([])) == 0:
            clearExit("ERROR: The variable ejbInterfaceBindings must be a list", -1)
         for dummy in ejbInterfaceBindings:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 4:
               clearExit("ERROR: Each object of the variable ejbInterfaceBindings must be a list of four strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each object of the variable ejbInterfaceBindings must be a not empty string", -1)
         if metadataComplete == 'true' or action == 'EDIT':
            if len(ejbInterfaceBindings) > 0:
               if action == 'EDIT': 
                  temp = appName
                  if len(edition) > 0: temp += '-edition' + edition
                  ejbInterfaceBindingsActual = retrieveEJBInterfaces(appName, action)
               else:
                  ejbInterfaceBindingsActual = retrieveEJBInterfaces(appLocation, action)
               for entry in ejbInterfaceBindings:
                  found = 0
                  for entryActual in ejbInterfaceBindingsActual:
                     if entry[0] == entryActual[0] and \
                        entry[1] == entryActual[1] and \
                        entry[2] == entryActual[3]:
                        entryActual[4] = entry[3]
                        found = 1
                        break
                  if found == 0:
                     if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                        clearExit("ERROR: The EJB Interface Binding %s/%s/%s is not present in the file %s.\nThe available EJB interfaces are: %s" % \
                                 (entry[0], entry[1], entry[2], appLocation, getTuple(ejbInterfaceBindingsActual, [0, 1, 3])), -1)
                     else:
                        clearExit("ERROR: The EJB Interface Binding %s/%s/%s is not present in the application %s.\nThe available EJB interfaces are: %s" % \
                                 (entry[0], entry[1], entry[2], appName, getTuple(ejbInterfaceBindingsActual, [0, 1, 3])), -1)
         
         if isinstance(ejbBindings, type([])) == 0:
            clearExit("ERROR: The variable ejbBindings must be a list", -1)
         for dummy in ejbBindings:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 5:
               clearExit("ERROR: Each object of the variable ejbBindings must be a list of three strings", -1)
            if isinstance(dummy[0], type('')) == 0 or len(dummy[0]) == 0:
               clearExit("ERROR: The item Module of the variable ejbBindings must be a not empty string", -1)
            if isinstance(dummy[1], type('')) == 0 or len(dummy[0]) == 0:
               clearExit("ERROR: The item EJB Name of the variable ejbBindings must be a not empty string", -1)
            if isinstance(dummy[2], type('')) == 0 :
               clearExit("ERROR: The item Target JNDI Name of the variable ejbBindings must be a string", -1)
            if isinstance(dummy[3], type('')) == 0:
               clearExit("ERROR: The item Local Home JNDI of the variable ejbBindings must be a string", -1)
            if isinstance(dummy[3], type('')) == 0:
               clearExit("ERROR: The item Remote Home JNDI of the variable ejbBindings must be a string", -1)
         if metadataComplete == 'true' or action == 'EDIT':
            if len(ejbBindings) > 0:
               if action == 'EDIT': 
                  temp = appName
                  if len(edition) > 0: temp += '-edition' + edition
                  ejbBindingsActual = retrieveEJBs(appName, action)
               else:
                  ejbBindingsActual = retrieveEJBs(appLocation, action)
               for entry in ejbBindings:
                  found = 0
                  for entryActual in ejbBindingsActual:
                     if entry[0] == entryActual[0] and \
                        entry[1] == entryActual[1]:
                        entryActual[3] = entry[2]
                        entryActual[4] = entry[3]
                        entryActual[5] = entry[4]
                        found = 1
                        break
                  if found == 0:
                     if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                        clearExit("ERROR: The EJB Binding %s/%s is not present in the file %s.\nThe available EJB bindings are: %s" % \
                                 (entry[0], entry[1], appLocation, getTuple(ejbBindingsActual, [0, 1])), -1)
                     else:
                        clearExit("ERROR: The EJB Binding %s/%s is not present in the application %s.\nThe available EJB bindings are: %s" % \
                                 (entry[0], entry[1], appName, getTuple(ejbBindingsActual, [0, 1])), -1)
         
         if isinstance(mdbBindings, type([])) == 0:
            clearExit("ERROR: The variable mdbBindings must be a list", -1)
         for dummy in mdbBindings:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 3:
               clearExit("ERROR: Each object of the variable mdbBindings must be a list of three strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each object of the variable mdbBindings must be a not empty string", -1)
         if len(mdbBindings) > 0:
            if action == 'EDIT': 
               temp = appName
               if len(edition) > 0: temp += '-edition' + edition
               mdbBindingsActual = retrieveMDBs(appName, action)
            else:
               mdbBindingsActual = retrieveMDBs(appLocation, action)
            for entry in mdbBindings:
               found = 0
               for entryActual in mdbBindingsActual:
                  if entry[0] == entryActual[0] and \
                     entry[1] == entryActual[1]:
                     entryActual[3] = ''
                     entryActual[4] = entry[2]
                     entryActual[5] = ''
                     entryActual[6] = ''
                     found = 1
                     break
               if found == 0:
                  if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                     clearExit("ERROR: The MDB %s/%s is not present in the file %s.\nThe available MDBs are: %s" % \
                              (entry[0], entry[1], appLocation, getTuple(mdbBindingsActual, [0, 1])), -1)
                  else:
                     clearExit("ERROR: The MDB %s/%s is not present in the application %s.\nThe available MDBs are: %s" % \
                              (entry[0], entry[1], appName, getTuple(mdbBindingsActual, [0, 1])), -1)
         
         if isinstance(ejbReferences, type([])) == 0:
            clearExit("ERROR: The variable ejbReferences must be a list", -1)
         for dummy in ejbReferences:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 2:
               clearExit("ERROR: Each object of the variable ejbReferences must be a list of two strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each object of the variable ejbReferences must be a not empty string", -1)
         if metadataComplete == 'true' or action == 'EDIT':
            if len(ejbReferences) > 0:
               if action == 'EDIT': 
                  temp = appName
                  if len(edition) > 0: temp += '-edition' + edition
                  ejbReferencesActual = retrieveEJBReferences(appName, action)
               else:
                  ejbReferencesActual = retrieveEJBReferences(appLocation, action)
               for entry in ejbReferences:
                  found = 0
                  for entryActual in ejbReferencesActual:
                     if entry[0] == entryActual[3]:
                        entryActual[5] = entry[1]
                        found = 1
                        break
                  if found == 0:
                     if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                        clearExit("ERROR: The EJB Reference %s is not present in the file %s.\nThe available EJB references are: %s" % \
                                 (entry[0], appLocation, getSingleList(ejbReferencesActual, 3)), -1)
                     else:
                        clearExit("ERROR: The EJB Reference %s is not present in the application %s.\nThe available EJB references are: %s" % \
                                 (entry[0], appName, getSingleList(ejbReferencesActual, 3)), -1)
         
         if isinstance(appEnvEntries, type([])) == 0:
            clearExit("ERROR: The variable appEnvEntries must be a list", -1)
         for dummy in appEnvEntries:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 2:
               clearExit("ERROR: Each object of the variable appEnvEntries must be a list of two strings", -1)
            for dummy2 in dummy:
               if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
                  clearExit("ERROR: Each object of the variable appEnvEntries must be a not empty string", -1)
         if metadataComplete == 'true' or action == 'EDIT':
            if len(appEnvEntries) > 0:
               if action == 'EDIT': 
                  temp = appName
                  if len(edition) > 0: temp += '-edition' + edition
                  appEnvEntriesActual = retrieveAppEnvEntries(appName, action)
               else:
                  appEnvEntriesActual = retrieveAppEnvEntries(appLocation, action)
               for entry in appEnvEntries:
                  found = 0
                  for entryActual in appEnvEntriesActual:
                     if entry[0] == entryActual[0]:
                        entryActual[3] = entry[1]
                        found = 1
                        break
                  if found == 0:
                     if action in ['INSTALL', 'ROLLOUT'] or (action == 'UPDATE' and updateContentType in ['app', 'modulefile']):
                        clearExit("ERROR: The APP Env Entry %s is not present in the file %s.\nThe available APP env entries are: %s" % \
                                 (entry[0], appLocation, getSingleList(appEnvEntriesActual, 0)), -1)
                     else:
                        clearExit("ERROR: The APP Env Entry %s is not present in the application %s.\nThe available APP env entries are: %s" % \
                                 (entry[0], appName, getSingleList(appEnvEntriesActual, 0)), -1)
         
         if ejbAutoLink not in ['true', 'false']:
            clearExit("ERROR: The variable ejbAutoLink must be boolean", -1)
         if ejbAutoLink == 'true': autoLinkActual = '-useAutoLink'
         if ejbAutoLink == 'false': autoLinkActual = '-nouseAutoLink'
   
   if action in ['INSTALL', 'UPDATE', 'EDIT', 'REMOVE', 'UNINSTALL']:
      if cellType == 'DISTRIBUTED':
         if isinstance(syncDelay, type(1)) == 0:
            clearExit("ERROR: The variable syncDelay must be an integer", -1)
         if syncDelay < -1 or syncDelay > 20:
            clearExit("ERROR: The variable syncDelay must be in the range [-1, 20]", -1)

   if action in ['INSTALL', 'UPDATE', 'EDIT', 'ROLLOUT']:
      if updateContentType not in ['file', 'partialapp']: 
         if updateValidationDate not in ['true', 'false']:
            clearExit("ERROR: The variable updateValidationDate must be boolean", -1)

   if action == 'ROLLOUT':
      if cellType == 'STANDALONE':
         clearExit("ERROR: The action ROLLOUT is not possible in a STANDALONE environment", -1)
      if isinstance(timeoutRollout, type(100)) == 0:
         clearExit("ERROR: The variable timoeoutRollout must be an integer", -1)
      if timeoutRollout < 10: timeoutRollout = 10
      elif timeoutRollout > 300: timeoutRollout = 300

   if action == 'INSTALL':
      if startApplication not in ['true', 'false']:
         clearExit("ERROR: The variable startApplication must be boolean", -1)

   if action in ['EDITION']:
      if cellType == 'STANDALONE':
         clearExit("ERROR: The action %s is not possible in a STANDALONE environment" % action, -1)

   if action in ['ACTIVATE', 'DEACTIVATE', 'ROLLOUTEDITION']:
      if cellType == 'STANDALONE':
         clearExit("ERROR: The action %s is not possible in a STANDALONE environment" % action, -1)
      if len(edition) == 0:
         clearExit("ERROR: The variable edition cannot be empty", -1)

   if action in ['INSTALL', 'UPDATE', 'UNINSTALL', 'EDIT', 'ROLLOUT']:
      if len(edition) > 0 and cellType == 'STANDALONE':
         clearExit("ERROR: The Application Edition Management (the variable edition is not empty) is not possible in a STANDALONE environment" % action, -1)
      
   if action == 'ROLLOUTEDITION':   
      if rolloutStrategy not in ['grouped', 'atomic']:
         clearExit("ERROR: The variable rolloutStrategy must be only 'grouped' or 'atomic'", -1)
      if rolloutResetStrategy not in ['soft', 'hard']:
         clearExit("ERROR: The variable rolloutResetStrategy must be only 'soft' or 'hard'", -1)
      if rolloutStrategy == 'grouped':
         if rolloutGroupSize < 1:
            clearExit("ERROR: The variable rolloutGroupSize must be >= 1", -1)
      if isinstance(drainageInterval, type(100)) == 0:
         clearExit("ERROR: The variable drainageInterval must be an integer", -1)
      if drainageInterval < 1: drainageInterval = 1
      elif drainageInterval > 300: drainageInterval = 300

   if action == 'REMOVE':
      if updateContentType not in ['file', 'modulefile']:
         clearExit("ERROR: The variable updateContentType must be ['file', 'modulefile']", -1)
      if len(updateContentURI) == 0:
         clearExit("ERROR: The variable updateContentURI is mandatory and cannot be empty", -1)

   if action == 'INSTALL':
      if createNewServicePolicy not in ['true', 'false']:
         clearExit("ERROR: The variable createNewServicePolicy must be boolean", -1)

   if action == 'UPDATE' and updateContentType not in ['app']:
      if forceUpdateOnly not in ['true', 'false']:
         clearExit("ERROR: The variable forceUpdateOnly must be boolean", -1)

   if action in ['INSTALL', 'UPDATE', 'EDIT', 'ROLLOUT']:
      if isinstance(latestChangedFiles, type([])) == 0:
         clearExit("ERROR: The variable latestChangedFiles must be a list", -1)
      for dummy in latestChangedFiles:
         if isinstance(dummy, type([])) == 0 or len(dummy) != 2:
            clearExit("ERROR: Each object of the variable latestChangedFiles must be a list of two strings", -1)
         for dummy2 in dummy:
            if isinstance(dummy2, type('')) == 0 or len(dummy2) == 0:
               clearExit("ERROR: Each object of the variable latestChangedFiles must be a not empty string", -1)
         if os.path.exists(dummy[1]) == 0:
            clearExit("ERROR: The %s file doesn't exist (variable latestChangedFiles)" % (dummy[1]), -1)
      if forceHttpOnly not in ['true', 'false']:
         clearExit("ERROR: The variable forceHttpOnly must be boolean", -1)
      if forceHttpsCookies not in ['true', 'false']:
         clearExit("ERROR: The variable forceHttpsCookies must be boolean", -1)
      if forceSecurityIntegration not in ['true', 'false']:
         clearExit("ERROR: The variable forceSecurityIntegration must be boolean", -1)
      if forceSessionPath not in ['true', 'false']:
         clearExit("ERROR: The variable forceSessionPath must be boolean", -1)

def completeOptions(options, metadataComplete):
   global targetModules
   global virtualHosts
   global virtualHostsActual
   global applicationRoles
   global contextRoots
   global contextRootsActual
   global sharedLibraries
   global sharedLibrariesFinal
   global resourceReferences
   global resourceRefActual
   global resourceEnvReferences
   global resourceEnvRefActual
   global ejbEnvEntries
   global ejbEnvEntriesActual
   global webEnvEntries
   global webEnvEntriesActual
   global servletInitParameters
   global servletInitParametersActual
   global ejbInterfaceBindings
   global ejbInterfaceBindingsActual
   global ejbBindings
   global ejbBindingsActual
   global mdbBindings
   global mdbBindingsActual
   global ejbReferences
   global ejbReferencesActual
   global appEnvEntries
   global appEnvEntriesActual
   global autoLinkActual
   global edition
   global editionDesc
   global extraOptions
   global serverVersion
   options.append('-MapModulesToServers')
   options.append(targetModules)
   print "tragetModules = %s " % targetModules
   if len(virtualHosts) > 0:
      options.append('-MapWebModToVH')
      options.append(virtualHostsActual)
   if len(contextRoots) > 0:
      options.append('-CtxRootForWebMod')
      options.append(contextRootsActual)
   if len(resourceEnvReferences) > 0:
      options.append('-MapResEnvRefToRes')
      options.append(resourceEnvRefActual)
   if len(mdbBindings) > 0:
      options.append('-BindJndiForEJBMessageBinding')
      options.append(mdbBindingsActual)
   if len(sharedLibraries) > 0:
      options.append('-MapSharedLibForMod')
      options.append(sharedLibrariesFinal)
   if metadataComplete == 'true':
      if len(applicationRoles) > 0:
         options.append('-MapRolesToUsers')
         options.append(applicationRoles)
      if len(resourceReferences) > 0:
         options.append('-MapResRefToEJB')
         options.append(resourceRefActual)
      if len(ejbEnvEntries) > 0:
         options.append('-MapEnvEntryForEJBMod')
         options.append(ejbEnvEntriesActual)
      if len(webEnvEntries) > 0:
         options.append('-MapEnvEntryForWebMod')
         options.append(webEnvEntriesActual)
      if len(servletInitParameters) > 0:
         options.append('-MapInitParamForServlet')
         options.append(servletInitParametersActual)
      if len(ejbInterfaceBindings) > 0:
         options.append('-BindJndiForEJBBusiness')
         options.append(ejbInterfaceBindingsActual)
      if len(ejbBindings) > 0:
         options.append('-BindJndiForEJBNonMessageBinding')
         options.append(ejbBindingsActual)
      if len(ejbReferences) > 0:
         options.append('-MapEJBRefToEJB')
         options.append(ejbReferencesActual)
      if len(appEnvEntries) > 0:
         options.append('-MapEnvEntryForApp')
         options.append(appEnvEntriesActual)
   if serverVersion >= '7.0': options.append(autoLinkActual)
   if len(edition) > 0:
      options.append('-edition')
      options.append(edition)
      if len(editionDesc) > 0:
         options.append('-edition.desc')
         options.append(editionDesc)
   if len(extraOptions) > 0:
      for option in extraOptions: options.append(option)

def completeEdit(metadataComplete):
   global appName
   global resourceEnvReferences
   global resourceReferences
   global applicationRoles
   global ejbEnvEntries
   global webEnvEntries
   global ejbInterfaceBindings
   global ejbBindings
   global mdbBindings
   global ejbReferences
   global appEnvEntries
   global wsPolicySets
   global scaWSBindings
   global scaEJBBindings
   global scaSCABindings
   global postSaveActions
   global scaModuleProperties
   global updateValidationDate
   global appClassloader
   global edition
   global createNewServicePolicy
   global cellType
   global latestChangedFiles
   if len(resourceEnvReferences) > 0: AdminApp.edit(appName, ['-MapResEnvRefToRes', resourceEnvRefActual])
   if metadataComplete == 'false':
      if len(resourceReferences) > 0:
         resourceRefActual = retrieveReferences(appName, 'EDIT', 'false')
         for ref in resourceReferences:
            found = 0
            for refActual in resourceRefActual:
               if isinstance(ref[0], type('')) == 1:
                  if ref[0] == refActual[3]:
                     refActual[5] = ref[1]
                     found = 1
               elif isinstance(ref[0], type([])) == 1:
                  if ref[0][1] == refActual[3]:
                     if (len(refActual[1]) == 0 and refActual[0] == ref[0][0]) or (len(refActual[1]) > 0 and refActual[1] == ref[0][0]):
                        refActual[5] = ref[1]
                        found = 1
                        break
            if found == 0:
               clearExit("ERROR: The Resource Reference %s is not present in the application %s.\nThe available resource references are: %s" % (ref[0], appName, getSingleList(resourceRefActual, 3)), -1)
         AdminApp.edit(appName, ['-MapResRefToEJB', resourceRefActual])
      if len(applicationRoles) > 0:
         roles = retrieveRoles(appName, 'EDIT')
         for role in applicationRoles:
            if role[0] not in roles:
               clearExit("ERROR: The role %s is not present in the application %s\nThe available roles are: %s" % (role[0], appName, roles), -1)
         AdminApp.edit(appName, ['-MapRolesToUsers', applicationRoles])
      if len(ejbEnvEntries) > 0:
         ejbEnvEntriesActual = retrieveEJBEnvEntries(appName, 'EDIT')
         for entry in ejbEnvEntries:
            found = 0
            for entryActual in ejbEnvEntriesActual:
               if entry[0] == entryActual[0] and \
                  entry[1] == entryActual[2] and \
                  entry[2] == entryActual[3]:
                  entryActual[6] = entry[3]
                  found = 1
                  break
            if found == 0:
               clearExit("ERROR: The EJB Environment Entry %s/%s/%s is not present in the application %s.\nThe available EJB env entries are: %s" % \
                        (entry[0], entry[1], entry[2], appName, getTuple(ejbEnvEntriesActual, [0, 2, 3])), -1)
         AdminApp.edit(appName, ['-MapEnvEntryForEJBMod', ejbEnvEntriesActual])
      if len(webEnvEntries) > 0:
         webEnvEntriesActual = retrieveWebEnvEntries(appName, 'EDIT')
         for entry in webEnvEntries:
            found = 0
            for entryActual in webEnvEntriesActual:
               if entry[0] == entryActual[0] and \
                  entry[1] == entryActual[2]:
                  entryActual[5] = entry[2]
                  found = 1
                  break
            if found == 0:
               clearExit("ERROR: The WEB Environment Entry %s/%s is not present in the application %s.\nThe available WEB env entries are: %s" % \
                        (entry[0], entry[1], appName, getTuple(webEnvEntriesActual, [0, 2])), -1)
         AdminApp.edit(appName, ['-MapEnvEntryForWebMod', webEnvEntriesActual])
      if len(servletInitParameters) > 0:
         servletInitParametersActual = retrieveServletInitParameters(appName, 'EDIT')
         for entry in servletInitParameters:
            found = 0
            for entryActual in servletInitParametersActual:
               if entry[0] == entryActual[0] and \
                  entry[1] == entryActual[2] and \
                  entry[2] == entryActual[3]:
                  entryActual[5] = entry[3]
                  found = 1
                  break
            if found == 0:
               clearExit("ERROR: The Servlet Init Parameter %s/%s/%s is not present in the application %s.\nThe available Servlet Init Parameters are: %s" % \
                        (entry[0], entry[1], entry[2], appName, getTuple(servletInitParametersActual, [0, 2, 3])), -1)
         AdminApp.edit(appName, ['-MapInitParamForServlet', servletInitParametersActual])
      if len(ejbInterfaceBindings) > 0:
         ejbInterfaceBindingsActual = retrieveEJBInterfaces(appName, 'EDIT')
         for entry in ejbInterfaceBindings:
            found = 0
            for entryActual in ejbInterfaceBindingsActual:
               if entry[0] == entryActual[0] and \
                  entry[1] == entryActual[1] and \
                  entry[2] == entryActual[3]:
                  entryActual[4] = entry[3]
                  found = 1
                  break
            if found == 0:
               clearExit("ERROR: The EJB Interface Binding %s/%s/%s is not present in the application %s.\nThe available EJB interfaces are: %s" % \
                        (entry[0], entry[1], entry[2], appName, getTuple(ejbInterfaceBindingsActual, [0, 1, 3])), -1)
         AdminApp.edit(appName, ['-BindJndiForEJBBusiness', ejbInterfaceBindingsActual])
      if len(ejbBindings) > 0:
         ejbBindingsActual = retrieveEJBs(appName, 'EDIT')
         for entry in ejbBindings:
            found = 0
            for entryActual in ejbBindingsActual:
               if entry[0] == entryActual[0] and \
                  entry[1] == entryActual[1]:
                  entryActual[3] = entry[2]
                  entryActual[4] = entry[3]
                  entryActual[5] = entry[4]
                  found = 1
                  break
            if found == 0:
               clearExit("ERROR: The EJB Binding %s/%s is not present in the application %s.\nThe available EJB bindings are: %s" % \
                        (entry[0], entry[1], appName, getTuple(ejbBindingsActual, [0, 1])), -1)
         AdminApp.edit(appName, ['-BindJndiForEJBNonMessageBinding', ejbBindingsActual])
      if len(ejbReferences) > 0:
         ejbReferencesActual = retrieveEJBReferences(appName, 'EDIT')
         for entry in ejbReferences:
            found = 0
            for entryActual in ejbReferencesActual:
               if entry[0] == entryActual[3]:
                  entryActual[5] = entry[1]
                  found = 1
                  break
            if found == 0:
               clearExit("ERROR: The EJB Reference %s is not present in the application %s.\nThe available EJB references are: %s" % \
                        (entry[0], appName, getSingleList(ejbReferencesActual, 3)), -1)
         AdminApp.edit(appName, ['-MapEJBRefToEJB', ejbReferencesActual])
      if len(appEnvEntries) > 0:
         appEnvEntriesActual = retrieveAppEnvEntries(appName, 'EDIT')
         for entry in appEnvEntries:
            found = 0
            for entryActual in appEnvEntriesActual:
               if entry[0] == entryActual[0]:
                  entryActual[3] = entry[1]
                  found = 1
                  break
            if found == 0:
               clearExit("ERROR: The APP Env Entry %s is not present in the application %s.\nThe available APP env entries are: %s" % \
                        (entry[0], appName, getSingleList(appEnvEntriesActual, 0)), -1)
         AdminApp.edit(appName, ['-MapEnvEntryForApp', appEnvEntriesActual])
   if len(wsPolicySets) > 0 and len(scaWSBindings) == 0: attachPolicySets(appName, wsPolicySets)
   if len(scaWSBindings) > 0:
      for sca in scaWSBindings: AdminTask.modifySCAImportWSBinding(['-moduleName', sca[0], '-import', sca[1], '-endpoint', sca[2], '-applicationName', appName])
      print "SCA import Web Services binding(s) modified successfully: %d" % len(scaWSBindings)
      if len(wsPolicySets) > 0: attachPolicySets(wsPolicySets)
   if len(scaEJBBindings) > 0:
      for sca in scaEJBBindings: AdminTask.modifySCAImportEJBinding(['-moduleName', sca[0], '-import', sca[1], '-jndiName', sca[2], '-applicationName', appName])
      print "SCA import EJB binding(s) modified successfully: %d" % len(scaEJBBindings)
   if len(scaSCABindings) > 0: postSaveActions = 'true'
   if len(scaModuleProperties) > 0:
      for sca in scaModuleProperties:
         if len(sca[2]) > 0: property = '[%s]%s' % (sca[2], sca[1])
         else: property = sca[1]
         AdminTask.modifySCAModuleProperty(['-moduleName', sca[0], '-propertyName', property, '-newPropertyValue', sca[3], '-applicationName', appName])
      print "SCA module propertie(s) modified successfully: %d" % len(scaModuleProperties)
   if hasBPELComponents(appName) == 'true':
      print "WARNING: The application %s contains at least one Business Process or Human Task instance" % (appName)
      if updateValidationDate == 'true': updateBPELValidationDate(appName)
   setAppClassLoader(appName, appClassloader)
   appdepid = getApplicationDeployment(appName, edition)
   AdminConfig.modify(appdepid, [ ['startingWeight', startingWeight], ['warClassLoaderPolicy', warClassLoaderPolicy] ])
   if createNewServicePolicy == 'true' and cellType == 'DISTRIBUTED': createServicePolicy(appName, edition)
   if len(latestChangedFiles) > 0:
      for latestFile in latestChangedFiles:
         options = ['-operation', 'addupdate', '-contents', latestFile[1], '-noprocessEmbeddedConfig', '-contenturi', latestFile[0]]
         AdminApp.update(appName, 'file', options)
         print "Updated/Added resource %s with file %s" % (latestFile[0], latestFile[1])

def validateCmdLine(data):
   argc = len(data)
   if argc < 1: return 'false'
   if data[0] == '-nosave': 
      nosave = 1
      action = data[1].upper()
      if action not in ['INSTALL', 'UPDATE', 'EDIT', 'ROLLOUT', 'UNINSTALL', 'REMOVE']: return 'false'
   else: 
      nosave = 0
      action = data[0].upper()
      if action not in ['INSTALL', 'UPDATE', 'ROLLOUT', 'UNINSTALL', 'ACTIVATE', 'DEACTIVATE', 'EDITION', 'VERSION', 'ROLLOUTEDITION', 'EDIT', 'REMOVE', 'MANAGE']: return 'false'
   if argc == 1 and action == 'VERSION': return 'true'
   if argc < (2 + nosave): return 'false'
   if action == 'EDITION':
      if argc == 2: return 'true'
      else: return 'false'
   if action in ['ROLLOUT', 'ACTIVATE', 'DEACTIVATE', 'ROLLOUTEDITION', 'UPDATE', 'EDIT', 'REMOVE', 'MANAGE']:
      if argc < (3 + nosave): return 'false'
   if action in ['INSTALL']:
      if argc < (4 + nosave): return 'false'
   if action == 'MANAGE':
      if data[2] not in ['start', 'stop', 'restart', 'status']: return 'false'
   return 'true'

def printCmdLineSyntax():
   print "Usage: %s INSTALL [-nosave] <application name> <application path> {<target data file>} [-targetObjects=<target>{,<target>}]" % (scriptName)
   print "       %s UPDATE [-nosave] <application name> <data path> {<target data file>}" % (scriptName)
   print "       %s EDIT [-nosave] <application name> {<target data file>}+" % (scriptName)
   print "       %s ROLLOUT [-nosave] <application name> <application path> {<target data file>}" % (scriptName)
   print "       %s UNINSTALL [-nosave] <application name> {<target data file>}" % (scriptName)
   print "       %s REMOVE [-nosave] <application name> {<target data file>}+" % (scriptName)
   print "       %s ACTIVATE <application name> {<target data file>}+" % (scriptName)
   print "       %s DEACTIVATE <application name> {<target data file>}+" % (scriptName)
   print "       %s ROLLOUTEDITION <application name> {<target data file>}+" % (scriptName)
   print "       %s VERSION [-long] {<application name>} (-long: print the vesion along with the information on the targets)" % (scriptName)
   print "       %s EDITION <application name>" % (scriptName)
   print "       %s MANAGE <application name> start|stop|restart|status {<target>}" % (scriptName)
   print "       <application name> ::= The application name"
   print "       <application path> ::= The absolute path of the EAR file"
   print "       <data path> :: = <application path>|<file path>|<module path>|<zip file path>"
   print "       <target data file> ::= Jython Property file or Java Property file (.properties files)"
   print "       <target> ::= A cluster or an application server involved on command"
   print "                    The application server syntax is [<node>:<server>]"

# Start
print "%s V%s" % (scriptName, version)



def start(args):
# Command Line
    print "Begin AdminApp with arg %s" %(args)
    global appClassloader
    global appEnvEntries
    global applicationRoles
    global contextRoots
    global createNewServicePolicy
    global drainageInterval
    global edition
    global editionDesc
    global ejbAutoLink
    global ejbBindings
    global ejbEnvEntries    
    global ejbInterfaceBindings
    global ejbReferences
    global extraOptions
    global forceHttpOnly
    global forceHttpsCookies
    global forceSecurityIntegration
    global forceSessionPath
    global forceUpdateOnly
    global latestChangedFiles
    global mdbBindings
    global metadataComplete
    global propagatePlugin
    global resourceEnvReferences
    global resourceReferences
    global rolloutGroupSize
    global rolloutResetStrategy
    global rolloutStrategy
    global scaEJBBindings
    global scaModuleProperties
    global scaSCABindings
    global scaWSBindings
    global servletInitParameters
    global sharedLibraries
    global startApplication
    global startingWeight
    global syncDelay
    global targetObjects
    global timeoutRollout
    global virtualHosts
    global updateContentType
    global updateContentURI
    global updateValidationDate
    global warClassLoaderPolicy
    global webEnvEntries
    global wsPolicySets
    
    global needPropagation
    global postSaveActions
    global targetModules
    global allModules
    global virtualHostsActual
    global contextRootsActual
    global sharedLibrariesActual
    global sharedLibrariesFinal
    global resourceRefActual
    global resourceEnvRefActual
    global ejbEnvEntriesActual
    global webEnvEntriesActual
    global ejbInterfaceBindingsActual
    global ejbBindingsActual
    global mdbBindingsActual
    global ejbReferencesActual
    global appEnvEntriesActual
    global servletInitParametersActual
    global autoLinkActual
    global cellType
    global appName
    global appLocation
    global action
    global lineSeparator
    global serverVersion
    lineSeparator = System.getProperty('line.separator')
    arguments = args
    
    if validateCmdLine(args) == 'false':
       print "ERROR: Command Line Parameters are empty or not correct"
       printCmdLineSyntax()
       clearExit("", -1)
    
    # Command Line Arguments
    appName = ''                      # Mandatory: (INSTALL, UPDATE, ROLLOUT, UNINSTALL, ACTIVATE, DEACTIVATE, EDITION, ROLLOUTEDITION, EDIT, REMOVE) - Optional: (VERSION)
    appLocation = ''                  # Mandatory: (INSTALL, UPDATE, ROLLOUT)
    # Retrieve action
    nosave = 0
    if arguments[0] == '-nosave': nosave = 1
    if nosave == 1: action = arguments[1].upper()
    else: action = arguments[0].upper()
    # Retrieve application name
    if action != 'VERSION': appName = arguments[1 + nosave]
    
    # Retrieve application path
    if action in ['INSTALL', 'UPDATE', 'ROLLOUT']:
       appLocation = arguments[2 + nosave]
       startIndex = 3 + nosave
    elif action == 'VERSION':
       startIndex = len(arguments)
    elif action == 'MANAGE':
       subaction = arguments[2]
       manageTargets = arguments[3:]
       startIndex = len(arguments)
    else:
       startIndex = 2 + nosave
    
    # Read target data file
    numfile = len(arguments) - startIndex
    if numfile > 0: 
       if arguments[startIndex + numfile -1].startswith('-targetObjects='):
          if action in ['INSTALL']:
             value = arguments[startIndex + numfile -1][15:]
             try:
                targetObjects = value.split(',')
                numfile = numfile - 1
             except:
                clearExit("KO: targetObjects syntax error or not valid syntax [%s]" % (value))
          else:
             print "ERROR: Command Line Parameters are not correct"
             printCmdLineSyntax()
             clearExit("", -1)
       print "Read %d target data file(s) ..." % numfile
       for i in range(numfile): 
          try:
             filename = arguments[startIndex + i]
             print "Read file %s:" % filename,
             if filename.endswith('.properties'):
                inStream = FileInputStream(filename)
                props = Properties()
                props.load(inStream)
                readProperties(props)
             else:
                execfile(filename)
             print "OK"
          except IOError, ioe:
             clearExit("KO (ERROR: %s)" % str(ioe), -1)
          except:
             type, value, traceback = sys.exc_info()
             clearExit("KO (ERROR: %s (%s))" % (str(value), type), -1)
       print "Read %d target data file(s) done" % numfile
    
    # Retrieve Cell Type
    cellType = AdminConfig.showAttribute(AdminConfig.list('Cell'), 'cellType')
    print "Cell Type: %s" % cellType
    if cellType not in ['STANDALONE', 'DISTRIBUTED']:
       clearExit("ERROR: The type of connectd server is not valid", -1)
    # Retrieving the server version
    if cellType == 'DISTRIBUTED':
       serverVersion = AdminControl.getAttribute(AdminControl.queryNames('WebSphere:*,type=Server,j2eeType=J2EEServer,name=dmgr'), 'platformVersion')
    else:
       serverVersion = AdminControl.getAttribute(AdminControl.queryNames('WebSphere:*,type=Server,j2eeType=J2EEServer,name=*'), 'platformVersion')
    print "Server Version: %s" % serverVersion
    if serverVersion < '6.1': clearExit("ERROR: Too old version of WAS.\nThe script is compatible with WAS 6.1 and later", -1)

    # Check all given parameters
    if action not in ['VERSION', 'MANAGE', 'UPDATE'] or (action == 'UPDATE' and numfile > 0): checkToDo = 1
    else: checkToDo = 0
    if checkToDo == 1: print "Check all given parameters ..."
    checkAllParameters(numfile)
    if checkToDo == 1: print "Check all given parameters done"
    
    if action == 'INSTALL':
       print "Install Application %s ..." % (appName)
       try:
          if appName in AdminApp.list().splitlines():
             buildId = getVersion(appName) 
             clearExit("ERROR: Application %s already exists (buildId = %s)" % (appName, buildId), -1)
          # Prepare installation options
          options = ['-appname', appName, '-noprocessEmbeddedConfig', '-installed.ear.destination', '${APP_INSTALL_ROOT}/${CELL}']
          
          # Deploy EJB
          oldEJB = isEJBDeployable(appLocation)
          if oldEJB == 1:
          	 options.append('-deployejb')
          	 print "Enabled EJBDeploy feature ..."
          else:
             options.append('-nodeployejb')
          # Metadata Complete
          if serverVersion >= '7.0': completeOptions(options, metadataComplete)
          else: completeOptions(options, 'true')
          
          # Install application
          AdminApp.install(appLocation, options)
          if len(edition) > 0: appName += '-edition' + edition
          completeEdit(metadataComplete)
          
          # Session Management
          #manageSession(appName, forceHttpOnly, forceHttpsCookies, forceSecurityIntegration, forceSessionPath)
          
          # Print Build Version
          print "Installed Version: %s" % getVersion(appName)
          
          # Print Target Servers
          print "Application deployed on:"
          printTargetServers(appName)
          
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    
    elif action == 'UNINSTALL':
       if len(edition) > 0: appName += '-edition' + edition
       print "Uninstall Application %s ..." % (appName)
       try:
          if appName not in AdminApp.list().splitlines():
             clearExit("ERROR: Application %s is not installed" % (appName), -1)
          print "Installed Version: %s" % (getVersion(appName))
          print "Application deployed on:"
          printTargetServers(appName)
          if hasBPELComponents(appName) == 'true':
             print "WARNING: The application %s contains at least one Business Process or Human Task instance" % (appName)
             targets = getTargets(appName)
             for target in targets:
                if target.find(',cluster=') != -1:
                   beg = target.find(',cluster=') + len(',cluster=')
                   clustername = target[beg:]
                   id = AdminConfig.getid('/ServerCluster:' + clustername + '/')
                   members = AdminConfig.showAttribute(id, 'members')[1:-1].split()
                   test = 0
                   for member in members: 
                      ltarget = 'WebSphere:node=%s,process=%s,*' % (AdminConfig.showAttribute(member, 'nodeName'), AdminConfig.showAttribute(member, 'memberName'))
                      test += len(AdminControl.queryNames(ltarget))
                      if test > 0: break
                   if test == 0:
                      clearExit("ERROR: The target %s is not running" % (target), -1)
                else:
                   if len(AdminControl.queryNames(target + ',*')) == 0:
                      clearExit("ERROR: The target %s is not running" % (target), -1)
          
          # Service Policy
          removeServicePolicy(appName)
          
          # Propagation plugin
          if propagatePlugin == 'true':
             needPropagation = 'true'
             targetModules, allModules = retrieveModules(appName, 'EDIT')
          
          # Uninstall application
          AdminApp.uninstall(appName)
          
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    
    elif action == 'REMOVE':
       if len(edition) > 0: appName += '-edition' + edition
       print "Removing %s for application %s ..." % (updateContentURI, appName)
       try:
          if appName not in AdminApp.list().splitlines():
             clearExit("ERROR: Application %s is not installed" % (appName), -1)
          print "Installed Version: %s" % (getVersion(appName))
          print "Application deployed on:"
          printTargetServers(appName)
          if hasBPELComponents(appName) == 'true':
             print "WARNING: The application %s contains at least one Business Process or Human Task instance" % (appName)
             targets = getTargets(appName)
             for target in targets:
                if target.find(',cluster=') != -1:
                   beg = target.find(',cluster=') + len(',cluster=')
                   clustername = target[beg:]
                   id = AdminConfig.getid('/ServerCluster:' + clustername + '/')
                   members = AdminConfig.showAttribute(id, 'members')[1:-1].split()
                   test = 0
                   for member in members: 
                      ltarget = 'WebSphere:node=%s,process=%s,*' % (AdminConfig.showAttribute(member, 'nodeName'), AdminConfig.showAttribute(member, 'memberName'))
                      test += len(AdminControl.queryNames(ltarget))
                      if test > 0: break
                   if test == 0:
                      clearExit("ERROR: The target %s is not running" % (target), -1)
                else:
                   if len(AdminControl.queryNames(target + ',*')) == 0:
                      clearExit("ERROR: The target %s is not running" % (target), -1)
    
          # Prepare update options
          options = ['-operation', 'delete', '-contenturi', updateContentURI]
          
          # Update application
          AdminApp.update(appName, updateContentType, options)
          
          # Propagation plugin
          if propagatePlugin == 'true':
             needPropagation = 'true'
             targetModules, allModules = retrieveModules(appName, 'EDIT')
          
          # Update done
          print "%s removed successfully for application %s" % (updateContentURI, appName)
          
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    elif action == 'UPDATE':
       if len(edition) > 0: appName += '-edition' + edition
       print "Update Application %s ..." % (appName)
       try:
          if appName not in AdminApp.list().splitlines():
             clearExit("ERROR: Application %s is not installed" % (appName), -1)
          print "Installed Version: %s" % (getVersion(appName))
          print "Application deployed on:"
          printTargetServers(appName)
          if hasBPELComponents(appName) == 'true':
             print "WARNING: The application %s contains at least one Business Process or Human Task instance" % (appName)
             targets = getTargets(appName)
             for target in targets:
                if target.find(',cluster=') != -1:
                   beg = target.find(',cluster=') + len(',cluster=')
                   clustername = target[beg:]
                   id = AdminConfig.getid('/ServerCluster:' + clustername + '/')
                   members = AdminConfig.showAttribute(id, 'members')[1:-1].split()
                   test = 0
                   for member in members: 
                      ltarget = 'WebSphere:node=%s,process=%s,*' % (AdminConfig.showAttribute(member, 'nodeName'), AdminConfig.showAttribute(member, 'memberName'))
                      test += len(AdminControl.queryNames(ltarget))
                      if test > 0: break
                   if test == 0:
                      clearExit("ERROR: The target %s is not running" % (target), -1)
                else:
                   if len(AdminControl.queryNames(target + ',*')) == 0:
                      clearExit("ERROR: The target %s is not running" % (target), -1)
    
          # Prepare update options
          operation = 'addupdate';
          if updateContentType == 'app' or forceUpdateOnly == 'true': operation = 'update'
          options = ['-operation', operation, '-contents', appLocation, '-noprocessEmbeddedConfig']
          oldEJB = isEJBDeployable(appLocation)
          if oldEJB == 1:
          	 options.append('-deployejb')
          	 print "Enabled EJBDeploy feature ..."
          else:
             options.append('-nodeployejb')
          if numfile == 0: options.append('-update.ignore.new')
          if updateContentType in ['file', 'modulefile', 'partialapp']: 
             options.append('-contenturi')
             options.append(updateContentURI)
       
          if updateContentType not in ['file', 'partialapp']:
             if numfile > 0:
                # Metadata Complete
                if serverVersion >= '7.0': completeOptions(options, metadataComplete)
                else: completeOptions(options, 'true')
          
          # Update application
          print " appName = %s" %(appName)
          print " updateContentType = %s" %(updateContentType)
          print " options = %s" %(options)
          
          AdminApp.update(appName, updateContentType, options)
          
          if updateContentType not in ['file', 'partialapp']:
             completeEdit(metadataComplete)
             AdminApp.edit(appName, ['-MapModulesToServers', targetModules])         
          
          # Session Management
          manageSession(appName, forceHttpOnly, forceHttpsCookies, forceSecurityIntegration, forceSessionPath)
          
          # Print Build Version
          print "Updated Version: %s" % (getVersion(appName))
          
          # Print Target Servers
          print "Application deployed on:"
          printTargetServers(appName)
    
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    
    elif action == 'EDIT':
       if len(edition) > 0: appName += '-edition' + edition
       print "Edit Application %s ..." % (appName)
       try:
          if appName not in AdminApp.list().splitlines():
             clearExit("ERROR: Application %s is not installed" % (appName), -1)
          print "Installed Version: %s" % (getVersion(appName))
          print "Application deployed on:"
          printTargetServers(appName)
          if hasBPELComponents(appName) == 'true':
             print "WARNING: The application %s contains at least one Business Process or Human Task instance" % (appName)
             targets = getTargets(appName)
             for target in targets:
                if target.find(',cluster=') != -1:
                   beg = target.find(',cluster=') + len(',cluster=')
                   clustername = target[beg:]
                   id = AdminConfig.getid('/ServerCluster:' + clustername + '/')
                   members = AdminConfig.showAttribute(id, 'members')[1:-1].split()
                   test = 0
                   for member in members: 
                      ltarget = 'WebSphere:node=%s,process=%s,*' % (AdminConfig.showAttribute(member, 'nodeName'), AdminConfig.showAttribute(member, 'memberName'))
                      test += len(AdminControl.queryNames(ltarget))
                      if test > 0: break
                   if test == 0:
                      clearExit("ERROR: The target %s is not running" % (target), -1)
                else:
                   if len(AdminControl.queryNames(target + ',*')) == 0:
                      clearExit("ERROR: The target %s is not running" % (target), -1)
    
          # Prepare update options
          options = []
          completeOptions(options, 'true')
             
          # Edit Application
          AdminApp.edit(appName, options)
          completeEdit('true')
          
          # Session Management
          manageSession(appName, forceHttpOnly, forceHttpsCookies, forceSecurityIntegration, forceSessionPath)
          
          # Print Target Servers
          print "Application deployed on:"
          printTargetServers(appName)
          
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    
    elif action == 'ROLLOUT':
       if len(edition) > 0: appName += '-edition' + edition
       print "Rollout Update for Application %s ..." % (appName)
       try:
          if appName not in AdminApp.list().splitlines():
             clearExit("ERROR: Application %s is not installed" % (appName), -1)
          print "Installed Version: %s" % (getVersion(appName))
          print "Application deployed on:"
          printTargetServers(appName)
          if hasBPELComponents(appName) == 'true':
             clearExit("ERROR: The application %s contains at least one Business Process or Human Task instance. Use the update action instead" % (appName), -1)
          
          # Prepare installation options
          options = ['-operation', 'update', '-contents', appLocation, '-noprocessEmbeddedConfig']
          
          # Metadata Complete
          if serverVersion >= '7.0': completeOptions(options, metadataComplete)
          else: completeOptions(options, 'true')
          
          # Update application
          AdminApp.update(appName, 'app', options)
          completeEdit(metadataComplete)
          
          # Session Management
          manageSession(appName, forceHttpOnly, forceHttpsCookies, forceSecurityIntegration, forceSessionPath)
          
          # Print Build Version
          print "Updated Version: %s" % (getVersion(appName))
          
          # Print Target Servers
          print "Application deployed on:"
          printTargetServers(appName)
    
          # Save
          if nosave == 0: AdminConfig.save()
          else: AdminConfig.reset()
          
          # Post Save Actions
          if nosave == 0 and postSaveActions == 'true':
             if len(scaSCABindings) > 0:
                try:
                   print "SCA import SCA binding ..."
                   for sca in scaSCABindings: 
                      if len(sca[4]) == 0: AdminTask.modifySCAImportSCABinding(['-moduleName', sca[0], '-import', sca[1], '-targetModule', sca[2], '-targetExport', sca[3], '-applicationName', appName])
                      else: AdminTask.modifySCAImportSCABinding(['-moduleName', sca[0], '-import', sca[1], '-targetModule', sca[2], '-targetExport', sca[3], '-applicationName', appName, '-targetApplicationName', sca[4]])
                   print "SCA import SCA binding(s) modified successfully: %d" % len(scaSCABindings)
                except:
                   type, value, traceback = sys.exc_info()
                   print "ERROR: %s (%s)" % (str(value), type)
                   clearAppAndExit(appName)
             AdminConfig.save()
    
          # Rollout Update
          print "Start Rollout Update"
          AdminTask.updateAppOnCluster('[-ApplicationNames [%s] -timeout %d]' %(appName, timeoutRollout))
          print "End Rollout Update"
          
          # Exit
          print "%s done" % scriptName
          sys.exit(0)
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    
    elif action == 'ACTIVATE':
       print "Activation for the edition %s of application %s ..." % (edition, appName)
       try:
          appNameWithEdition = appName + '-edition' + edition
          if appNameWithEdition not in AdminApp.list().splitlines():
             clearExit("ERROR: The edition %s for application %s is not installed" % (edition, appName), -1)
          state = AdminTask.getEditionState(['-appName', appName, '-edition', edition])
          if state != 'INACTIVE':
             clearExit("ERROR: The edition %s for application %s is not on the state INACTIVE" % (edition, appName), -1)
          ret = AdminTask.activateEdition(['-appName', appName, '-edition', edition])
          if ret == 'true':
             print "SUCCESS: The edition %s for application %s has been ACTIVATED" % (edition, appName)
          else:
             clearExit("ERROR: The edition %s for application %s has not been ACTIVATED" % (edition, appName), -1)
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    
    elif action == 'DEACTIVATE':
       print "Deactivation for the edition %s of application %s ..." % (edition, appName)
       try:
          appNameWithEdition = appName + '-edition' + edition
          if appNameWithEdition not in AdminApp.list().splitlines():
             clearExit("ERROR: The edition %s for application %s is not installed" % (edition, appName), -1)
          state = AdminTask.getEditionState(['-appName', appName, '-edition', edition])
          if state != 'ACTIVE':
             clearExit("ERROR: The edition %s for application %s is not on the state ACTIVE" % (edition, appName), -1)
          ret = AdminTask.deactivateEdition(['-appName', appName, '-edition', edition])
          if ret == 'true':
             print "SUCCESS: The edition %s for application %s has been DEACTIVATED" % (edition, appName)
          else:
             clearExit("ERROR: The edition %s for application %s has not been DEACTIVATED" % (edition, appName), -1)
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    
    elif action == 'ROLLOUTEDITION':
       print "Rollout for the edition %s of application %s ..." % (edition, appName)
       try:
          appNameWithEdition = appName + '-edition' + edition
          if appNameWithEdition not in AdminApp.list().splitlines():
             clearExit("ERROR: The edition %s for application %s is not installed" % (edition, appName), -1)
          state = AdminTask.getEditionState(['-appName', appName, '-edition', edition])
          if state != 'INACTIVE':
             clearExit("ERROR: The edition %s for application %s is not on the state INACTIVE" % (edition, appName), -1)
          params = [ ['rolloutStrategy', rolloutStrategy], ['resetStrategy', rolloutResetStrategy], ['drainageInterval', drainageInterval], ['quiesceStrategy', 'DEFAULT'] ]
          if rolloutStrategy == 'grouped': options.append(['groupSize', rolloutGroupSize])
          ret = AdminTask.rolloutEdition(['-appName', appName, '-edition', edition, '-params', params])
          if ret == 'true':
             print "SUCCESS: The edition %s for application %s has been ACTIVATED" % (edition, appName)
          else:
             clearExit("ERROR: The edition %s for application %s has not been ACTIVATED" % (edition, appName), -1)
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    
    elif action == 'EDITION':
       print "List the editions for the application %s ..." % (appName)
       try:
          editions = AdminTask.listEditions(['-appName', appName]).splitlines()
          for edition in editions:
             state = AdminTask.getEditionState(['-appName', appName, '-edition', edition])
             print "Edition: %s - State: %s" % (edition, state)
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)
    
    elif action == 'VERSION':
       print "Get application build id(s) ..."
       
       # Retrieve application names and format
       format = 'short'
       argc = len(arguments) - 1
       start = 1
       if argc > 0 and arguments[1] == '-long':
          format = 'long'
          argc = len(arguments) - 2
          start = 2
          print
       if argc > 0: 
          names = arguments[start:]
          listApps = AdminApp.list().splitlines()
       else:
          names = AdminApp.list().splitlines()
          listApps = names
    
       # Get App Module BuildID (and Target Servers)
       for name in names:
          try:
             found = 0
             for app in listApps:
                if app == name or app.find(name + '-edition') == 0:
                   data = getVersion(app)
                   found = 1
                   print "%s: %s" % (app, data)
                   if format == 'long':
                      printTargetServers(app)
                      print 
             if found == 0:
                print "%s: Not Deployed" % (name)
                if format == 'long': print 
          except:
             print "%s: N/A" % (name)
             if format == 'long': print
       
       if len(names) > 0 and format == 'long': print
       print "Get application build id(s) done"
    
    elif action == 'MANAGE':
       print "%s application %s ..." % (subaction.capitalize(), appName)
       try:
          if appName not in AdminApp.list().splitlines():
             clearExit("ERROR: The application %s is not installed" % (appName), -1)
          servers = []
          for target in manageTargets:
             if target.find(':') != -1:
                sep = target.find(':')
                servers.append([target[:sep], target[sep + 1:]])
             else:
                serverids = AdminConfig.getid('/Server:%s/' % target).splitlines()
                if len(serverids) > 0:
                   for serverid in serverids:
                      serverType = AdminConfig.showAttribute(serverid, 'serverType')
                      if serverType != 'APPLICATION_SERVER': continue
                      beg = serverid.find('/nodes/')
                      if beg == -1: continue
                      beg += len('/nodes/')
                      end = serverid.find('/servers/', beg)
                      if end == -1: continue
                      servers.append([serverid[beg:end], target])
                else:
                   clusterid = AdminConfig.getid('/ServerCluster:%s/' % target)
                   if len(clusterid) == 0: continue
                   members = AdminConfig.showAttribute(clusterid, 'members')[1:-1].split(' ')
                   if len(members) == 0: continue
                   for member in members: 
                      servers.append([AdminConfig.showAttribute(member, 'nodeName'), AdminConfig.showAttribute(member, 'memberName')])
          if len(manageTargets) == 0:
             targets = getTargets(appName)
             for target in targets:
                if target.find('cluster=') != -1:
                   cluster = target[target.find('cluster=') + len('cluster='):]
                   clusterid = AdminConfig.getid('/ServerCluster:%s/' % cluster)
                   if len(clusterid) == 0: continue
                   members = AdminConfig.showAttribute(clusterid, 'members')[1:-1].split(' ')
                   if len(members) == 0: continue
                   for member in members: 
                      servers.append([AdminConfig.showAttribute(member, 'nodeName'), AdminConfig.showAttribute(member, 'memberName')])
                else:
                   beg = target.find('node=') + len('node=')
                   end = target.find(',', beg)
                   node = target[beg:end]
                   server = target[target.find('server=') + len('server='):]
                   servers.append([node, server])
          for server in servers:
             appman = AdminControl.queryNames('WebSphere:*,type=ApplicationManager,node=%s,process=%s' % (server[0], server[1]))
             if len(appman) == 0 and subaction in ['start', 'stop', 'restart']: continue
             try:
                if subaction in ['start', 'stop', 'restart']:
                   print "%s on %s:%s ..." % (subaction.capitalize(), server[0], server[1])
                if subaction == 'start':
                   try: 
                      AdminControl.invoke(appman, '_canStopApplication', appName)
                      isStarted = 1
                      print "WARNING: Application %s is already started on %s:%s" % (appName, server[0], server[1])
                   except: isStarted = 0
                   if isStarted == 0: 
                      if AdminApp.isAppReady(appName) == 'true':
                         AdminControl.invoke(appman, 'startApplication', appName)
                      else: 
                         clearExit("The application %s is not ready to start" % (appName), -1)
                elif subaction == 'stop':
                   try: 
                      AdminControl.invoke(appman, '_canStopApplication', appName)
                   except:
                      print "WARNING: Application %s is not started on %s:%s" % (appName, server[0], server[1])
                      continue
                   AdminControl.invoke(appman, 'stopApplication', appName)
                elif subaction == 'restart':
                   try: 
                      AdminControl.invoke(appman, '_canStopApplication', appName)
                      isStopped = 'false'
                   except:
                      print "WARNING: Application %s is not started on %s:%s" % (appName, server[0], server[1])
                      isStopped = 'true'
                   if isStopped == 'false': AdminControl.invoke(appman, 'stopApplication', appName)
                   if AdminApp.isAppReady(appName) == 'true':
                      AdminControl.invoke(appman, 'startApplication', appName)
                   else: 
                      clearExit("The application %s is not ready to start" % (appName), -1)
                elif subaction == 'status':
                   print "%s:%s =" % (server[0], server[1]),
                   try: 
                      AdminControl.invoke(appman, '_canStopApplication', appName)
                      print "STARTED"
                   except:
                      print "STOPPED"
                if subaction in ['start', 'stop', 'restart']:
                   print "%s on %s:%s done" % (subaction.capitalize(), server[0], server[1])
             except:
                type, value, traceback = sys.exc_info()
                print "%s on %s:%s failed (%s)" % (subaction.capitalize(), server[0], server[1], str(value))
          
          print "%s application %s done" % (subaction.capitalize(), appName)
                                  
       except SystemExit, e: sys.exit(e)
       except:
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
          clearExit("Rollback and exit", -1)   
    
    if AdminConfig.hasChanges() == 1:
       if nosave == 0:
          # Save
          print "Save ..."
          AdminConfig.save()
          print "Save done"
       else:
          # Reset
          print "Reset ..."
          AdminConfig.reset()
          print "Reset done"
       
       # Check if there are post save actions
       if nosave == 0 and postSaveActions == 'true':
          print "Post Save Actions ..."
          
          # Update SCA Import Bindings
          if len(scaSCABindings) > 0:
             try:
                print "SCA import SCA binding ..."
                for sca in scaSCABindings: 
                   if len(sca[4]) == 0: AdminTask.modifySCAImportSCABinding(['-moduleName', sca[0], '-import', sca[1], '-targetModule', sca[2], '-targetExport', sca[3], '-applicationName', appName])
                   else: AdminTask.modifySCAImportSCABinding(['-moduleName', sca[0], '-import', sca[1], '-targetModule', sca[2], '-targetExport', sca[3], '-applicationName', appName, '-targetApplicationName', sca[4]])
                print "SCA import SCA binding(s) modified successfully: %d" % len(scaSCABindings)
             except:
                type, value, traceback = sys.exc_info()
                print "ERROR: %s (%s)" % (str(value), type)
                clearAppAndExit(appName)
          
          # Save
          print "Save ..."
          AdminConfig.save()
          print "Save done"
          print "Post Save Actions done"
    
       # Synchronization
       if nosave == 0 and cellType == 'DISTRIBUTED':
          print "Synchronization ..."
          nodes = AdminControl.queryNames('type=NodeSync,*')
          if len(nodes) > 0:
             nodelist = nodes.split(lineSeparator)
             if len(nodelist) > 0:
                for node in nodelist:
                   beg = node.find('node=') + 5
                   end = node.find(',', beg)
                   print "Synchronization for node \"" + node[beg:end] + "\" :",
                   try: AdminControl.invoke(node, 'sync')
                   except: print "KO"
                   else: print "OK"
                   if syncDelay > 0:
                      print "Sleep for %d second(s) ..." % syncDelay
                      time.sleep(syncDelay)
                      print "Sleep done"
          else:
             print "No running nodeagents found"
          print "Synchronization done"
    
    # Plug-in generation and propagation
    if nosave == 0 and needPropagation == 'true':
       print "Plug-in generation and propagation ..."
       try:
          connectedNode = AdminControl.getNode()
          nodeid = AdminConfig.getid('/Node:' + connectedNode + '/')
          variables = AdminConfig.list('VariableSubstitutionEntry', nodeid).splitlines()
          for variable in variables:
             name = AdminConfig.showAttribute(variable, 'symbolicName')
             if name == 'USER_INSTALL_ROOT':
                configPath = AdminConfig.showAttribute(variable, 'value') + '/config'
                break
          generator = AdminControl.completeObjectName('type=PluginCfgGenerator,*')
          webServers = getWebServers(targetModules)
          for webServer in webServers:
             try:
                print "WebServer %s:%s:" % (webServer[0], webServer[1]),
                AdminControl.invoke(generator, 'generate', '%s %s %s %s true' % (configPath, AdminControl.getCell(), webServer[0], webServer[1]))
                print "OK"
             except:
                type, value, traceback = sys.exc_info()
                print "KO (ERROR: %s (%s))" % (str(value), type)
       except:                  
          type, value, traceback = sys.exc_info()
          print "ERROR: %s (%s)" % (str(value), type)
       print "Plug-in generation and propagation done"
    
    # Start application
    if cellType == 'STANDALONE': nodes = ['DUMMY']
    if nosave == 0 and action == 'INSTALL' and startApplication == 'true' and len(nodes) > 0:
       print "Starting application %s ..." % (appName)
       if syncDelay > 0:
          for i in range(syncDelay):
             if AdminApp.isAppReady(appName) == 'false': time.sleep(1)
             else: break
       elif syncDelay == -1:
          print "Wait until the application %s is ready ..." % (appName)
          while AdminApp.isAppReady(appName) == 'false': time.sleep(1)
          print "Application %s is ready" % (appName)
       if AdminApp.isAppReady(appName) == 'true':
          nstarted = 0
          targetList = []
          targets = getTargets(appName)
          for target in targets:
             if target.find('cluster=') != -1:
                cluster = target[target.find('cluster=') + len('cluster='):]
                clusterid = AdminConfig.getid('/ServerCluster:%s/' % cluster)
                if len(clusterid) == 0: continue
                members = AdminConfig.showAttribute(clusterid, 'members')[1:-1].split(' ')
                if len(members) == 0: continue
                for member in members: 
                   targetList.append([AdminConfig.showAttribute(member, 'nodeName'), AdminConfig.showAttribute(member, 'memberName')])
             else:
                beg = target.find('node=') + len('node=')
                end = target.find(',', beg)
                node = target[beg:end]
                server = target[target.find('server=') + len('server='):]
                targetList.append([node, server])
          for server in targetList:
             appman = AdminControl.queryNames('WebSphere:*,type=ApplicationManager,node=%s,process=%s' % (server[0], server[1]))
             if len(appman) == 0: continue
             try:
                print "Starting application %s on server %s:%s ..." % (appName, server[0], server[1])
                AdminControl.invoke(appman, 'startApplication', appName)
                nstarted += 1
                print "Started application %s on server %s:%s" % (appName, server[0], server[1])
                time.sleep(1) # Mandatory delay
             except:
                type, value, traceback = sys.exc_info()
                print "ERROR: Starting application %s on server %s:%s failed (%s)" % (appName, server[0], server[1], str(value))
          if nstarted > 0: print "Application %s started on %d server(s)" % (appName, nstarted)
          else: print "Application %s is not started. Probably no target servers are running" % (appName)
       else: print "The application %s cannot be started because is not ready (probably not all the nodes are synchronized yet)" % (appName)
       print "Starting application %s done" % (appName)
    # Done
    #clearExit("", 0)

    
    