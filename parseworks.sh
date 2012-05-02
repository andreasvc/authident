#!/bin/bash
# parses a series of textfiles in sub-directories of "books/"
# results are placed in files with '.stp' extensions, one tree per line.
#The following parameters should be configured:
JAVA="/datastore/acranenb/SOFTWARE/Java/jdk1.6.0/bin/java"
STANFORDPARSER="/datastore/acranenb/src/stanford-parser-2012-03-09/"
NUMPROC=16

N=0
for a in books/*/*.txt
do
	$JAVA -Xmx5000m -cp "$STANFORDPARSER/*:" \
		edu.stanford.nlp.parser.lexparser.LexicalizedParser \
		-outputFormat oneline \
		-writeOutputFiles \
		$STANFORDPARSER/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz \
		"$a" \
		2> /dev/null &
	N=$[ $N + 1 ]
	if [[ $[$N % $NUMPROC] -eq 0 ]]; then
			echo waiting for batch $[ $N / $NUMPROC ]
			wait
	fi
done
wait
echo finished; parsed $N files.
