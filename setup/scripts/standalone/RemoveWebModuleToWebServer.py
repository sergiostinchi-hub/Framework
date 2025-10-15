# Author: Stinchi Sergio

# Version        Description
# 1.0.0          Starting version

import os
import java.io.File as f
import sys
from time import gmtime, strftime


commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))

# Info Variables
authors ="Sergio Stinchi (IBM WebSphere Lab Services)"
scriptName = "RemoveWebModuleToWebServer.py"
version = "1.1.0"

# Global variables
webList=['']
appList=['']


# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

# Command Line
argc = len(sys.argv)
if argc != 1:
   log.ERROR( "Usage: %s <target data file>" % (scriptName))
   clearExit("No target data file found",-1)


# Read target data file 
log.INFO( "Read target data file ..." )
try: execfile(sys.argv[0]) 
except IOError, ioe: 
   log.INFO( "ERROR: " + str(ioe) )
   sys.exit(-1) 
else: log.INFO( "Read target data file done" )
   

#Check Parameter
if len(webList) > 0:
         if isinstance(webList, type([])) == 0:
            log.ERROR("The variable webList must be a list")
            clearExit("The variable webList must be a list",-1)

if len(appList) > 0:
         if isinstance(appList, type([])) == 0:
            log.ERROR("The variable appList must be a list")
            clearExit("The variable appList must be a list",-1)



def getWebList():
    webServerToPrint=""
    try:
        for web in webList:
            webServerToPrint=webServerToPrint+web.split(":")[1] + " "
        log.DEBUG(  webServerToPrint)
    except:
        log.INFO( "KO")
        type, value, traceback = sys.exc_info()
        log.INFO( "ERROR: %s (%s)" % (str(value), type))
        clearExit("Rollback and exit", -1)
    return webServerToPrint

def getIDServer(nodeName,serverName):
    try:
        cell = AdminConfig.list('Cell')
        cellName = AdminConfig.showAttribute(cell, 'name')
        str = "/Cell:%s/Node:%s/Server:%s/" %(cellName,nodeName,serverName)
        id = AdminConfig.getid(str)
        log.DEBUG("XXX - getIDServer = %s" %(id))
    except:
        log.INFO( "KO")
        type, value, traceback = sys.exc_info()
        log.INFO( "ERROR: %s (%s)" % (str(value), type))
        clearExit("Rollback and exit", -1)
    return id


def createCompleteTargetString(webServerList,cellName):
   targetString=""
   try:
       for webserver in webServerList:
           log.INFO("   Check webserver: %s" %webserver)
           if len(targetString.strip())>0:
               conjuntion="+"
           else: 
               conjuntion=""
           targetString= targetString+"%sWebSphere:cell=%s,node=%s,server=%s" %(conjuntion,cellName,webserver.split(":")[0],webserver.split(":")[1])
       log.DEBUG("createCompleteTargetString= %s" %targetString)
   except:
        log.INFO( "KO")
        type, value, traceback = sys.exc_info()
        log.INFO( "ERROR: %s (%s)" % (str(value), type))
        clearExit("Rollback and exit", -1)
   return targetString

 

    
def main():
    webServerToPrint=getWebList()
    printBasicScriptInfo(authors,scriptName,version)   
    apps = AdminApp.list().splitlines()
    # Map the modules for each app
    try:
        for app in appList:
            log.INFO( "###################################################################") 
            log.INFO ("Check Application %s" %app)
            log.INFO( "###################################################################") 
            modules = AdminApp.listModules(app).splitlines()
            for module in modules:
                if module.find('ejb-jar.xml') > 0:
                    log.INFO("   Module %s is an EJB : it Doesnt be to mapped to WebServer %s" %(module,webServerToPrint))
                else:
                    log.DEBUG (">>> %s" %app)
                    log.DEBUG ("module %s" %module)
                    var = "/Deployment:"+app+"/"
                    deployments=AdminConfig.getid(var)
                    deploymentObject = AdminConfig.showAttribute(deployments, 'deployedObject')
                    myModules = AdminConfig.showAttribute(deploymentObject, 'modules')
                    myModules = myModules[1:len(myModules)-1].split(" ")
                    log.DEBUG("1- %s" %myModules)
                    cell=AdminConfig.list("Cell").splitlines()
                    cellName = AdminConfig.showAttribute(cell[0], 'name')
                    for myModule in myModules:
                        log.DEBUG( "module = %s" %myModule)
                        if myModule.find("WebModule")>0:
                            mappings=AdminConfig.showAttribute(myModule,'targetMappings')
                            log.DEBUG(" mappings = %s" %mappings)
                            mappings = mappings[1:len(mappings)-1].split(" ")
                            log.DEBUG ("dopo mappings = %s" %mappings)
                            targetString=""
                            for mapping in mappings:
                                target = AdminConfig.showAttribute(mapping,"target")
                                if target.find('ClusteredTarget') > 0:
                                    clusterName=AdminConfig.showAttribute(target,"name")
                                    if len(targetString.strip())>0:
                                        targetString=targetString+"+"+"WebSphere:cell=%s,cluster=%s" %(cellName,clusterName)
                                    else:
                                        targetString= "WebSphere:cell=%s,cluster=%s" %(cellName,clusterName)
                                    log.DEBUG("    ClusteTargetString = %s" %targetString)
                            prefix = createCompleteTargetString(webList,cellName)
                            completeTargetString="%s+%s" %(prefix, targetString)
                            log.DEBUG("COMPLETE completeTargetString = %s" %completeTargetString)
                            mod = module.split("#")[1].replace('+',',')
                            log.DEBUG ("mod = %s" %mod)
                            opt=['.*',mod, targetString]
                            log.DEBUG("opt = %s" %opt)
                            #INFO("   Mapping modules %s to Webserver %s" %(mod.split(",")[0],webServerToPrint))
                            log.DEBUG( "AdminApp.edit("+str(app)+", ['-MapModulesToServers', ["+str(opt)+"]])")
                            AdminApp.edit(app, ['-MapModulesToServers', [opt]])
            log.INFO( "###################################################################") 
            log.INFO ("End Check Application %s" %app)
            log.INFO( "###################################################################")  
            log.LINEBREAK()       
    except:
        log.INFO( "KO")
        type, value, traceback = sys.exc_info()
        log.INFO( "ERROR: %s (%s)" % (str(value), type))
        clearExit("Rollback and exit", -1)
    
    syncEnvDelayed(AdminConfig.hasChanges(),5)  

#launch script
main()
log.INFO("End %s v%s" %(scriptName,version))