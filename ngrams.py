import re, os, glob
from sys import argv
from nltk import FreqDist, PorterStemmer, ingrams
assert len(argv) == 4, "usage: %s inputdir outputdir dev|test" % argv[0]
assert os.path.isdir(argv[1])
indir = argv[1]
wordposngram = "%s/" % argv[2]
os.mkdir(wordposngram)
assert argv[3] in ("dev", "test")
devortest=argv[3]
leaves = re.compile(r" ([^ )]+)\)")
pos = re.compile(r"\(([^ ]+) [^ )]+\)")
porter = PorterStemmer()
print "extracting ngrams"
for train in glob.glob("%s/*.*.train" % indir):
	fold = int(train.split(".")[-2])
	if fold > 3: continue
	postrigrams = FreqDist(ingrams((tag for t in open(train)
		for tag in pos.findall(t)), 3))
	wordpostrigrams  = FreqDist(ingrams((porter.stem(word)+"/"+tag
		for t in open(train)
		for word, tag in zip(leaves.findall(t), pos.findall(t))), 3))
	for test in glob.glob("%s/*/*.%d.%s*" % (indir, fold, devortest)):
		output = "%s_%s" % (train.split("/")[-1], test.split("/")[-1])
		testtrigrams = FreqDist(ingrams((porter.stem(word)+"/"+tag
			for t in open(test).readlines()
			for word,tag in zip(leaves.findall(t), pos.findall(t))), 3))
		open(wordposngram+output, "w").writelines("%s\t%d\n" % (" ".join(a), b)
			for a, b in testtrigrams.iteritems() if wordpostrigrams[a])
		print output
print "done"
