# Authors: Sergio Stinchi, Lorenzo Monaco

# 1.1.0          Add System Logging
# 1.0.0          Starting version

import sys
import java
from string import replace

# Variables
scriptName = "AddCustomPropertiesAS.py"
version = "1.1.0"

commonPath = info.getCommonPath()
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return
# Start
print "%s V%s" % (scriptName, version)

# Command Line
argc = len(sys.argv)
if argc != 1:
   log.INFO( "Usage: %s <target data file>" % (scriptName))
   sys.exit(-1)

# Read target data file
log.INFO( "Read target data file ...")
try: execfile(sys.argv[0])
except IOError, ioe:
   log.ERROR( "ERROR: " + str(ioe))
   sys.exit(-1)
else: log.INFO( "Read target data file done")

# Check data read
log.INFO( "Check data read ...")


def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   log.INFO( "%s done" % scriptName)
   sys.exit(status)
   return


(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
def applyProperty(scopeid):
       jvm = AdminConfig.list('JavaVirtualMachine', scopeid)
       if len(jvm) == 0: 
           log.INFO("Error no JVM Found for ID %s" %(scopeid))
           return;
       else: 
           for property in properties:
              name = property[0]
              value = property[1]
              required= property[2]
              jvmprop = [ ["name", name], ["value", "" + value], ["required", required ]]
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

if AdminConfig.hasChanges() == 1: 
      print "Save ..." 
      AdminConfig.save() 
      print "Save done" 
      print "Synchronization ..." 
      nodes = AdminControl.queryNames('type=NodeSync,*') 
      if len(nodes) > 0: 
         nodelist = nodes.splitlines()       
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
# end def