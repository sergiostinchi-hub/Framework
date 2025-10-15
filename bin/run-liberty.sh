#!/bin/bash
ANT_HOME=../apache-ant/

export JAVA_HOME=../jdk1.8.0_152/

echo "call ant for liberty"

../apache-ant/bin/ant build-liberty.xml