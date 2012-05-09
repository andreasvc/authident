#!/bin/sh
#wrapper script to parse some files. redirects stderr to /dev/null because stanford parser is too verbose
JAVA="/datastore/acranenb/SOFTWARE/Java/jdk1.6.0/bin/java"
STANFORDPARSER="/datastore/acranenb/src/stanford-parser-2012-03-09"
LEXPARSE=edu.stanford.nlp.parser.lexparser.LexicalizedParser #we actually use an UNlexicalized grammar! 
GRAMMAR=edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz

$JAVA -Xmx5000m -cp $STANFORDPARSER/*: $LEXPARSE \
	-outputFormat oneline \
	-writeOutputFiles \
	$STANFORDPARSER/$GRAMMAR \
	"$@" 2>/dev/null \
 && echo "done parsing $*" || echo "error with $*"
