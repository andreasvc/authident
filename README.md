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
- edit parseworks.sh and parsefiles.sh to set the right paths for Java and the stanford parser
- edit and run runexpbooks.sh
- alternatively, run runexpfederalist.sh to download the federalist papers and evaluate on the disputed and co-authored papers.

