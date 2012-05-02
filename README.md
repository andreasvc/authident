authident
=========

Authorship attribution with syntactic fragments

Requirements:

- Stanford parser
- disco-dop http://github.com/andreasvc/disco-dop
- Python 2.6+
- NLTK

Procedure:

- prepare a directory "books/" with one directory for each author, each containing one file per work in UTF-8.
- edit parseworks.sh to set the right paths and run. Will parse documents with stanford parser
- run devtestsplits.py: make dev-test-train set splits with leave-one-out cross-validation, results written to "splits/"
- edit commonfragments.sh to set the location of disco-dop and run. Will extract syntactic fragments, results written to "out/"
- run evaluate.py: do classification & evaluation

