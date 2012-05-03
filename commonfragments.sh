#!/bin/bash
NUMPROC=16
OUTDIR=fragments
DEVORTEST=test
FRAGMENTSEEKER=../disco-dop/fragmentseeker.py

mkdir -p $OUTDIR
N=0
# 4 folds, 5 authors against 5 authors, test each work 5 times
TOTAL=$[ 4 * 5 * 5 * 5 ]

for part in `seq 0 4`
do
	for fold in `seq 0 3`
	do
		for testtext in splits/*.$fold.$DEVORTEST$part
		do
			aa=`basename "$testtext"`
			for authortext in splits/*.train$fold
			do
				bb=`basename "$authortext"`
				output=$OUTDIR/"$bb"_"$aa"
				# if file does not exist or has zero-size:
				if [ ! -e "$output" ] || [ ! -s "$output" ]; then
					#echo compare $authortext with $testtext write to $output
					#echo python $FRAGMENTSEEKER --exact --numproc 1 --quiet "$authortext" "$testtext" \> "$output"
					(python $FRAGMENTSEEKER \
						--exact --numproc 1 --quiet \
						"$authortext" "$testtext" > "$output" \
						&& (wc -l "$output" && echo Job $N of $TOTAL finished) \
						|| echo error with $output) &
					N=$[ $N + 1 ]
					if [[ $[$N % $NUMPROC] -eq 0 ]]; then
						echo -n waiting for batch $[ $N / $NUMPROC ] 
						echo " of $[ $TOTAL / $NUMPROC ]"
						wait
					fi
				fi
			done
		done
	done
done
echo $N / $TOTAL
