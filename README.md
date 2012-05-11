authident
=========

Authorship attribution with syntactic fragments.
Cf. http://staff.science.uva.nl/~acranenb/clfl2012.pdf

Requirements:

- [Stanford parser](http://nlp.stanford.edu/software/lex-parser.shtml]
- [disco-dop](http://github.com/andreasvc/disco-dop]
- [Python 2.6+](http://www.python.org]
- [NLTK](http://www.nltk.org]

Usage:

- run `runexpfederalist.sh` to download the federalist papers and evaluate on the disputed and co-authored papers.

alternatively, evaluate on larger set of texts with cross-validation:

- prepare a directory `books/` with one directory for each author, each containing one `.txt` file per work in UTF-8.
- edit `parseworks.sh` and `parsefiles.sh` to set the right paths for Java and the Stanford parser
- edit and run `runexpbooks.sh`

