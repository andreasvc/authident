#!/bin/bash
# parses a series of textfiles in sub-directories of "books/"
# results are placed in files with '.stp' extensions, one tree per line.
#The following parameters should be configured: (and the ones in parsefiles.sh)
NUMPROC=16
BOOKS=$1

N=`find $BOOKS -name "*.txt" | wc -l`
echo "parsing texts"
find $BOOKS -name "*.txt" -print0 | xargs --null --max-procs=$NUMPROC --max-args=1 ./parsefiles.sh \
 && echo "finished; parsed $N files." || echo some problem occurred.
