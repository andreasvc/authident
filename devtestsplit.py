import os, random, sys, re, codecs
from glob import glob

def devtestsplit():
	""" produce n-fold train/dev/test splits: 
	splits/[author].train0
	splits/[author].title.0.test0
	splits/[author].title.0.test1
	splits/[author].title.0.dev1
	"""
	testchunk = 100
	trainchunk = 15000
	maxtestchunks = 5
	texts = glob("books/*/*.stp")
	cnt = 0
	for author in glob("books/*"):
		if not os.path.isdir(author): continue
		author = author.lstrip("books/")
		os.mkdir("splits/%s" % author)
		works = glob("%s/*.stp" % author)
		for n, work in enumerate(works):
			print work
			otherworks = [a for a in works if a != work]
			train = [a for otherwork in otherworks
				for a in codecs.open(otherwork, encoding="UTF-8")]
			codecs.open("splits/%s.train%d" % (author, n), "w",
				encoding="UTF-8").writelines(train[:trainchunk])
			text = codecs.open(work, encoding="UTF-8").readlines()
			dev = text[:len(text)/2]
			test = text[len(text)/2:]
			for m in range(0, len(dev), testchunk):
				if m / testchunk == maxtestchunks: break
				codecs.open("splits/%s.%d.dev%d" % (
					work.rstrip(".txt.stp"), n, m / testchunk), "w",
					encoding="UTF-8").writelines(dev[m:m+testchunk])
				cnt += 1
			for m in range(0, len(test), testchunk):
				if m / testchunk == maxtestchunks: break
				codecs.open("splits/%s.%d.test%d" % (
					work.rstrip(".txt.stp"), n, m / testchunk), "w",
					encoding="UTF-8").writelines(test[m:m+testchunk])
				cnt += 1
	print "done. wrote %d files." % cnt

if __name__ == '__main__': devtestsplit()
