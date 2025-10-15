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
scriptName = "createVirtualHosts.py"
version = "1.0.0"
printBasicScriptInfo(authors,scriptName,version)


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
   print "Usage: %s <target data file>" % (scriptName)
   sys.exit(-1)
        
# Start
print "%s V%s" % (scriptName, version)

# Data
#Vhost:default_host;Host:*;Port:9046

# Read target data file
print "Read target data file ..."
try: execfile(sys.argv[0])
except IOError, ioe:
   print "ERROR: " + str(ioe)
   sys.exit(-1)
else: print "Read target data file done"

# Check data read
print "Check data read ..."
file_name=sys.argv[0]

# if deleteIfExist not in [0, 1]:
#    print "ERROR: The variable deleteIfExist can be 0 or 1"
#    print "%s done" % (scriptName)
#    sys.exit(-1)
   
print "Check data read done"

# Create Virtual Hosts

print "Create Virtual Hosts ... %s" % (name)
VhostFile = open(file_name,'r')
for line in VhostFile:
    print line



# cell=AdminConfig.list("Cell").splitlines()[0]  
# VHostList = AdminConfig.list('VirtualHost', cell) 
# line=''
# for vhost in VHostList.splitlines():
#     VHostName = AdminConfig.showAttribute(vhost, 'name')
#     (resourceId , resourceName) = checkIfResourceExist(cell, VHostName, "VirtualHost")
#     if resourceId != None: 
#         print "Virtual Hosts %s already exists " % (name) 
#         if deleteIfExist == 1:
#             print "Delete existing URL:",
#             try: 
#               AdminConfig.remove(resourceId)
#               print "OK"
#             except: clearExit("KO\nRollback and exit", -1) 
#         else: clearExit("", 0)   
#     print "Create %s:" % (name)
# try:
#    print "Create VirtualHosts %s " % (name),
# 
#    AdminConfig.create('VirtualHost', cell, '[[name "%s"]]' %()) 
#    
#    
#    
#    UrlProviderList = AdminConfig.list('URLProvider',scopeid)
#    providerID=UrlProviderList.splitlines()[0]
#    providerName=AdminConfig.showAttribute(providerID,'name')
#    urlAttrs = [name, jndiName, spec]
#    ulrId = AdminConfig.create('URL', providerID, urlAttrs)         
#    print "URL %s created" % (AdminConfig.showAttribute(ulrId,'name'))
#    print "OK"
# except:
#    print "KO"
#    type, value, traceback = sys.exc_info()
#    print "ERROR: %s (%s)" % (str(value), type)
#    clearExit("Rollback and exit", -1)
# print "Save ..."
# 
# syncEnv(AdminConfig.hasChanges())
# # Done
# print "%s V%s done" % (scriptName, version)
