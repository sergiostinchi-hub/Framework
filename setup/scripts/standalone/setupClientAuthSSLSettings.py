# Authors: Sergio Stinchi (IBM WebSphere Lab Services)

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
scriptName = "setupXDDefaultSSLSettings.py"
version = "1.1.0"


printBasicScriptInfo(authors,scriptName,version)

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   sys.exit(status)
   return

#sslConfigAlias=["XDADefaultSSLSettings","NodeDefaultSSLSettings"]
sslConfigAlias=["XDADefaultSSLSettings"]
clientAuth= 'false'

sslConfigs = [x for x in AdminConfig.list('SSLConfig').split(lineSeparator) if AdminConfig.showAttribute(x, 'alias') in sslConfigAlias]
if len(sslConfigs)==0:
   clearExit("ERRORE: Non Esiste Alcuna SSLConfiguration con il seguente nome %s" % sslConfigAlias,-1)

   
for sslConfig in sslConfigs:
    settings= AdminConfig.showAttribute(sslConfig,'setting')
    log.INFO("Disable Client Authentication Policy  for SSLSetting   %s " %(AdminConfig.showAttribute(sslConfig,'alias')))
    clientAuthentication = AdminConfig.showAttribute(settings,'clientAuthentication')
    AdminConfig.modify(settings, [['clientAuthentication', clientAuth],['clientAuthenticationSupported',clientAuth]])

syncEnv(AdminConfig.hasChanges())

log.INFO("End %s " %scriptName)
