# Authors: Andrea Minuto (IBM WebSphere Lab Services)

# Version        Description
# 1.0.1          Added default and maximum expiration days management
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
Authors =" Andrea Minuto (IBM WebSphere Lab Services)"
scriptName = "renewPluginPersonalCertificates.py"
version = "1.0.1"

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   sys.exit(status)
   return

def getIssuerInfo(keyStoreName, keyStoreScope, alias):
   CN = OU = O = C = ''
   certdata = AdminTask.getCertificate(['-keyStoreName', keyStoreName, '-certificateAlias', alias, '-keyStoreScope', keyStoreScope])
   if len(certdata) > 0:
      beg = certdata.find('[issuedTo [')
      if beg != -1:
         beg += len('[issuedTo [')
         end = certdata.find(']', beg)
         first = certdata[beg:end].split(', ')
         for data in first:
            dummy = data.split('=')
            if dummy[0] == 'CN':
               CN = dummy[1]
            elif dummy[0] == 'OU':
               if len(OU) == 0:
                  OU += dummy[1]
               else:
                  OU += ', OU=' + dummy[1]
            elif dummy[0] == 'O':
               if len(O) == 0:
                  O += dummy[1]
               else:
                  O += ', O=' + dummy[1]
            elif dummy[0] == 'C':
               C = dummy[1]
            else: 
               continue
   return CN, O, OU, C

def getExpireDate(edate):
   month = edate[0:3]
   if month == 'Jan': m = 0
   elif month == 'Feb': m = 1
   elif month == 'Mar': m = 2
   elif month == 'Apr': m = 3
   elif month == 'May': m = 4
   elif month == 'Jun': m = 5
   elif month == 'Jul': m = 6
   elif month == 'Aug': m = 7
   elif month == 'Sep': m = 8
   elif month == 'Oct': m = 9
   elif month == 'Nov': m = 10
   elif month == 'Dec': m = 11
   d = int(edate[4:edate.find(',')])
   y = int(edate[-4:]) - 1900
   return (Date(y, m, d, 23, 59, 59).getTime() - Date().getTime()) / 86400000L

def getValidationDays(keyStoreName, keyStoreScope, alias):
   days = 0
   certdata = AdminTask.getCertificateChain(['-keyStoreName', keyStoreName, '-certificateAlias', alias, '-keyStoreScope', keyStoreScope])
   if len(certdata) > 0:
      beg = certdata.rfind('[validity [Valid from')
      if beg != -1: beg = certdata.find('to ', beg)
      if beg != -1:
         end = certdata.find('.', beg)
         days = getExpireDate(certdata[beg + len('to '):end])
   return days

# Start
print "%s V%s" % (scriptName, version)

# Script Variables (fixed)
certificateVersion = '3'
certificateSize = 2048
signatureAlgorithm = 'SHA256withRSA'

# Command Line
arguments = ['basic', 'medium', 'strong', 'strong2', 'strong3']
usage = "Usage: %s <certificate expiration days>|default|maximum\n" % scriptName
if len(sys.argv) != 1: clearExit(usage, -1);
if len(sys.argv) == 1 and sys.argv[0] not in ['default', 'maximum'] and re.match(r"^\d+$", sys.argv[0]) == None: clearExit(usage, -1); 

# Parse the command argument
expiration = sys.argv[0]
if sys.argv[0] not in ['default', 'maximum']: certificateValidDays = int(sys.argv[0])

# Input
print "Certificate expiration days = %s" % expiration

try:
   print "Renew default personal certificate in CMS Key Stores ..."
   sslStores = AdminTask.listKeyStores(['-keyStoreUsage', 'SSLKeys']).split(lineSeparator)
   for sslStore in sslStores:
      sslStoreName = AdminConfig.showAttribute(sslStore, 'name')
      sslStoreScope = AdminConfig.showAttribute(AdminConfig.showAttribute(sslStore, 'managementScope'), 'scopeName')
      if sslStoreName.endswith('CMSKeyStore'):
         print "%s [%s]:" % (sslStoreName, sslStoreScope),
         cn, o, ou, c = getIssuerInfo(sslStoreName, sslStoreScope, 'default')
         if cn == '' or o == '' or ou == '' or c == '': raise Exception("Something goes wrong with the default certificate")
         days = getValidationDays(sslStoreName, sslStoreScope, 'default')
         AdminTask.deleteCertificate(['-keyStoreName', sslStoreName, '-certificateAlias', 'default', '-keyStoreScope', sslStoreScope])
         if expiration == 'default': AdminTask.createChainedCertificate(['-keyStoreName', sslStoreName, '-certificateAlias', 'default', '-keyStoreScope', sslStoreScope, '-rootCertificateAlias', 'root', '-certificateVersion', certificateVersion, '-certificateSize', certificateSize, '-certificateOrganization', o, '-certificateCommonName', cn, '-certificateOrganizationalUnit', ou, '-certificateCountry', c])
         elif expiration == 'maximum': 
             days="7300"
             AdminTask.createChainedCertificate(['-keyStoreName', sslStoreName, '-certificateAlias', 'default', '-keyStoreScope', sslStoreScope, '-rootCertificateAlias', 'root', '-certificateVersion', certificateVersion, '-certificateSize', certificateSize, '-certificateOrganization', o, '-certificateCommonName', cn, '-certificateOrganizationalUnit', ou, '-certificateCountry', c, '-certificateValidDays', days])
         elif certificateValidDays < days: AdminTask.createChainedCertificate(['-keyStoreName', sslStoreName, '-certificateAlias', 'default', '-keyStoreScope', sslStoreScope, '-rootCertificateAlias', 'root', '-certificateVersion', certificateVersion, '-certificateSize', certificateSize, '-certificateOrganization', o, '-certificateCommonName', cn, '-certificateOrganizationalUnit', ou, '-certificateCountry', c, '-certificateValidDays', certificateValidDays])
         else: AdminTask.createChainedCertificate(['-keyStoreName', sslStoreName, '-certificateAlias', 'default', '-keyStoreScope', sslStoreScope, '-rootCertificateAlias', 'root', '-certificateVersion', certificateVersion, '-certificateSize', certificateSize, '-certificateOrganization', o, '-certificateCommonName', cn, '-certificateOrganizationalUnit', ou, '-certificateCountry', c, '-certificateValidDays', days])
         print "OK"
   print "Renew default personal certificate in CMS Key Stores done"
except:
   print "KO"
   type, value, traceback = sys.exc_info()
   print "ERROR: %s (%s)" % (str(value), type)
   clearExit("Rollback and exit", -1)

if AdminConfig.hasChanges() == 1:
   # Save
   print "Save ..."
   AdminConfig.save()
   print "Save done"
   # Synchronization
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
   else:
      print "No running nodeagents found"
   print "Synchronization done"

# Done
print "%s done" % (scriptName)
