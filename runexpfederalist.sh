#!/bin/bash
NUMPROC=16
if [ ! -e federalist.txt ]; then
	wget -O federalist.txt \
		http://mirrors.xmission.com/gutenberg/1/18/18.txt
fi
python splitfed.py \
&& sh parseworks.sh fed \
&& mkdir fedsplits \
&& mkdir "fedsplits/Hamilton Or Madison" \
&& mkdir "fedsplits/Hamilton And Madison" \
&& cat fed/Jay/*.stp >fedsplits/Jay.0.train \
&& cat fed/Madison/*.stp >fedsplits/Madison.0.train \
&& cat fed/Hamilton/*.stp >fedsplits/Hamilton.0.train \
|| exit 1

for a in fed/Hamilton\ {And,Or}\ Madison/*.stp; do
	cp "$a" "fedsplits/Madison/Madison - `basename "$a"`.0.test0" 
done

mkdir fedfragments && mkdir fedngrams \
&& python ngrams.py fedsplits fedngrams test \
&& sh commonfragments.sh fedsplits fedfragments test \
&& python evaluate.py federalist
