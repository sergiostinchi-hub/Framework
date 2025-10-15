# Author: Andrea Minuto (WebSphere Lab Services)

# Version        Description
# 1.0.1          Added hpel variable
# 1.0.0          Starting version

# Import
import sys

# Variables
scriptName = "setDmgrJvmConfig.py"
version = "1.0.0"

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

# Start
print "%s V%s" % (scriptName, version)

# Data
user = 'root'
group = 'root'
initialHeap = 512 # MB
maximumHeap = 1024 # MB
properties = [ ['com.ibm.cacheLocalHost', 'true'], ['java.net.preferIPv4Stack', 'true'] ]
hpel = 0

# Set DMGR user and group
print "Set Execution User and Group:",
try:
   dmgr = AdminConfig.getid('/Server:dmgr/')
   processDef = AdminConfig.showAttribute(dmgr, 'processDefinitions')[1:-1]
   execution = AdminConfig.showAttribute(processDef, 'execution')
   execprop = "[ ['runAsUser' [" + user + "] ] ['runAsGroup' [" + group + "] ] ]"
   AdminConfig.modify(execution, execprop)
   print "OK"
except:
   print "KO"
   type, value, traceback = sys.exc_info()
   print "ERROR: %s (%s)" % (str(value), type)
   clearExit("Rollback and exit", -1)

# Set DMGR JVM Heap Size
command = '[-serverName dmgr -initialHeapSize ' + str(initialHeap) + ' -maximumHeapSize ' + str(maximumHeap) + ']'
print "Set JVM Heap Size:",
try:
   AdminTask.setJVMProperties(command)
   print "OK"
except:
   print "KO"
   type, value, traceback = sys.exc_info()
   print "ERROR: %s (%s)" % (str(value), type)
   clearExit("Rollback and exit", -1)

# Property settings
print "Property settings ..."
jvm = AdminConfig.list('JavaVirtualMachine', dmgr)
for property in properties:
   print '   name = %s, value = %s:' % (property[0], property[1]) , 
   name = property[0]
   value = property[1]
   jvmprop = [ ["name", name], ["value", "" + value], ["required", "false"] ]
   sysprops = ["systemProperties", [jvmprop]]      
   found = 0
   curr = AdminConfig.showAttribute(jvm, "systemProperties")
   if len(curr) > 0: propslist = curr[1:-1].split()
   else: propslist = []
   for prop in propslist:
      if name == AdminConfig.showAttribute(prop, 'name'):
         if value == AdminConfig.showAttribute(prop, 'value'):
            print "OK (property already set)"
            found = 1
            break
         else:
            try: 
               AdminConfig.modify(prop, jvmprop)
               print "OK (property updated)"
            except:                  
               type, value, traceback = sys.exc_info()
               print "KO (ERROR: %s (%s))" % (str(value), type)
               clearExit("Rollback and exit", -1)
            found = 1
            break                  
   if found == 0:
      try: 
         AdminConfig.modify(jvm, [sysprops])
         print "OK (property added)"
      except:                  
         type, value, traceback = sys.exc_info()
         print "KO (ERROR: %s (%s))" % (str(value), type)
         clearExit("Rollback and exit", -1)
print "Property settings done"

# Switch to HPEL Logging
if hpel == 1:
   print "Switch to HPEL Logging:",
   try:
      hpelService = AdminConfig.list('HighPerformanceExtensibleLogging', dmgr)
      AdminConfig.modify(hpelService, "[[enable true]]")
      hpelTextLog = AdminConfig.showAttribute(hpelService, 'hpelTextLog')
      AdminConfig.modify(hpelTextLog, "[[enabled false]]")
      rasLogging = AdminConfig.list('RASLoggingService', dmgr)
      AdminConfig.modify(rasLogging, "[[enable false]]")
      print "OK"
   except:
      print "KO"
      type, value, traceback = sys.exc_info()
      print "ERROR: %s (%s)" % (str(value), type)
      clearExit("Rollback and exit", -1)

# Save
if AdminConfig.hasChanges() == 1:
   print "Save ..."
   AdminConfig.save()
   print "Save done"

# Done
print "%s done" % scriptName
