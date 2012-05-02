#!/bin/bash
NUMPROC=16
FRAGMENTSEEKER=../disco-dop/fragmentseeker.py
mkdir -p out
N=0
TOTAL=$[ `ls -1 splits/*/*.train | wc -l` * `ls -1 splits/*/*.dev* | wc -l` ]

for authortext in splits/*.train
do
	for testtext in splits/*.dev*
	do
		output=out/"$testauthor"_$authortext
		(python $FRAGMENTSEEKER --numproc 1 --quiet \
			"$authortext" "$testtext" > $output \
		&& wc -l $output \
		|| echo error with $output) &
		echo compare $authortext with $testtext write to out/"$testauthor"_$authortext
		N=$[ $N + 1 ]
		if [[ $[$N % $NUMPROC] -eq 0 ]]; then
			echo waiting for batch $[ $N / $NUMPROC ] of $[ $TOTAL / $NUMPROC ]
			wait
		fi
	done
done
