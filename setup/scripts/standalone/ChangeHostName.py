#! /usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version


# Import

import java
from string import replace
global f, reportName



# Variables
scriptName = "AddWCProperties.py"
version = "1.0.0"
msgPrefix=''

print "%s V%s" % (scriptName, version)


# Command Line
argc = len(sys.argv)
if argc != 2:
   log.INFO("Usage: <OldHostName>  <NewHostName>")
   sys.exit(-1)

    
newHostName = sys.argv[0]
oldHostName = sys.argv[1]


print("newHostName = %s" % newHostName)

# check parameter
print("Check Parameter .... ")
if (newHostName == None) or (len(newHostName.strip()) == 0):
   print "ERROR: The variable newHostName is mandatory"
   print "%s done" % (scriptName)
   sys.exit(-1)

# Auxiliary functions
def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

def wsadminToList(inStr):
    outList=[]
    if (len(inStr)>0 and inStr[0]=='[' and inStr[-1]==']'):
        inStr = inStr[1:-1]
        tmpList = inStr.split(" ")
    else:
        tmpList = inStr.split("\n") #splits for Windows or Linux
    for item in tmpList:
        item = item.rstrip();       #removes any Windows "\r"
        if (len(item)>0):
           outList.append(item)
    return outList
#endDef

def getNodeNameForServer(ServerID):
   beg = ServerID.find('/nodes/') + len('/nodes/')
   end = ServerID.find('/', beg)
   out = ServerID[beg:end]    
   return  out

def getServerName(ServerID):
   # print "ServerID == %s " % (SeverID)
   beg = ServerID.find('/servers/') + len('/servers/')
   end = ServerID.find('|', beg)
   app = ServerID[beg:end]
   return app

## Example 10 Convert string to list ##
def convertToList( inlist ):
    outlist = []
    if (len(inlist) > 0):
       if (inlist[0] == '[' and inlist[len(inlist) - 1] == ']'):
          # Special checking when the config name contain space 
          if (inlist[1] == "\"" and inlist[len(inlist)-2] == "\""):
             clist = inlist[1:len(inlist) -1].split(")\" ")
          else:
             clist = inlist[1:len(inlist) - 1].split(" ")
          #endIf
       else:
          clist = inlist.split(java.lang.System.getProperty("line.separator"))
       #endIf
        
       for elem in clist:
           elem = elem.rstrip();
           if (len(elem) > 0):
              if (elem[0] == "\"" and elem[len(elem) -1] != "\""):
                 elem = elem+")\""
              #endIf   
              outlist.append(elem)
           #endIf
        #endFor
    #endIf    
    return outlist
#endDef


def displayEndPointsFunc(serverEntryId,nodeName):
          print( " serverEntryId = %s " %(serverEntryId))
          partName = serverEntryId.split( '(', 1 )[ 0 ]
          print(  "System information listPorts(): Server Name : " +  partName)
          displayList = []
          NamedEndPoints = AdminConfig.list('NamedEndPoint', serverEntryId).splitlines()
          print( " NamedEndPoints = %s " %(NamedEndPoints))
          ListPorts = ""
          for namedEndPoint in NamedEndPoints:
                endPointName = AdminConfig.showAttribute(namedEndPoint, "endPointName" )
                endPoint = AdminConfig.showAttribute(namedEndPoint, "endPoint" )
                host = AdminConfig.showAttribute(endPoint, "host" )
                port = AdminConfig.showAttribute(endPoint, "port" )
                ListPorts += "['%s','%s','%s']," % (endPointName, host, port)
          ListPorts = ListPorts[0:len(ListPorts)-1]
          displayList.append("endpoints=[%s]" % (ListPorts))
          displayList.append("deleteIfExist=%s" %(deleteIfExist))
          void = display(displayList, f)
 
# end def

































def changeHostNameEndpoints():
    servers = AdminConfig.list('ServerEntry').splitlines()
    if len(servers) > 0:
      for server in servers:
         serverName = getServerName(server)
         nodeName = getNodeNameForServer(server)
         lista = [x for x in  AdminConfig.list('ServerEntry').splitlines() if AdminConfig.showAttribute(x,'serverName') == serverName]
         for seId in lista:
            changeEndPoint(scopeid,scopeName)

def getCellName():
       cell=AdminConfig.list("Cell").splitlines()
       cellName = AdminConfig.showAttribute(cell[0], 'name')
       return cellName
   
def getNodeId( nodename ):
    """Given a node name, get its config ID"""
    return AdminConfig.getid( '/Cell:%s/Node:%s/' % ( getCellName(), nodename ) )
   
def nodeIsIHS( nodename ):
    """Returns true if the node is IHS."""
    # Note: This method queries whether variable WAS_INSTALL_ROOT is defined.
    # This is a weak technique for identifying an IHS node.
    # Hopefully a more robust mechanism can be found in the future.
    return None == getWasInstallRoot(nodename)

def getNodeVariable(nodename, varname):
    """Return the value of a variable for the node -- or None if no such variable or not set"""
    print "getNodeVariable(%s, %s) " %(nodename, varname)
    vmaps = _splitlines(AdminConfig.list('VariableMap', getNodeId(nodename)))
    if 0 < len(vmaps):  # Tolerate nodes with no such maps, for example, IHS nodes.
        map_id = vmaps[-1] # get last one
        entries = AdminConfig.showAttribute(map_id, 'entries')
        # this is a string '[(entry) (entry)]'
        entries = entries[1:-1].split(' ')
        for e in entries:
            name = AdminConfig.showAttribute(e,'symbolicName')
            value = AdminConfig.showAttribute(e,'value')
            if name == varname:
                return value
    return None

def getWasInstallRoot(nodename):
    """Return the absolute path of the given node's WebSphere installation"""
    return getNodeVariable(nodename, "WAS_INSTALL_ROOT")
   
def _splitlines(s):
  rv = [s]
  if '\r' in s:
    rv = s.split('\r\n')
  elif '\n' in s:
    rv = s.split('\n')
  if rv[-1] == '':
    rv = rv[:-1]
  return rv   
   
def syncEnv(hasChanges):
   if hasChanges == 1: 
      print("Save ...") 
      AdminConfig.save() 
      print("Save done") 
      print("Synchronization ...") 
      nodes = AdminControl.queryNames('type=NodeSync,*') 
      if len(nodes) > 0: 
         nodelist = nodes.splitlines()       
         for node in nodelist: 
            beg = node.find('node=') + 5 
            end = node.find(',', beg) 
            print("Synchronization for node \"" + node[beg:end] + "\" :")
            try: AdminControl.invoke(node, 'sync') 
            except: print("KO") 
            else: print("OK")
         print("Synchronization done")    
      else:
         print("No Nodeagent found ") 
   else: 
      print("No changes made syncronization skipped") 
# end def

def restartNodes():
   nodes = AdminConfig.list('Node').splitlines()
   if len(nodes) > 0:
      for node in nodes:
         print "Node To Restart:  %s" %(node) 
         nodeName = AdminConfig.showAttribute(node, 'name')
         nodeagent = AdminControl.queryNames('type=NodeAgent,node=%s,*'%(nodeName))
         print "Invoke Restart on NodeAgent : ", 
         if (len(nodeagent)>0):
             print "No NodeAgent Found"
             if(not nodeIsIHS(nodeName)):
                 restartAllServerOnNode(nodeName)
                 print "proceed to restart nodeAgent: " + nodeagent
                 AdminControl.invoke(nodeagent,'restart','true true')
         else:
             print "No NodeAgent Started found"    
                 
def startAllServers( nodeName):
    msgPrefix = "startAllServers('"+nodeName+"'): "
    try:
        #--------------------------------------------------------------------
        # Start all servers 
        #--------------------------------------------------------------------
        print "---------------------------------------------------------------"
        print " ChangeHostName:   Start all servers"
        print " Node name:               "+nodeName
        print " Usage: ChangeHostName.startAllServers(\""+nodeName+"\") "
        print " Return: None"
        print "---------------------------------------------------------------"
        print " "
        print " "
        if (nodeName == ""):
            clearExit("NodeName cannot be Null" ,-1)
        else:
            node = AdminConfig.getid("/Node:" +nodeName+"/")
            if (len(node) == 0):
                    clearExit("Cannot Fine Node ID" ,-1)
        servers = AdminConfig.getid("/Node:"+nodeName+"/Server:/")
        if (len(servers) == 0):
           clearExit("No servers exist" ,-1)
        else:           
           servers = convertToList(servers)
           for aServer in servers:
              serverName = AdminConfig.showAttribute(aServer,"name")
              nodeagent = AdminControl.queryNames("type=NodeAgent,node="+nodeName+",*")
              if (serverName != "nodeagent"):
                 if (len(nodeagent) == 0):
                    print(" node agent is not started.  Unable to start server")
                 else:
                    runningServer = AdminControl.queryNames("type=Server,node="+nodeName+",name="+serverName+",*")
                    if (len(runningServer) > 0 and AdminControl.getAttribute(runningServer, "state") == "STARTED"):
                       print("Server " + serverName + " started already")
                    else:
                       print("Start server: " + serverName)
                       AdminControl.startServer(serverName, nodeName)
    except:
        print "KO"
        type, value, traceback = sys.exc_info()
        print traceback
        print "ERROR: %s (%s)" % (str(value), type)
        clearExit("Rollback and exit", -1)
    
#endDef

def stopAllServers( nodeName):
    msgPrefix = "stopAllServers('"+nodeName+"'): "
    try:
        #--------------------------------------------------------------------
        # Stop all running servers 
        #--------------------------------------------------------------------
        print "---------------------------------------------------------------"
        print " ChangeHostName:   Stop all servers"
        print " Node name:               "+nodeName
        print " Usage: ChangeHostName.stopAllServers(\""+nodeName+"\") " 
        print " Return: None"
        print "---------------------------------------------------------------"
        print " "
        print " "
        
        # Check the required parameters
        if (nodeName == ""):
           clearExit("NodeName cannot be Null" ,-1)
        else:
            node = AdminConfig.getid("/Node:" +nodeName+"/")
            if (len(node) == 0):
                clearExit("Cannot Fine Node ID" ,-1)
            #endIf
        #endIf

        # Retrieve server configuration objects
        servers = AdminConfig.getid("/Node:"+nodeName+"/Server:/")
        
        if (len(servers) == 0):
           # No servers exist
          clearExit("No servers exist" ,-1)
        else:
           # Identify the running server MBeans
           runningServers = AdminControl.queryNames("type=Server,node="+nodeName+",processType=ManagedProcess,*")
           
           if (len(runningServers) == 0):
              # no any server mbeans are running
              print("no any server mbeans are running")
           else:        
              # Convert Jython string to list
              runningServers = AdminUtilities.convertToList(runningServers)
              # Stop each running server in the server list
              for aRunningServer in runningServers:
                 if (len(aRunningServer) > 0):
                    serverName = AdminControl.getAttribute(aRunningServer, "name")
                    print("Stop server: " + serverName)
                    AdminControl.stopServer(serverName, nodeName)
    except:
        print "KO"
        type, value, traceback = sys.exc_info()
        print traceback
        print "ERROR: %s (%s)" % (str(value), type)
        clearExit("Rollback and exit", -1)

print "OK:" + str(msgPrefix) 
#endDef


def restartAllServerOnNode(nodeName):
  stopAllServers(nodeName)
  startAllServers(nodeName)

def checkIfIsServerTemplate(ScopeId):
     print "ScopeId = %s " %(ScopeId)
     if ScopeId.find('/dynamicclusters/') != -1:
         print("ScopeId %s is ServerTemplate " %(ScopeId)) 
         return 1
     else:
         print "return 0"
         return 0    

def main():
    lstServerIndex = AdminConfig.list('ServerIndex').splitlines()
    for serverIndex in lstServerIndex:
        print "Change HostName for %s " + serverIndex
        if(checkIfIsServerTemplate(serverIndex)==0):
            AdminConfig.modify(serverIndex,  "[[hostName %s]]" %(newHostName))
            syncEnv(AdminConfig.hasChanges())
            restartNodes()
  
displayEndPointsFunc() 

print("%s V%s done" % (scriptName, version))
