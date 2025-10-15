# Author: Stinchi Sergio

# Version        Description
# 1.0.0          Starting version

# Import
import sys
import java

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))

# Global variables
authors="Sergio Stinchi WebSphere Lab Services"
scriptName = "checkWebServerType.py"
version = "1.1.0"
#printBasicScriptInfo(authors,scriptName,version)

servers = AdminConfig.list('Server').splitlines()
for server in servers:
    if not checkIfIsServerTemplate(server):
        nodeName= getNodeNameForServer(server)
        serverName = AdminConfig.showAttribute(server,'name')
        log.DEBUG("checkIfIsServerTemplate nodeName= %s " %nodeName)
        log.DEBUG("checkIfIsServerTemplate serverName= %s " %serverName)
        type=getTypeOfServer(nodeName,serverName)
        log.DEBUG("Server %s is " %serverName,1)
        if type=='WEB_SERVER':
            res=isIntelligentManagementEnabled(nodeName,serverName)
            if res==1:
                print "Server %s:%s: ODR_ENABLED " %(nodeName,serverName)
                log.DEBUG("Server %s:%s: ODR_ENABLED " %(nodeName,serverName))
            else:
                print "Server %s:%s: ODR_DISABLED " %(nodeName,serverName)
                log.DEBUG("Server %s:%s: ODR_DISABLED " %(nodeName,serverName))
        else:
            log.DEBUG(" NOT WEB_SERVER", 2)
    else:
        log.DEBUG("Server %s is Server Template" %(server))
    




