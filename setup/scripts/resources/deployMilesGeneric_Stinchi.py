#
# This scripts install the Miles EAR file
#
# Execute this as follows:
# wsadmin -profileName PRODUCTION -f deployMiles.py nodeName serverName cellName
#
# Modify these parameters
#
appLocation = 'd:/local/miles/update/miles.ear'
# Importing modules
import sys
import time as Time
from time import sleep
#
# Parse argument
#
serverName = ''
nodeName = ''
scriptName="deployMilesGeneric.py"
version="1.0.0"
usage_command =" ./wsadmin.sh -f deployMilesGeneric.py NODENAME SERVERNAME CELLNAME APPLOCATION "
serverName = 'ITUP2'
nodeName = 'MirNode01'
cellName= 'AldProdCell'


print "%s v%s" %(scriptName,version)

# Auxiliary functions
def appIsRunning(name):
   appStatus=AdminControl.completeObjectName('type=Application,name='+str(name)+',*')
   if len(strip(appStatus)) == 0:
      return 0
   else:
      return 1
#end def
 
def clearExit(text, status):
   if len(text): 
      print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
return

def syncEnv(hasChanges,delay): 
   if hasChanges == 1: 
      print("Save ...") 
      AdminConfig.save() 
      print("Save done") 
      print("Synchronization ...") 
      nodes = AdminControl.queryNames('type=NodeSync,*') 
      if len(nodes) > 0: 
         nodelist = nodes.splitlines()       
         for node in nodelist: 
            beg = node.find('node=') + 5 
            end = node.find(',', beg) 
            print("Synchronization for node \"" + node[beg:end] + "\" :",1) ,
            try: AdminControl.invoke(node, 'sync') 
            except: print "KO"
            else: print "OK"
            print " waiting for %s seconds " %delay
            sleep(delay) 
         print "Synchronization done"     
      else: 
         print "No Nodeagent found " 
   else: 
       print "No changes made syncronization skipped" 
#end def
try:
        nodeName = sys.argv[0]
        serverName = sys.argv[1]
        cellName = sys.argv[2]
        appLocation = sys.argv[3]
        if len(sys.argv) > 4: 
            jee7 = sys.argv[4]
        else:
            jee7 = '0'
except:
        pass
print jee7
appName = 'Miles_' + serverName
defaultHost = serverName + '_host'
#
# Display usage if there is no argument given
#
if len(strip(nodeName)) == 0:
   clearExit(" ERROR: no SERVERNAME given! \n %s" %usage_command )
if len(strip(serverName)) == 0:
   clearExit(" ERROR: no NODENAME given! \n %s" %usage_command )
if len(strip(cellName)) ==0:
   clearExit(" ERROR: no CELLNAME given! \n %s " %usage_command )
if len(strip(appLocation)) ==0:
   clearExit(" ERROR: no APP_LOCATION given! \n %s " %usage_command )
#
#webServer1 = 'dOdrlib01'
#webNode1 = 'AldCoreDevxNode01'
#webServer2 = 'dOdrlib02'
#webNode2 = 'AldCoreDevxNode02'

#
# Do the magic
#
webModule = "miles.war"
MMCModule = "mmc.war"
OrbitModule = "orbit.war"
milesUri = "miles.war,WEB-INF/web.xml"
mmcUri = "mmc.war,WEB-INF/web.xml"
orbitUri = "orbit.war,WEB-INF/web.xml"
#
# mapping for rootcontext
#
webContext = "/" + serverName + "_miles" 
MMCContext = "/" + serverName + "_mmc" 
OrbitContext = "/" + serverName + "_orbit"
if jee7 == '0':
    mapWebOptions = [[webModule, milesUri, defaultHost],[MMCModule, mmcUri, defaultHost]]
    mapContextOptions = [[webModule, milesUri, webContext],[MMCModule, mmcUri, MMCContext]]
else:
    mapWebOptions = [[webModule, milesUri, defaultHost],[MMCModule, mmcUri, defaultHost],[OrbitModule, orbitUri, defaultHost]]
    mapContextOptions = [[webModule, milesUri, webContext],[MMCModule, mmcUri, MMCContext],[OrbitModule, orbitUri, OrbitContext]]
#
# mapping for modules
#
baseCampModule = "BaseCamp"
bean = "SofCommandQueue"
baseCampUri = "miles.jar,META-INF/ejb-jar.xml"
target = "mas/CommandActivationSpec"
destination = "/jms/SofCommandQueue"
BindJndi4EJBMessageBinding = [[ baseCampModule, bean, baseCampUri, "", target, destination, "" ]]
wmEJB = "CommandCtrl"
wmTarget = "wm/WorkManager"
wmResRefJNDI = "commonj.work.WorkManager"
wmResType = "wm/WorkManager"
wmTargetBQ = "wm/WorkManagerBQ"
wmResTypeBQ = "wm/WorkManagerBQ"
MapResRefToEJB = [[ baseCampModule, wmEJB, baseCampUri, wmTarget, wmResRefJNDI, wmResType, "", "", "" ] ,[ baseCampModule, wmEJB, baseCampUri, wmTargetBQ, wmResRefJNDI, wmResTypeBQ, "", "", "" ]]
milesServer = "WebSphere:cell=" + cellName + ",node=" + nodeName + ",server=" + serverName
webServer = "WebSphere:cell=" + cellName + ",node=" + nodeName + ",server=" + serverName + "+WebSphere:cell=" + cellName + ",node=" + webNode1 + ",server=" + webServer1 + "+WebSphere:cell=" + cellName + ",node=" + webNode2 + ",server=" + webServer2
mapModulesToServers = [[baseCampModule, baseCampUri, milesServer],[webModule, milesUri, webServer],[MMCModule, mmcUri, webServer]]
# Get Mbean
fubar = 'type=ApplicationManager,process=' + serverName + ',node=' + nodeName + ',cell=' + cellName + ',*'
am = AdminControl.queryNames(fubar)
#print am
if len(strip(am)) == 0:
   print "Application Server was alrady stopped NO need to stop Miles Application"
else:
    if appIsRunning(appName) == 1:
         try:  
            print "Stopping Miles ... ",
            AdminControl.invoke(am, 'stopApplication', appName, '[java.lang.String]')
            print " OK  " 
         except:
            print " KO "
            type, value, traceback = sys.exc_info() 
            print "ERROR: %s (%s)" %(str(value), type)
            print "Error stopping Miles"
    else:
       print " Application Miles  was already stopped NO need to stop " 


   # UNINSTALL
try:
    print "Uninstall Miles ...  ",
    AdminApp.uninstall(appName)
    print " OK " 
    # AdminConfig.save()
except:
     type, value, traceback = sys.exc_info()
     print "ERROR: %s (%s)" % (str(value), type)
     print "Error uninstalling Miles, maybe Miles was not installed?"

# INSTALL
try:
    print "Install Miles"
    if jee7 == '0':
        #AdminApp.install(appLocation, ["-appname", appName, "-node", nodeName, "-cell", cellName, "-server", serverName, "-MapWebModToVH", mapWebOptions, "-CtxRootForWebMod", mapContextOptions, "-MapModulesToServers", mapModulesToServers])
        AdminApp.install(appLocation, ["-appname", appName, "-node", nodeName, "-cell", cellName, "-server", serverName, "-MapWebModToVH", mapWebOptions, "-CtxRootForWebMod", mapContextOptions])
    else:
        print "Install JEE7"
        AdminApp.install(appLocation, ["-appname", appName, "-node", nodeName, "-cell", cellName, "-server", serverName, "-MapWebModToVH", mapWebOptions, "-CtxRootForWebMod", mapContextOptions, "-MapModulesToServers", mapModulesToServers, "-BindJndiForEJBMessageBinding", BindJndi4EJBMessageBinding, "-MapResRefToEJB", MapResRefToEJB])
    #AdminConfig.save()
except:
   type, value, traceback = sys.exc_info()
   print "ERROR: %s (%s)" % (str(value), type)
   clearExit("Error installing Miles Rollback and Exit",-1)
# SYNCHRONIZE
syncEnv(AdminConfig.hasChanges(),20)


# Stop Servers
try:
#stop procedure
    runningServer = AdminControl.queryNames("WebSphere:name="+serverName+",type=Server,node="+nodeName+",processType=ManagedProcess,*")
    if (len(runningServer) == 0):
        print "Server %s was stopped already "  %serverName
    else:
        serverName = AdminControl.getAttribute(runningServer, "name")
        print "Stop server: %s" %serverName
        AdminControl.stopServer(serverName, nodeName)
        print "Server: %s is Stopped" %serverName
except:
        type, value, traceback = sys.exc_info()
        print "START AS - ERROR: %s (%s)" % (str(value), type)

#start procedure
try:
        print "Starting Application Server %s" %serverName
        AdminControl.startServer(serverName, nodeName)
except:
        type, value, traceback = sys.exc_info()
        print "STOP AS - ERROR: %s (%s)" % (str(value), type)
        
print "Application Install Procedure Complete"

print "%s v%s Finished" %(scriptName,version)
