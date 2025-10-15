#!/bin/bash 
#set -x
echo "begin run shell"
value=''
buildfile=$1
builddir=`dirname $0`

cd $builddir
while read line 
do
	param=`echo $line|cut -d '=' -f1`
	
	if [[ $param = 'DeploymentManagerBin' ]] 
	then
		value=`echo $line|cut -d '=' -f2`
		echo "Deployment Manager path = $value"
		break
	fi
done < Resources.properties

if [[ $value = '' ]]
then
	echo "Please configure the Deployment Manager bin into the Resources.properties file and run again the script"
else
	if [[ $buildfile = '' ]]
	then
	   
     	$value/ws_ant.sh -buildfile configuration-build.xml $2
	else
	   
		$value/ws_ant.sh -buildfile $buildfile $2
	fi
fi 

