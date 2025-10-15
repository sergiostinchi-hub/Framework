#! /usr/bin/python
# Authors: Sergio Stinchi
# Version        Description
# 1.0.0          Starting version
# Imports
import sys
import re
import string
import glob
from string import replace
from java.util import Date

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))

# Info Variables
authors ="Sergio Stinchi (IBM WebSphere Lab Services)"
scriptName = "readVirtualHosts.py"
version = "1.0.0"
printBasicScriptInfo(authors,scriptName,version)

# # Command Line
argc = len(sys.argv)
if argc != 1:
    print "Usage: <outputPath>  "
    sys.exit(-1)

print "Read target data file ..."
outputPath = sys.argv[0]
# 
print "outputPath = %s" %(outputPath)

# check parameter
# print "Check Parameter .... "


   
def listVirtualHosts():
   cell=AdminConfig.list("Cell").splitlines()[0]    
   VHostList = AdminConfig.list('VirtualHost', cell) 
   line=''
   for vhost in VHostList.splitlines():
      partName = AdminConfig.showAttribute(vhost, 'name')
      if not os.path.exists(outputPath): clearExit("Output Path Not Found - Rollback and exit",-1)
      fileName = "%s.VHOST.py" % (replace(partName, " ", "_"))
      log.INFO(" Create File %s for Virtual Hosts %s " % (fileName, partName))
      fp = fileName
      displayList = []
      f = open(str(outputPath) + "/"+ str(fileName), "w")
      hostAliases = AdminConfig.list('HostAlias',vhost)
      lName="name=%s" %partName
      displayList.append('%s' %(lName))
      listVhosts=""
      for hostAlias in hostAliases.splitlines():
          host=AdminConfig.showAttribute(hostAlias,'hostname')
          port=AdminConfig.showAttribute(hostAlias,'port')
          log.INFO("   Vhost:%s  Host:%s Port:%s " %(partName,host,port))
          listVhosts = str(listVhosts) + "[%s,%s]," %(host,port)
      listVhosts = listVhosts[0:-1]
      displayList.append('vHosts=[%s]' %listVhosts)
      void = display(displayList, f)
      f.close()

listVirtualHosts()
print "%s V%s done" % (scriptName, version)
