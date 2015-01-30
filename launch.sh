#!/bin/bash
#AUTORUNDISABLE 
VERSION="0.1"

echo "wisecondor debug" > /tmp/ion-wisecondor

OUTFILE=${RESULTS_DIR}/${PLUGINNAME}.html 

echo "<html><body>test ${PLUGINCONFIG__TEST} </body></html>" > $OUTFILE

