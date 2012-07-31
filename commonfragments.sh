#!/bin/bash
NUMPROC=16
INDIR=$1
OUTDIR=$2
DEVORTEST=$3
FRAGMENTSEEKER=../disco-dop/fragments.py

echo extracting fragments
for fold in `seq 0 3`; do
	for authortext in $INDIR/*.$fold.train; do
		if [ -e "$authortext" ]; then
			(find $INDIR -name "*.$fold.$DEVORTEST*" -print0 \
			| xargs --null \
				python $FRAGMENTSEEKER --quiet --batch $OUTDIR "$authortext" \
			&& echo "Compared all unknown test chunks in fold $fold to known texts of $authortext " \
			|| echo error with $authortext) &
		fi
	done
done
wait
echo done

