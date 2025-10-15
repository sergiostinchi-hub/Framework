#/bin/sh
read -p "Make your choice `echo $'\n1) Install WebSphere Application Server '` `echo $'\n2) Configure Resources for WebSphere Application Server '` `echo $'\n3) Install and configure Liberty Servers '` `echo $'\nMake your choice> '`" RESP
if [ $RESP = '1' ]; then
	./run-install.sh
elif [ $RESP = '2' ]; then
	./run-customize.sh
elif [ $RESP = '3' ]; then
   ./run-customize.sh
fi
