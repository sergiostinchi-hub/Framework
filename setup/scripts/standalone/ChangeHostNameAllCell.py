# Authors: Sergio Stinchi

# Version        Description
# 1.1.0          Correct Variable description
# 1.0.0          Starting version


import os
import java.io.File as fileLog
import java.io.File as fileTrace
import sys
from time import gmtime, strftime


# Variables
scriptName = "ChangeHostNameAllCell.py"
version = "1.0.0"

#Usare il dictionary leggendo da un file ed inserendolo nella struttura dai creata
#HostOld2HostNewList = [ ['ENWAS8V04-01.srv.sogei.it','hostName1'],['ENWAS8V04-02.srv.sogei.it','hostName2'] ]                    
HostOld_HostNew = {}
#HostOld_HostNew["ENWAS8V04-01.srv.sogei.it"] = "hostName1"
#HostOld_HostNew["ENWAS8V04-02.srv.sogei.it"] = "hostName2"

def loggerInfo(msg,position=None):
    tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
    prefix="[%s] I" %tm
    if position==1:
        print "[%s] I %s" % (tm,msg),
    elif position==2: 
        print "%s" %  msg
    else:
        print "[%s] I %s" % (tm,msg)

print "%s V%s" % (scriptName, version)
loggerInfo("Read target data file %s" % (sys.argv[0]))
file = sys.argv[0]

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return 0
    for x in a:
        if not x.isdigit():
            return 0
        i = int(x)
        if i < 0 or i > 255:
            return 0
    return -1

def ip_address_validator(ip):
   try:
      ip_obj = ipaddress.ip_address(ip)
      print("%s is a valid IP address" %(ip))
      clearExit(" There is an IpAddress as HostName - RollBack and Exit", -1)
   except ValueError:
      print("HostName %s is correct so Continue " %(ip) )
    
def polulateDict(file):
   # Struttura linea file "hostOld:hostNew:TypeHost"
   #loggerInfo("Begin polulateDict")
   file1 = open(file, 'r')
   Lines = file1.readlines()
   count = 0
   # Strips the newline character
   for line in Lines:
      count += 1
      #print("Line: %s: %s" %(count, line.strip()))
      HostOld = line.split(',')[0].strip().split(".")[0]
      HostNew = line.split(',')[1].strip()
      #print "Line[0] HostName old = %s" % (HostOld)
      #print "Line[1] HostName new = %s" % (HostNew)
      #print("Line[2] TypeHost = %s" % (line[2]))
      HostOld_HostNew[HostOld]=HostNew
   print ("Dictionary created is %s" %(HostOld_HostNew))
   #end for


def clearExit(text, status):
   if len(text): print text
   AdminConfig.reset()
   print "%s done" % scriptName
   sys.exit(status)
   return

def syncEnv(hasChanges):
   if hasChanges == 1: 
      loggerInfo("Save ...") 
      AdminConfig.save() 
      loggerInfo("Save done") 
      loggerInfo("Synchronization ...") 
      nodes = AdminControl.queryNames('type=NodeSync,*') 
      if len(nodes) > 0: 
         nodelist = nodes.splitlines()       
         for node in nodelist: 
            beg = node.find('node=') + 5 
            end = node.find(',', beg) 
            loggerInfo("Synchronization for node \"" + node[beg:end] + "\" :",1)
            try: AdminControl.invoke(node, 'sync') 
            except: loggerInfo("KO",2) 
            else: loggerInfo("OK",2)
         loggerInfo("Synchronization done")    
      else:
         loggerInfo("No Nodeagent found ") 
   else: 
      loggerInfo("No changes made syncronization skipped") 
    
def _splitlines(s):
  rv = [s]
  if '\r' in s:
    rv = s.split('\r\n')
  elif '\n' in s:
    rv = s.split('\n')
  if rv[-1] == '':
    rv = rv[:-1]
  return rv


def getTypeName(id):
   ObjStr = str(id)
   beg = id.find('#') + 1
   end = id.find('_', beg)
   sType = id[beg:end]
   return sType

def AdminConfigShowAttribute(obj, attrib):
   result=''
   try:
      result = str(AdminConfig.showAttribute(obj, attrib))
      if result == 'None': result = ''
      return result
   except:
      type, value, traceback = sys.exc_info()
      loggerInfo("%s (%s)" % (str(value), type))
      return result


def isString(str):
   try: 
      str = str.upper() 
      return 0
   except AttributeError: 
      return -1
########################### MAIN ######################################
polulateDict(file)

nodes = AdminConfig.list('Node').splitlines()
for node in nodes:
   nodeName = AdminConfigShowAttribute(node, 'name')
   print("     ")
   loggerInfo("Begin ChangeHost Name for Node %s" %(nodeName))
   #estrarre l'hostname del rispettivo nodo
   #fare la get dal dictionary della chiave con hostname attuale
   #se c'è si procede alla sostituzuione usando il  nome del nodo (var:node)
   #nel caso in cui non esista un hostname corrispondente la procedura si blocca e ritorna un codice di errore
   #Attività effettuata con DMGspento, senza syncEnv
   hostNameOld = AdminConfigShowAttribute(node, 'hostName')
   HostNameWithoutDomain = hostNameOld.split(".")[0]
   loggerInfo("   Current HostName is : %s Dictionary_Key will be %s" %(hostNameOld,HostNameWithoutDomain))
   validIP = validate_ip(hostNameOld)
   if validIP == -1:
         msgLogger = "Current HostName %s is an IPAddress ROLLBACK and Exit" %(hostNameOld)
         clearExit(msgLogger,-1)
   hostNameNew = HostOld_HostNew.get(HostNameWithoutDomain)
   if hostNameNew == None:
      loggerInfo("   No Record Found for HostName:  %s No action will be done" %(HostNameWithoutDomain))
   else:
      loggerInfo("   New HostName is:  %s" %(hostNameNew))

   if isString(hostNameNew) == 0:
         loggerInfo("   Execute changeHostName for Node %s from OLD HostName %s to New HostName %s"  % (nodeName,hostNameOld,hostNameNew))
         #AdminTask.changeHostName('-hostName %s -nodeName %s -regenDefaultCert') % (HostMap,nodeName)
         #AdminConfig.save()
      #endif
   loggerInfo("End ChangeHost Name for Node %s" %(nodeName))
   print("     ")
#endfor



        

 