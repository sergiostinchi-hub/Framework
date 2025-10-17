# Authors: Sergio Stinchi,Luciani Gianluca
#migrate from new gitrepos
# 1.0.0          Starting version

import sys
import java

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print ("%s done") % scriptName
   sys.exit(status)
   return
# Start

# Variables
scriptName = "setupVerifyHostNameProps.py"
version = "1.0.0"
print ("%s V%s") % (scriptName, version)


print ("Setup Custom Property com.ibm.ssl.verifyHostname = false")

sec = AdminConfig.getid('/Security:/')
prop = AdminConfig.getid('/Cell:/Security:/Property:com.ibm.ssl.verifyHostname/')
try:
   if prop:
      AdminConfig.modify(prop, [['value', 'false']])
   else:
      AdminConfig.create('Property', sec, [['name','com.ibm.ssl.verifyHostname'], ['value','false']])
except:
      type, value, traceback = sys.exc_info()
      print "KO (ERROR: %s (%s))" % (str(value), type)
      clearExit("Rollback and exit", -1)

AdminConfig.save()
