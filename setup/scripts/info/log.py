import os
import java.io.File as fileLog
import java.io.File as fileTrace
import sys
from time import gmtime, strftime



print "Initialize log framework v 1.1"
tm =strftime("%d-%m-%Y",gmtime())
logfileName="framework_%s.log" %tm
tracerFileName="framework_%s.trace" %tm
filelogger = open('/tmp/%s'%logfileName, 'a')
filelogger.write("Initialize log framework v 1.1")
filelogger.close
#f.close()
fileTracer = open('/tmp/%s'%tracerFileName, 'a')
fileTracer.write("Initialize log framework v 1.1")
fileTracer.close
ERROR_LEVEL=1
INFO_LEVEL=2
WARNING_LEVEL=3
DEBUG_LEVEL=4
TRACE_LEVEL=5

className=""
logLevel=4

def closeLogger():
 filelogger.close()
 fileTracer.close()

def writeTrace(msg):
   fileTracer.write(msg)
    
    
def writeLog(msg):
   filelogger.write(msg)
             
             
def setClass(cls):
    global className
    className=cls

def setLevel(lvl):
    global logLevel
    logLevel=lvl

def LINEBREAK():
    print "  "
    
    
def INFO(msg,position=None):
    tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
    prefix="[%s] I" %tm
    if logLevel >=INFO_LEVEL:
        if position==1:
            print "[%s] I %s" % (tm,msg),
        elif position==2: 
            print "%s" %  msg
        else:
             print "[%s] I %s" % (tm,msg)
        writeLog("%s %s" %(prefix ,msg))
        
def DEBUG(msg,position=None):
    tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
    prefix="[%s] D " %tm
    if logLevel >=DEBUG_LEVEL:
        tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
        if position==1:
            print "[%s]  D %s: %s" % (tm,className, msg),
        elif position==2: 
            print "%s" %  msg
        else:
             print "[%s] D %s: %s" % (tm,className, msg)
        writeTrace("%s %s" %(prefix ,msg))


def WARNING(msg):
    tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
    prefix="[%s] W" %tm
    if logLevel >=WARNING_LEVEL:
        tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
        print "[%s] W %s" % (tm, msg)
        writeTrace("%s %s" %(prefix ,msg))

def ERROR(msg):
    tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
    prefix="[%s] E" %tm
    if logLevel >=ERROR_LEVEL:
        tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
        print "[%s] E %s" % (tm, msg)
        writeTrace("%s %s" %(prefix ,msg))
    
def ERROR(msg,position=None):
    tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
    prefix="[%s] E" %tm
    if logLevel >=ERROR_LEVEL:
        tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
        if position==1:
            print "[%s] E %s" % (tm, msg),
        elif position==2: 
            print "%s" %  msg
        else:
             print "[%s] E %s" % (tm, msg)
        writeTrace("%s %s" %(prefix ,msg))

def TRACE(msg,position=None):
    tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
    prefix="[%s] Trace >> " %tm
    if logLevel >=TRACE_LEVEL:
        tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
        if position==1:
            print "[%s]  T %s: %s" % (tm,className, msg),
        elif position==2: 
            print "%s" %  msg
        else:
             print "[%s] T %s: %s" % (tm,className, msg)
        writeTrace("%s %s" %(prefix ,msg))

def time():
        tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
        
