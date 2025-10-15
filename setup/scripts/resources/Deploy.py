#
# This scripts install the Miles EAR file
#
# Execute this as follows:
# wsadmin -profileName PRODUCTION -f deployMiles.py nodeName serverName cellName
#
# Modify these parameters
#
# Importing modules
## 2019.06.10 - Edited by Paolo Milani with IBM support
import sys
import time as Time
from time import sleep
#
# Parse argument
#

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
except:
    pass

if len(strip(nodeName)) == 0:
   clearExit(" ERROR: no SERVERNAME given! \n %s" %usage_command )
if len(strip(serverName)) == 0:
   clearExit(" ERROR: no NODENAME given! \n %s" %usage_command )
if len(strip(cellName)) ==0:
   clearExit(" ERROR: no CELLNAME given! \n %s " %usage_command )
if len(strip(appLocation)) ==0:
   clearExit(" ERROR: no APP_LOCATION given! \n %s " %usage_command )

appName = 'Miles_' + serverName
defaultHost = serverName + '_host'
#
# Display usage if there is no argument given
#
#        print "e.g.: ./wsadmin.sh -f deployMilesGeneric.py DEMO_SILKROAD server1 milessilkroaddevNode01Cell"
#
# Do the magic
#
webModule = "miles.war"
MMCModule = "mmc.war"
uri = "miles.war,WEB-INF/web.xml"
uri2 = "mmc.war,WEB-INF/web.xml"
mapWebOptions = [[webModule, uri, defaultHost],[MMCModule, uri2, defaultHost]]
#
webContext = serverName + "_miles"
MMCContext = serverName + "_mmc"
mapContextOptions = [[webModule , uri, webContext],[MMCModule, uri2, MMCContext]]
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
   print "Install Miles... ", 
   AdminApp.install(appLocation, ["-appname", appName, "-node", nodeName, "-cell", cellName, "-server", serverName, "-MapWebModToVH", mapWebOptions, "-CtxRootForWebMod", mapContextOptions])
   #AdminConfig.save()
except:
   type, value, traceback = sys.exc_info()
   print "ERROR: %s (%s)" % (str(value), type)
   clearExit("Error installing Miles Rollback and Exit",-1)

syncEnv(AdminConfig.hasChanges(),20)




# SYNCHRONIZE
#try:
#        nodeSync = AdminControl.completeObjectName("type=NodeSync,node="+nodeName+",*")
#        print "Invoking synchronization"
#        AdminControl.invoke(nodeSync,"sync")
#        print "Sleeping for 20 seconds"
#        Time.sleep(20)
#        print "Synchronization complete"
#except:
#        print "Error in synchronization"

# START
try:
    print "Starting Miles"
    AdminControl.invoke(am, 'startApplication', appName, '[java.lang.String]') 
except:
    print "Error starting Miles"
print 'Done updating ' + serverName + '!'
