#!/bin/sh
sh parseworks.sh books
python devtestsplit.py books splits
mkdir ngrams/
mkdir fragments/
python ngrams.py splits ngrams dev
python ngrams.py splits ngrams test
sh commonfragments.sh splits fragments dev
sh commonfragments.sh splits fragments test
python evaluate.py dev
python evaluate.py test
