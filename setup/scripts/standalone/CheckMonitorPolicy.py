# 20180320 Team Sistemisti Middleware 
# Script per impostare nodeRestartState (STOPPED o RUNNING o PREVIOUS) di tutti gli  Application Servers 
# versione con la possibilita' di escudere alcuni application server dalla modifica
#
# comando esecuzione: 
#      /prod/IBM/WebSphere/AppServer/profiles/Dmgr01/bin/wsadmin.sh -lang jython -f /prod/scripts/chPolicyMonitorAS_richiestaServer.py -user <utenteAmministrativo> -password <password>
#   se necessario specificare due dmgr presenti sullo stesso server: 
#      /prod/IBM/WebSphere/AppServer/profiles/Dmgr01/bin/wsadmin.sh -conntype SOAP -host <nomehost> -port <numero porta dmgr 3389(default) o altra > -lang jython -f /prod/scripts/chPolicyMonitorAS_richiestaServer.py


# Import
import os
import sys
import re
import java
import AdminUtilities
import difflib
import time
from java.lang import System
# Start
scriptName = "CheckMonitorPolicy.py"
version = "1.0(2018-11-10)"
# Start
print "%s V%s" % (scriptName, version)

# clearExit Variable
startt = 0
def clearExit(text, status):
   if len(text): print text
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   print "Elapsed Time: %.3f s" % (time.clock() - startt)
   print "%s done" % scriptName
   sys.exit(status)
   return

def customExit(text, status):
   if len(text): print text
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   print "Elapsed Time: %.3f s" % (time.clock() - startt)
   print "%s done" % scriptName
   sys.exit(0)

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


def doesDynamicClusterExist(clusterName):
   dcid = AdminConfig.getid("/DynamicCluster:" + clusterName)
   if (dcid != None and dcid != ""):
      return "true"
   else:
      return "false"


state = ''
while state != ('RUNNING' or 'STOPPED' or 'PREVIOUS'):
    state = raw_input('specifica lo stato che vuoi impostare? (S|R|P)(STOPPED|RUNNING|PREVIOUS)').upper()
    if state == 'R':
        state = 'RUNNING'
        break
    elif state == 'S':
        state = 'STOPPED'
        break
    elif state == 'P':
        state = 'PREVIOUS'
        break
    else:
        clearExit("La scelta non valida",-1)
try:
    print " "
    print "#######################################################################"
    print "Change Monitor policy Status to %s" %state        
    print "#######################################################################"
    print " "
    dynamiClusters= AdminTask.listDynamicClusters().splitlines()
    cell = AdminConfig.list('Cell')
    cellName = AdminConfig.showAttribute(cell, 'name')
    answer = raw_input('Vuoi modificare il comportamento di restart di tutti i cluster? [Y,N] :')
    if answer.upper() not in ['Y', 'N']:
          print "ERROR: Answer not in scope . Only [Y] or [N]"
    if answer.upper() == 'Y':
        clusters = AdminConfig.list('ServerCluster').splitlines()
        for cluster in clusters:
            clusterName=AdminConfig.showAttribute(cluster, 'name')
            if doesDynamicClusterExist(clusterName)=='true':
                print "ClusterName %s is dinamic" %clusterName
                clusterId = AdminConfig.getid('/Cell:%s/DynamicCluster:%s/'%(cellName,clusterName))  
                monitoringPolicy = AdminConfig.list("MonitoringPolicy", clusterId)
                AdminConfig.modify(monitoringPolicy, '[[nodeRestartState ' + state.upper() + ']]')
                print " "
                print "#######################################################################"
                print "Modified Monitor policy for Dinamic Cluster %s  to %s " %(clusterName,state)
                print "#######################################################################"
                print " "
            else:
                members = AdminConfig.showAttribute(cluster, "members")
                members = AdminUtilities.convertToList(members)
                #print "members = %s" % members
                if len(members) > 0:
                       #print "cluster " + clusterName + " has %s members" % (len(members))
                       for member in members:
                           serverName = AdminConfig.showAttribute(member, "memberName")
                           nodeName= AdminConfig.showAttribute(member, "nodeName")
                           str = "/Cell:%s/Node:%s/Server:%s" % (cellName, nodeName, serverName)
                           id = AdminConfig.getid(str)
                           #print "id member: " + id
                           monitoringPolicy = AdminConfig.list( "MonitoringPolicy", id )
                           #print "monitorPolicy for server %s is %s" % (serverName,monitoringPolicy)
                           AdminConfig.modify( monitoringPolicy, '[[nodeRestartState ' + state.upper() + ']]' )
                           print " "
                           print "#######################################################################"
                           print "Modified Monitor policy for Server %s:%s  to %s " %(nodeName,serverName,state)
                           print "#######################################################################"
                           print " "
                           #print "AdminConfig.hasChanges = %d" % AdminConfig.hasChanges()
    elif answer.upper() == 'N':
        clusters = AdminConfig.list('ServerCluster').splitlines()
        for cluster in clusters:
            clusterName=AdminConfig.showAttribute(cluster, 'name')
            answer = raw_input('Vuoi modificare il comportamento di restart del cluster %s [Y,N] :' %clusterName )
            if answer.upper() not in ['Y', 'N']:
                print "ERROR: Answer not in scope . Only [Y] or [N]"
            if answer.upper()=='Y':
                clusterName=AdminConfig.showAttribute(cluster, 'name')
                if doesDynamicClusterExist(clusterName)=='true':
                    print "clusterName %s is dinamic" %clusterName
                    clusterId = AdminConfig.getid('/Cell:%s/DynamicCluster:%s/'%(cellName,clusterName))  
                    monitoringPolicy = AdminConfig.list("MonitoringPolicy", clusterId)
                    AdminConfig.modify(monitoringPolicy, '[[nodeRestartState ' + state.upper() + ']]')
                    print " "
                    print "#######################################################################"
                    print "Modified Monitor policy for Dinamic Cluster %s  to %s " %(clusterName,state)
                    print "#######################################################################"
                    print " "
                else:
                    members = AdminConfig.showAttribute(cluster, "members")
                    members = AdminUtilities.convertToList(members)
                    #print "members = %s" % members
                    if len(members) > 0:
                           #print "cluster " + clusterName + " has %s members" % (len(members))
                           for member in members:
                               serverName = AdminConfig.showAttribute(member, "memberName")
                               nodeName= AdminConfig.showAttribute(member, "nodeName")
                               str = "/Cell:%s/Node:%s/Server:%s" % (cellName, nodeName, serverName)
                               id = AdminConfig.getid(str)
                               #print "id member: " + id
                               monitoringPolicy = AdminConfig.list( "MonitoringPolicy", id )
                               #print "monitorPolicy for server %s is %s" % (serverName,monitoringPolicy)
                               AdminConfig.modify( monitoringPolicy, '[[nodeRestartState ' + state.upper() + ']]' )
                               print " "
                               print "###############################################################################"
                               print "Modified Monitor policy for Server %s:%s  to %s " %(nodeName,serverName,state)
                               print "###############################################################################"
                               print " "
                               #print "AdminConfig.hasChanges = %d" % AdminConfig.hasChanges()

    else:
        print "No Action are made "
        print "Elapsed Time: %.3f s" % (time.clock() - startt)
        print "%s done" % scriptName
except:
   type, value, traceback = sys.exc_info()
   print "ERROR: %s (%s)" % (str(value), type)
   clearExit("Rollback and exit", -1)
print "Save ..."
if AdminConfig.hasChanges() == 1:
  print "Synchronization ..."
  AdminConfig.save()
  nodes = AdminControl.queryNames('type=NodeSync,*')
  if len(nodes) > 0:
     nodelist = nodes.split(lineSeparator)      
     for node in nodelist:
        beg = node.find('node=') + 5
        end = node.find(',', beg)
        print "Synchronization for node \"" + node[beg:end] + "\" :",
        try: AdminControl.invoke(node, 'sync')
        except: print "KO"
        else: print "OK"
  else:
     print "Non ci sono Nodeagents running"
  print "Synchronization done"