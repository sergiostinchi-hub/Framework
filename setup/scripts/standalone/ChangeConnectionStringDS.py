# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version

import  sys 
import os
import glob
from string import replace
import time

scriptName = "ChangeDSConnectionString.py"
scriptVersion = "1.0"
authors = "Sergio Stinchi - Lab Services"

#EXAMPLE COMAND wsadmin.sh -lang jython -username <user> -password <password> -f changeDSConnectionString.py <cluster> <hostName> <portNumber>

def checkIfIsStarted(clusterName):
   started = notstarted = 0
   clusterid = AdminConfig.getid('/ServerCluster:%s/' % clusterName)
   if len(clusterid) > 0:
      members = [[AdminConfig.showAttribute(x, 'memberName'), AdminConfig.showAttribute(x, 'nodeName')] for x in AdminConfig.showAttribute(clusterid, 'members')[1:-1].split()]
      for member in members:
         server = AdminControl.queryNames('WebSphere:*,type=Server,name=%s,node=%s' % (member[0], member[1]))
         if len(server) > 0: started = started + 1
         else: notstarted = notstarted + 1
   print "Starting in progress ... "
   #print "Started: %d, Not Started: %d" % (started, notstarted)
   time.sleep(5)
   if notstarted > 0: checkIfIsStarted(clusterName)
   else: 
        print " "
        print "The Cluster %s is started" %clusterName
        print " "

def checkIfStopped(clusterName):
   started = notstarted = 0
   clusterid = AdminConfig.getid('/ServerCluster:%s/' % clusterName)
   if len(clusterid) > 0:
      members = [[AdminConfig.showAttribute(x, 'memberName'), AdminConfig.showAttribute(x, 'nodeName')] for x in AdminConfig.showAttribute(clusterid, 'members')[1:-1].split()]
      for member in members:
         server = AdminControl.queryNames('WebSphere:*,type=Server,name=%s,node=%s' % (member[0], member[1]))
         if len(server) > 0: started = started + 1
         else: notstarted = notstarted + 1
   print "Stopping in progress ... "
   #print "Started: %d, Not Started: %d" % (started, notstarted)
   time.sleep(5)
   if started > 0: checkIfStopped(clusterName)
   else: 
        print " "
        print "The cluster %s is stopped " %clusterName
        print " "

def reset(text, arg):
   if len(text) > 0: print text
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   print "Execute on file %s done" % arg
   return -1

def printBasicScriptInfo(authors,scriptName,scriptVersion):
    print "--------------------------------------- "
    print " Author:  %s" %(authors)
    print " Script:  %s" %(scriptName)
    print " Version: %s" %(scriptVersion)
    print "--------------------------------------- "


def syncEnv(hasChanges):
   if hasChanges == 1: 
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
            print "Synchronization for node \"" + node[beg:end] + ":", 
            try: AdminControl.invoke(node, 'sync') 
            except: print "KO" 
            else: print "OK"
         print "Synchronization done"   
         print " " 
      else:
        print "No Nodeagent found "
        print " " 
   else: 
      print "No changes made syncronization skipped"
      print " " 
# end def
def stopSingleCluster( clusterName ):
        try:
                #--------------------------------------------------------------------
                # Set up globals
                #--------------------------------------------------------------------
               
                #--------------------------------------------------------------------
                # Stop a cluster
                #--------------------------------------------------------------------
                print "---------------------------------------------------------------"
                print " ClusterManagement:         Stop a cluster"
                print " Cluster name:              "+clusterName
                print "---------------------------------------------------------------"
                print " "
                # check  the required arguments
                if (clusterName == ""):
                   print "WASL6041E: The following argument value is not valid [ClusterName,'%s']" %clusterName
                else:
                   cluster = AdminConfig.getid("/ServerCluster:" +clusterName+"/")
                   if (len(cluster) == 0):
                     print "WASL6041E: The following argument value is not valid [ClusterName,'%s']" %clusterName
                   #endIf
                #endIf
                
                cell = AdminConfig.list("Cell")
                cellName = AdminConfig.showAttribute(cell, "name")
                
                # Obtain the list of cluster MBeans
                cluster = AdminControl.completeObjectName("cell="+cellName+",type=Cluster,name="+clusterName+",*")
                
                # Stop the running cluster 
                if (AdminControl.getAttribute(cluster, "state") != "websphere.cluster.running"):
                   print "WASL6044E: The Cluster %s is  is not running" %clusterName
                   return 0
                else:
                   print "####################### Begin Stop cluster: %s #######################  " %(clusterName)
                   AdminControl.invoke(cluster, "stop")
                #endIf
        except:
                type, value, traceback = sys.exc_info()
                print "%s (%s)" % (str(value), type)
                #endIf
                
        #endTry
        #print "Stop Cluster %s" %clusterName
        return 0  # succeed
#endDef

def startSingleCluster(clusterName ):
        try:
                #--------------------------------------------------------------------
                # Set up globals
                #--------------------------------------------------------------------
               
                #--------------------------------------------------------------------
                # Start a cluster
                #--------------------------------------------------------------------
                print "---------------------------------------------------------------"
                print " ClusterManagement:         Start a cluster"
                print " Cluster name:              "+clusterName
                print "---------------------------------------------------------------"
                print " "
                if (clusterName == ""):
                    print "WASL6041E: The following argument value is not valid [ClusterName,'%s']" %clusterName
                else:
                   cluster = AdminConfig.getid("/ServerCluster:" +clusterName+"/")
                   if (len(cluster) == 0):
                      print "WASL6041E: The following argument value is not valid [ClusterName,'%s']" %clusterName
                cell = AdminConfig.list("Cell")
                cellName = AdminConfig.showAttribute(cell, "name")
                clusterMgr = AdminControl.queryNames("cell="+cellName+",type=ClusterMgr,*")
                AdminControl.invoke(clusterMgr, "retrieveClusters")
                cluster = AdminControl.completeObjectName("cell="+cellName+",type=Cluster,name="+clusterName+",*")
                if (AdminControl.getAttribute(cluster, "state") != "websphere.cluster.stopped"):
                   print "WASL6043E: The Cluster %s is  is already running" %clusterName
                   return 0
                else:
                   print "####################### Begin Start cluster: %s #######################  " %(clusterName)
                   AdminControl.invoke(cluster, "start")
                #endIf   
        except:
                type, value, traceback = sys.exc_info()
                print "%s (%s)" % (str(value), type)
                #endIf
                
        #endTry
        #print "Start Cluster %s completed" %clusterName
        return 1  # succeed
#endDef



def modifyResourceProperty(Object,propertyName,oType,oDescription,oValue,oRequired):
    try:
       AdminConfig.modify(Object, '[[name "%s"] [type "%s"] [description "%s"] [value "%s"] [required "%s"]]' %(propertyName,oType,oDescription,oValue,oRequired)) 
       print " OK"
    except:
         print " KO"
         type, value, traceback = sys.exc_info()
         print "%s (%s)" % (str(value), type)
         reset("Rollback and exit", arg)
    
    
                   
printBasicScriptInfo(authors,scriptName,scriptVersion)     

print "--------------------------------------- "
print "Setup Disaster Recovery Enviroments  "
print "--------------------------------------- "

argc = len(sys.argv)
if argc < 3: 
   print " ERROR: Number Of Parameter aren't correct! "
   print " Usage <ClusterName> <ServerName> <PortNumber>"
   os._exit()


cell=AdminConfig.list("Cell").splitlines()[0]
cellName=AdminConfig.showAttribute(cell, "name")
ClusterNameValue=sys.argv[0]
disasterRecServerNameValue=sys.argv[1]
disasterRecPortNumberValue=sys.argv[2]

#ClusterNameValue="first_cluster"
#disasterRecServerNameValue="LOCALHOST_1"
#disasterRecPortNumberValue="11111"
     
stopSingleCluster(ClusterNameValue)
checkIfStopped(ClusterNameValue)

print " "
print "############## Change DataSource Properties ##############"
print " "
id='/Cell:%s/ServerCluster:%s/'%(cellName,ClusterNameValue)
datasources = AdminConfig.list('DataSource', AdminConfig.getid(id)).splitlines()
for datasource in datasources:
        dsName = AdminConfig.showAttribute(datasource,'name')
        print "Change Datasource %s attributes:  " %dsName
        propertySet = AdminConfig.showAttribute(datasource,'propertySet')
        propertyList = AdminConfig.list('J2EEResourceProperty', propertySet).splitlines()
        for property in propertyList:
                propName = AdminConfig.showAttribute(property, 'name')
                if propName=="portNumber":
                   propValue = AdminConfig.showAttribute(property, 'value')
                   print "   modify %s from %s to %s: " %(propName,propValue,disasterRecPortNumberValue),
                   modifyResourceProperty(property,propName,"java.lang.Integer","Disaster Recovery SQL Server Port",disasterRecPortNumberValue,"false")
                if propName=="serverName":
                   propValue = AdminConfig.showAttribute(property, 'value')
                   print "   modify %s from %s to %s: " %(propName,propValue,disasterRecServerNameValue),
                   modifyResourceProperty(property,propName,"java.lang.Integer","Disaster Recovery SQL Server Server Name",disasterRecServerNameValue,"false")
print " "
print "############## ############################ ##############"
print " "

syncEnv(AdminConfig.hasChanges())
startSingleCluster(ClusterNameValue)
checkIfIsStarted(ClusterNameValue)

print "%s Version: %s finished" %(scriptName,scriptVersion)
    
