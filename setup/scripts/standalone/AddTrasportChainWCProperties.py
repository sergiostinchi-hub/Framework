# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version
 
import sys 
import java 
import time
from java.lang import String as jString
from time import gmtime, strftime

#commonPath = info.getCommonPath()
#resourcesPath = info.getResourcesPath()
#execfile("%s/%s" % (commonPath, "Utility.py"))
  
# Variables 
scriptName = "AddTrasportChainWCProperty.py" 
version = "1.0" 


def getTime():
     tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
     prefix="[%s] I" %tm
     return prefix

def printBasicScriptInfo(authors,scriptName,scriptVersion):
    print  "--------------------------------------- "
    print  " Author:  %s" %(authors)
    print  " Script:  %s" %(scriptName)
    print  " Version: %s" %(scriptVersion)
    print  "--------------------------------------- "


def clearExit(text, status):
   if len(text): print  "%s %s" %(getTime(),text)
   AdminConfig.reset()
   print  "%s %s done" %(getTime(),scriptName)
   sys.exit(status)
   return

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
      print "%s Save ..." %(getTime())
      AdminConfig.save() 
      print "%s Save done " %getTime()
      print "%s Synchronization ..." %getTime()
      nodes = AdminControl.queryNames('type=NodeSync,*') 
      if len(nodes) > 0: 
         nodelist = nodes.splitlines()       
         for node in nodelist: 
            beg = node.find('node=') + 5 
            end = node.find(',', beg) 
            print getTime() + " Synchronization for node \"" + node[beg:end] + "\" :",
            try: AdminControl.invoke(node, 'sync') 
            except: print "KO"
            else: print"OK"
         print "%s Synchronization done" %getTime() 
      else:
         print "%s No Nodeagent found " %getTime()
   else: 
      print "%s No changes made syncronization skipped" %getTime()
# end def


def main():
    name="trustedSensitiveHeaderOrigin"
    value="*"
    try:
        servers = AdminConfig.list('Server').splitlines()
        for server in servers:
           pServerType = AdminConfig.showAttribute(server,'serverType')
           pServerName = AdminConfig.showAttribute(server,'name')
           print "DEBUG Server %s is type of %s" %(pServerName,pServerType)
           print "%s Adding/modifying property %s to Transport Chain for Server %s " %(getTime(),name,pServerName)
           if pServerType != 'DEPLOYMENT_MANAGER' and pServerType != 'NODE_AGENT' and pServerType != 'WEB_SERVER':
               #print "DEBUG serverType %s of %s " %(pServerType,pServerName)
               #print "DEBUG Server : %s" %server
               tcs = AdminConfig.list('TransportChannelService', server)
               tcs = _splitlines(AdminConfig.list('TransportChannelService', server))[0]
               channel_list = (AdminConfig.list('HTTPInboundChannel', tcs)).splitlines()
               for channel in channel_list: 
                  #print "stampa debug channel %s " %channel
                  #ret = channel.find('dynamicclusters') 
                  #if ret != 0:
                  #print channel
                  channelName = AdminConfig.showAttribute(channel,"name")
                  if channelName == "HTTP_2" or  channelName == "HTTP_4":
                    print "%s Channel Name found %s" %(getTime(),channelName)
                    properties = _splitlines(AdminConfig.list('Property', channel))
                    if len(properties)>0:
                        for p in properties:
                            pname = AdminConfig.showAttribute(p, "name")
                            #print "pname = %s" %pname
                            if pname == name:
                                try:
                                   print  "%s Property Already exists, just change value with %s" %(getTime(),value),
                                   AdminConfig.modify(p, [['value', value]])
                                   print " OK "
                                   break
                                except:
                                    print  " KO "
                                    type, value, traceback = sys.exc_info()
                                    clearExit("ERROR: %s (%s)" % (str(value), type),-1)
                            else:
                                try:
                                   print "%s Adding a new  property %s" %(getTime(),name),  
                                   p = AdminConfig.create('Property', channel, [['name', name],['value', value]])
                                   print " OK "
                                except:
                                    print  " KO"
                                    type, value, traceback = sys.exc_info()
                                    clearExit("ERROR: %s (%s)" % (str(value), type),-1)
                    else:
                        try:
                            print "%s create property %s from scratch" %(getTime(),name),   
                            p = AdminConfig.create('Property', channel, [['name', name],['value', value]])
                            print " OK "
                        except:
                            print  " KO "
                            type, value, traceback = sys.exc_info()
                            clearExit("ERROR: %s (%s)" % (str(value), type),-1)
           #end if
    except:
        type, value, traceback = sys.exc_info()
        clearExit("ERROR: %s (%s)" % (str(value), type),-1)
#end def


printBasicScriptInfo("Sergio Stinchi",scriptName,version)
print " "
print "############## ####################"
print "Setup Trasport Chain Custom property"
print "trustedSensitiveHeaderOrigin = *"
print "used from WAS traditional 8.5.5.16  "
print "############## ####################"
print " "
main()
syncEnv(AdminConfig.hasChanges())
