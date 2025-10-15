
import os
import java.io.File as f
import sys

print "Info V. 1.0"
from time import gmtime, strftime

def getResourcesPath():
    return  "%s/../resources" %(os.path.dirname(__file__))

def getCommonPath():
    return  "%s/../common" %(os.path.dirname(__file__))

def getApplicationPath():
    return  "%s/../../input/AppDeployment" %(os.path.dirname(__file__))

def getApplicationPropertiesPath():
    return  "%s/../../input/AppDeployment/props" %(os.path.dirname(__file__))


def printStatement(msg):
    tm =strftime("%d-%m-%Y %H.%M.%S",gmtime())
    print "[%s] %s" % (tm, msg)


