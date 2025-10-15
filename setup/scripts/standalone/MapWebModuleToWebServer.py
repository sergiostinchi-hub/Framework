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
scriptName = "MapWebModuleToWebServer.py"
version = "2.0.0"
printBasicScriptInfo(authors,scriptName,version)   
# Global variables

webServersList=['']
webList=['']
appList=['']
webServerListToRemove=['']
log.setClass(scriptName[0:-3])

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
else: 
    log.INFO( "Read target data file done" )
    log.INFO("------ Parameter ----------")
    log.INFO("webServersList = %s" %webServersList)
    log.INFO("appList = %s" %appList)
    log.INFO("webserverSource = %s" %webserverSource)
    log.INFO("webServerTarget = %s" %webServerTarget)
    log.INFO("webServerListToRemove = %s" %webServerListToRemove)
    log.INFO("------ Parameter ----------")

#Check Parameter
if len(webServersList) > 0:
         if isinstance(webServersList, type([])) == 0:
            log.ERROR("The variable webServersList must be a list")
            clearExit("The variable webServersList must be a list",-1)

if len(appList) > 0:
    if  isinstance(appList, type([])) == 0:
            log.ERROR("The variable appList must be a list")
            clearExit("The variable appList must be a list",-1)
    else:
        log.TRACE("appList = %s" % appList)

if len(webServerListToRemove) > 0:
    if  isinstance(webServerListToRemove, type([])) == 0:
            log.ERROR("The variable webServerListToRemove must be a list")
            clearExit("The variable webServerListToRemove must be a list",-1)
    else:
        log.TRACE("webServerListToRemove = %s" % webServerListToRemove)

def printWebServersList():
    webServerToPrint=""
    for web in webServersList:
        webServerToPrint=webServerToPrint+web.split(":")[1] + " "
    return webServerToPrint

def printWebServersListToRemove():
    webServerToPrint=""

    for web in webServerListToRemove:
        webServerToPrint=webServerToPrint + " " + web + " "
    log.INFO(" ##################################################################### ")
    log.INFO(" WebServer to Remove is = %s" %webServerToPrint)
    log.INFO(" ##################################################################### ")

def getIDServer(nodeName,serverName):
    cell = AdminConfig.list('Cell')
    cellName = AdminConfig.showAttribute(cell, 'name')
    str = "/Cell:%s/Node:%s/Server:%s/" %(cellName,nodeName,serverName)
    id = AdminConfig.getid(str)
    log.TRACE("getIDServer = %s" %(id))
    return id

def createCompleteTargetString(webServerList,cellName):
   targetString=""
   for webserver in webServerList:
       log.INFO("   Check webserver: %s" %webserver)
       if len(targetString.strip())>0:
           conjuntion="+"
       else: 
           conjuntion=""
       targetString= targetString+"%sWebSphere:cell=%s,node=%s,server=%s" %(conjuntion,cellName,webserver.split(":")[0],webserver.split(":")[1]);
       
   log.TRACE("createCompleteTargetString= %s" %targetString)
   return targetString

def main(webList,appList):
    printWebServersListToRemove()
    webServerToPrint=printWebServersList()
    apps = AdminApp.list().splitlines()
    # Map the modules for each app
    for dummy in appList:
        log.TRACE("dummy == %s " % dummy)
        if dummy =='ALL':
            log.INFO("ALL Application must be Checked")
            appList = apps
    for app in appList:
        log.INFO( "###################################################################") 
        log.INFO ("Check Application %s" %app)
        log.INFO( "###################################################################") 
        log.TRACE ("app Name is %s" %app)
        var = "/Deployment:"+app+"/"
        deployments=AdminConfig.getid(var)
        deploymentObject = AdminConfig.showAttribute(deployments, 'deployedObject')
        myModules = AdminConfig.showAttribute(deploymentObject, 'modules')
        myModules = myModules[1:len(myModules)-1].split(" ")
        log.TRACE("Lista Moduli  %s" %myModules)
        cell=AdminConfig.list("Cell").splitlines()
        cellName = AdminConfig.showAttribute(cell[0], 'name')
        for myModule in myModules:
            log.TRACE("################################")
            log.TRACE("EAR MODULE %s" %app)
            log.TRACE("<<Modules>> %s" %myModules)
            log.TRACE("SINGLE MODULE %s" %myModule)
            log.TRACE("################################")
            log.TRACE( "Modulo Singolo %s" %myModule)
            if myModule.find("WebModule")>0:
                uri = AdminConfig.showAttribute(myModule,'uri')
                #BexBridge.war,WEB-INF/web.xml'
                infoMod="%s,+WEB-INF/web.xml" %(uri)
                log.INFO("WebModule To Update %s" %infoMod)
                mappings=AdminConfig.showAttribute(myModule,'targetMappings')
                mod = myModule.split("#")[1].replace('+',',')
                printMappingName(mappings,mod)
                webList = createPreviuosWebServerMapping(mappings,webServerListToRemove)
                if needToAddWebServers(mappings,mod):
                    log.INFO("Added a WebServer %s" %webServerTarget)
                    if webServerTarget!='NONE':
                        webList.append(webServerTarget)
                    log.TRACE("webList after Append %s" %webList)
                if len(webServersList)>0:
                    for dummy in webServersList:
                        webList.append(dummy)
                log.TRACE(" Lista Targets = %s" %mappings)
                mappings = mappings[1:len(mappings)-1].split(" ")
                targetString=""
                for mapping in mappings:
                    target = AdminConfig.showAttribute(mapping,"target")
                    log.TRACE("target %s for mapping %s" %(target,mapping))
                    if target.find('ClusteredTarget') > 0:
                        clusterName=AdminConfig.showAttribute(target,"name")
                        if len(targetString.strip())>0:
                            targetString=targetString+"+"+"WebSphere:cell=%s,cluster=%s" %(cellName,clusterName)
                        else:
                            targetString= "WebSphere:cell=%s,cluster=%s" %(cellName,clusterName)
                        log.TRACE("ClusteredTarget Find With value = %s" %targetString)
                    elif target.find('ServerTarget') > 0:
                        serverName=AdminConfig.showAttribute(target,"name")
                        nodeName=AdminConfig.showAttribute(target,"nodeName")
                        if getServerType(nodeName,serverName) == 'APPLICATION_SERVER':
                           if len(targetString.strip())>0:
                              targetString=targetString+"+"+"WebSphere:cell=%s,node=%s,server=%s" %(cellName,nodeName,serverName)
                           else:
                              targetString= "WebSphere:cell=%s,node=%s,server=%s" %(cellName,nodeName,serverName)
                        log.TRACE("ServerTarget Find With value = %s" %targetString)
                prefix = createCompleteTargetString(webList,cellName)
                completeTargetString="%s+%s" %(prefix, targetString)
                log.TRACE("targetString before = %s" %completeTargetString)
                log.TRACE("targetString[:1] = %s" %completeTargetString[:1])
                if completeTargetString[:1] == "+":
                    completeTargetString = completeTargetString[1:]
                    log.TRACE("AA targetString now is = %s" %completeTargetString)
                log.TRACE("Complete completeTargetString = %s" %completeTargetString)
                log.TRACE ("mod = %s" %mod)
                opt=['.*',infoMod, completeTargetString]
                log.TRACE("opt = %s" %opt)
                log.INFO("   Mapping modules %s to Webserver %s" %(infoMod.split(",")[0],webServerToPrint))
                log.TRACE( "AdminApp.edit("+str(app)+", ['-MapModulesToServers', ["+str(opt)+"]])")
                AdminApp.edit(app, ['-MapModulesToServers', [opt]])
        log.INFO( "###################################################################") 
        log.INFO ("End Check Application %s" %app)
        log.INFO( "###################################################################")  
        log.LINEBREAK()        
    
    #syncEnvDelayed(AdminConfig.hasChanges(),5)  
    # Save the changes
def printMappingName(mappings,myModule):
    mappings = mappings[1:len(mappings)-1].split(" ")
    for mapping in mappings:
        target = AdminConfig.showAttribute(mapping,'target')
        log.TRACE(" target= %s" %target)
        nameTarget = AdminConfig.showAttribute(target,'name')
        log.TRACE(" nameTarget= %s" %nameTarget)
        log.TRACE(" target.find('ClusteredTarget') =%s" %target.find('ClusteredTarget'))
        if target.find('ClusteredTarget')==-1:
            nodeNameTarget="%s:" %AdminConfig.showAttribute(target,'nodeName')
            log.TRACE(" nodeNameTarget= %s" %nodeNameTarget)
        else:
            nodeNameTarget=""
            log.TRACE(" target.find('ClusteredTarget') == 0")
        completeNameTarget="%s%s" %(nodeNameTarget,nameTarget)
        log.TRACE(" completeNameTarget= %s" %completeNameTarget)
        log.DEBUG("Name of Target for Application %s is %s" %(myModule,completeNameTarget))

def needToAddWebServers(mappings,myModule):
    output=False;
    mappings = mappings[1:len(mappings)-1].split(" ")
    log.DEBUG(" webserverSource = %s" %webserverSource)
    log.DEBUG(" mappings = %s" %mappings)
    for mapping in mappings:
        target = AdminConfig.showAttribute(mapping,'target')
        log.TRACE(" target= %s" %target)
        nameTarget = AdminConfig.showAttribute(target,'name')
        log.TRACE("target= %s" %target)
        log.TRACE("target.find('ClusteredTarget') =%s" %target.find('ClusteredTarget'))
        if target.find('ClusteredTarget')==-1:
            nodeNameTarget="%s" %AdminConfig.showAttribute(target,'nodeName')
            log.TRACE(" nodeNameTarget= %s" %nodeNameTarget)
        else:
            nodeNameTarget=""
            log.TRACE(" target.find('ClusteredTarget') present")
        completeNameTarget="%s:%s" %(nodeNameTarget,nameTarget)
        if webserverSource==completeNameTarget:
            log.INFO("Found WebServer Match %s" %completeNameTarget)
            output=True
    return output       


def createPreviuosWebServerMapping(mappings,webServerListToRemove):
    log.TRACE(" Start createPreviuosWebServerMapping")
    log.TRACE("mappings : %s" %mappings)
    log.TRACE("webServerListToRemove=%s " %webServerListToRemove)
    webserverLst=[]
    mappings = mappings[1:len(mappings)-1].split(" ")
    webserverLst= createNewWebServerList(mappings,webServerListToRemove)
    log.TRACE(" webserverLst modified  by exclusion= %s" %webserverLst)
    return webserverLst

def webserverMatch(namePreviousMapping ,webServerListToRemove):
        target = AdminConfig.showAttribute(namePreviousMapping,'target')
        nameTarget = AdminConfig.showAttribute(target,'name')
        nodeNameTarget="%s" %AdminConfig.showAttribute(target,'nodeName')
        webServerMapped="%s:%s" %(nodeNameTarget,nameTarget)
        for webToExclude in webServerListToRemove:
           log.TRACE("webToExclude: %s" %webToExclude)
           log.TRACE("webServerMapped= %s" %webServerMapped)
           if webToExclude==webServerMapped:
               log.TRACE("MATCHING FOUND for %s " %webServerMapped)
               log.INFO("Remove WebServer %s from Mapping Module" %webServerMapped)
               return "true" , webToExclude
        return "false", webServerMapped


               
def createNewWebServerList(mappings,webServerListToRemove):
    log.TRACE("BEGIN createNewWebServerList")
    lst=[]
    for mapping in mappings:
        log.TRACE("single map : %s" %mapping)
        target = AdminConfig.showAttribute(mapping,'target')
        #log.TRACE(" target= %s" %target)
        nameTarget = AdminConfig.showAttribute(target,'name')
        if target.find('ClusteredTarget')==-1:
            nodeNameTarget="%s" %AdminConfig.showAttribute(target,'nodeName')
            log.TRACE(" nodeNameTarget= %s" %nodeNameTarget)
            completeNameTarget="%s:%s" %(nodeNameTarget,nameTarget)
            if getServerType(nodeNameTarget,nameTarget) == 'WEB_SERVER':
                (matching, webToExclude) = webserverMatch(mapping,webServerListToRemove)
                if matching=='true':
                    log.TRACE("EXCLUDE THIS TARGET: %s" %webToExclude)
                else:
                    log.TRACE("THIS TARGET %s NEEDS TO STAY IN LIST" %webToExclude)
                    lst.append(webToExclude)
    return lst

main(webServersList,appList)

