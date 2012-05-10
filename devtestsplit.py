import os, random, re, codecs
from itertools import izip_longest
from sys import argv
from glob import glob

def devtestsplit(indir, outdir):
	""" produce n-fold train/dev/test splits: 
	splits/[author].train0
	splits/[author].title.0.test0
	splits/[author].title.0.test1
	splits/[author].title.0.dev1
	"""
	trainchunk = 15000		#no. of sents for known author text
	testchunk = 20			#no. of sents in a single test chunk
	maxtestchunks = 25		#number of test chunks for one fold
	texts = glob("%s/*/*.stp" % indir)
	cnt = 0
	os.mkdir("splits/")
	authors = filter(os.path.isdir, glob("%s/*" % indir))
	assert authors
	for author in authors:
		works = sorted(glob("%s/*.stp" % author))
		assert works, "%s/*.stp" % author
		author = author.split("/", 1)[1]
		os.mkdir("%s/%s" % (outdir, author))
		for n, work in enumerate(works):
			print work
			otherworks = [a for a in works if a != work]
			# initial segment
			#train = [a for otherwork in otherworks
			#	for a in codecs.open(otherwork, encoding="UTF-8")]
			# true random sample, not repeatable
			#train = random.sample(train, trainchunk)
			# interleave sentences of all works, to obtain a repeatable, representative sample.
			# i.e., each work contributes at least min(len(work), len(allworks) / len(works))
			train = [a for b in izip_longest(*(codecs.open(otherwork,
				encoding="UTF-8") for otherwork in otherworks)) for a in b if a]
			codecs.open("%s/%s.%d.train" % (outdir, author, n), "w",
				encoding="UTF-8").writelines(train[:trainchunk])
			text = codecs.open(work, encoding="UTF-8").readlines()
			work = work.split("/", 1)[1]
			dev = text[:len(text)/2]
			test = text[len(text)/2:]
			for m in range(0, len(dev), testchunk):
				if m / testchunk == maxtestchunks: break
				codecs.open("%s/%s.%d.dev%d" % (outdir,
					work.rsplit(".", 2)[0], n, m / testchunk), "w",
					encoding="UTF-8").writelines(dev[m:m+testchunk])
				cnt += 1
			for m in range(0, len(test), testchunk):
				if m / testchunk == maxtestchunks: break
				codecs.open("%s/%s.%d.test%d" % (outdir,
					work.rsplit(".", 2)[0], n, m / testchunk), "w",
					encoding="UTF-8").writelines(test[m:m+testchunk])
				cnt += 1
	print "done. wrote %d files." % cnt

if __name__ == '__main__':
	assert len(argv) == 3, "usage: %s inputdir outputdir" % argv[0]
	devtestsplit(argv[1], argv[2])
