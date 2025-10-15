# Authors: Sergio Stinchi, Lorenzo Monaco
#migrate from new gitrepos     
# 1.0.0          Starting version
# 2.0.0          Other version

import sys
import java
from string import replace

# Variables
scriptName = "AddCustomPropertiesAS.py"
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

# Convert a list of items separated by linefeeds into an array
def getListArray(l):
    return l.splitlines()

# Data
#scopeName="EjbDestCluster"
#properties=[ ['pippoAttr_50', 'Value'] ,['pippoAttr_60', 'Value'],['pippoAttr_70', 'Value']]  

scopeName= sys.argv[0]
attrs= [sys.argv[1],sys.argv[2]]
properties=[ attrs ]

print "Create Property %s with value %s for cluster %s" %(sys.argv[1],sys.argv[2],sys.argv[0])

# Command Line
argc = len(sys.argv)
if argc != 3:
   print "Usage: %s <ClusterName> <JVMpropertyName> <JVMpropertyValue" % (scriptName)
   sys.exit(-1)

# Read target data file
#print "Read target data file ..."
#try: execfile(sys.argv[0])
#except IOError, ioe:
#   print "ERROR: " + str(ioe)
#   sys.exit(-1)
#else: print "Read target data file done"

# Check data read
print "Check data read ..."


def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

def checkScopeName(scopeName):
    print "Check scopeName ... for %s" % (scopeName)  
    scope = None 
    scopeid = None 
    nodeName = None 
    serverName = None 
    clusterName = None
    cell = AdminConfig.list('Cell') 
    nodes = AdminConfig.list('Node') 
    clusters = AdminConfig.list('ServerCluster') 
    servers = AdminConfig.list('Server') 
    if cell.find(scopeName + '(') != -1: 
       scope = 'Cell' 
       scopeid = cell 
       #print "Scope: %s - id: %s" % (scope, scopeid) 
    elif nodes.find(scopeName + '(') != -1: 
       scope = 'Node' 
       beg = nodes.find(scopeName + '(') 
       end = nodes.find(')', beg) + 1 
       scopeid = nodes[beg:end]
       nodeName = scopeName
       #print "Scope: %s - id: %s" % (scope, scopeid) 
    elif clusters.find(scopeName + '(') != -1: 
       scope = 'ServerCluster' 
       beg = clusters.find(scopeName + '(') 
       end = clusters.find(')', beg) + 1 
       scopeid = clusters[beg:end] 
       clusterName = scopeName
       #print "Scope: %s - id: %s" % (scope, scopeid) 
    elif servers.find(scopeName + '(') != -1: 
       scope = 'Server' 
       beg = servers.find(scopeName + '(') 
       end = servers.find(')', beg) + 1 
       scopeid = servers[beg:end] 
       #print "ScopeName %s  - Scope: %s - id: %s" % (scopeName, scope, scopeid) 
    elif scopeName.find(':') != -1: 
       scope = 'Server' 
       colon = scopeName.find(':') 
       nodeName = scopeName[:colon] 
       serverName = scopeName[colon + 1:] 
       scopeid = AdminConfig.getid('/Node:' + nodeName + '/Server:' + serverName + '/')
       if len(scopeid) == 0: 
          print "ERROR: %s not found" % (scopeName) 
          print "%s done" % (scriptUtilityName) 
          sys.exit(-1) 
       # print "Scope: %s - id: %s" % (scope, scopeid) 
    else: 
       print "ERROR: %s not found" % (scopeName) 
       print "%s done" % (scriptUtilityName) 
       sys.exit(-1) 
    return scope , scopeid, scopeName, nodeName, serverName, clusterName


(scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
if scope=="ServerCluster":
   serverids= AdminConfig.list('ClusterMember', scopeid).splitlines()
   for serverid in serverids:
       server = AdminConfig.showAttribute(serverid, 'memberName')
       (scope, scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(server)
       jvm = AdminConfig.list('JavaVirtualMachine', scopeid)
       if len(jvm) == 0: continue 
       for property in properties:
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

