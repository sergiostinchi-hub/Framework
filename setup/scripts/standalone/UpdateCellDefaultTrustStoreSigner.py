#! /usr/bin/python
# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version


# Import

import java
import os
from string import replace
global f, reportName
from time import gmtime, strftime

# Variables
scriptName = "UpdateCellDefaultTrustStoreSigner.py"
version = "1.0.0"
pathCertificates=""
signers = [ '','' ]  

print "%s V%s" % (scriptName, version)

# Command Line
argc = len(sys.argv)
if argc != 1:
   print"Usage: <certPath>"
   sys.exit(-1)


startt = 0   
signer = sys.argv[0]

print("signer = %s" % signer)


if (signer == None) or (len(signer.strip()) == 0):
   print "ERROR: The variable signer cannot be blank or null"
   print "%s done" % (scriptName)
   sys.exit(-1)

def clearExit(text, status):
   if len(text): print text
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   print "Elapsed Time: %.3f s" % (time.clock() - startt)
   print "%s done" % scriptName
   sys.exit(status)
   return
def syncEnv(hasChanges):
   if hasChanges == 1: 
      print"Save ..."
      AdminConfig.save() 
      print"Save done"
      print"Synchronization ..."
      nodes = AdminControl.queryNames('type=NodeSync,*') 
      if len(nodes) > 0: 
         nodelist = nodes.splitlines()       
         for node in nodelist: 
            beg = node.find('node=') + 5 
            end = node.find(',', beg) 
            print"Synchronization for node \"" + node[beg:end] + "\" :",
            try: AdminControl.invoke(node, 'sync') 
            except: print"KO"
            else: print"OK"
         print"Synchronization done"    
      else:
         print"No Nodeagent found "
   else: 
      print"No changes made syncronization skipped"
# end def

def mydate():
        tm =strftime("%Y-%m-%d" ,gmtime())
        return tm

def insertSigner(pathCert,typOfStore):
   cell = AdminConfig.list('Cell')
   cellName = AdminConfig.showAttribute(cell, 'name')
   if (typOfStore == None) or (len(typOfStore.strip()) == 0):
      typOfStore='CellDefaultTrustStore'
   
   alias = os.path.basename(signer)
   alias = alias[0:len(alias)-4]
   alias = "%s_%s" %(alias,mydate())
   
   print "#################### UpdateTrustStoreSigner ####################### " 
   print "TrustStore %s" %typOfStore
   print "certificate path %s" %signer
   print "Alias  %s" %alias
   print "#################### UpdateTrustStoreSigner ####################### "
   try:   
      print "Update %s  " %typOfStore,
      AdminTask.addSignerCertificate('[-keyStoreName %s -keyStoreScope (cell):%s -certificateFilePath %s -base64Encoded true -certificateAlias %s ]' %(typOfStore,cellName,signer,alias))
      print "OK"
   except:
      print " KO"
      type, value, traceback = sys.exc_info()
      print "ERROR: %s (%s)" % (str(value), type)
      clearExit(" - KO: Rollback and exit", -1)  


insertSigner(signer,"")
syncEnv(AdminConfig.hasChanges())

print("%s V%s done" % (scriptName, version))
