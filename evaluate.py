import os, re, cPickle
from os.path import basename
from glob import glob
from pprint import pprint
from nltk import Tree, ConfusionMatrix

termsre = re.compile(r"[^ )]\)")
#works for both trees and word/POS ngrams
contentwordsre =  re.compile(r"(?:/|\()(NN(?:[PS]|PS)?|(?:JJ|RB)[RS]?|VB[DGNPZ])\b(?! \))")
functionwordsre = re.compile(r"(?:/|\()(CC|DT|EX|IN|MD|PDT|PRP[\$]?|RP|TO|WDT|WP[\$]?|WRB)\b(?! \))")
fragcontentwordsre =  re.compile(r"\((NN(?:[PS]|PS)?|(?:JJ|RB)[RS]?|VB[DGNPZ])\b(?! \))")
fragfunctionwordsre = re.compile(r"\((CC|DT|EX|IN|MD|PDT|PRP[\$]?|RP|TO|WDT|WP[\$]?|WRB)\b(?! \))")
ngramcontentwordsre = re.compile(r"\b(NN[SP]?|NNPS|RB[RS]?|JJ[RS]?|VB[DGNPZ]?)\b")
ngramfunctionwordsre = re.compile(r"\b(CC|DT|EX|IN|MD|PDT|PRP[\$]?|RP|TO|WDT|WP[\$]?|WRB)\b")
frontier = re.compile(r" \)")
def terms(a):
	return len(termsre.findall(a))

def contentwords(a):
	return len(contentwordsre.findall(a))

def frontiernodes(a):
	return len(frontier.findall(a))

def nodes(a):
	return a.count("(")

def truenodes(a):
	return a.count("(") + terms(a)

def depth(a):
	return a.count("(") #this is wrong but works to check if depth > 1

def getauthor(name):
	"""return first word of filename, Capitalized."""
	return basename(name).split(".")[0].split(",")[0].capitalize()

def evaluate(fragments, sumfunc, condition, normalization, verbose=True, perbook=False, topfragments=False, breakdown=True, conftable=False):
	green = "\033[32m"; red = "\033[31m"; gray = "\033[0m" # ANSI codes
	names = set(map(getauthor, fragments.values()[0]))
	results = {}
	# heading
	if verbose and not perbook:
		print "\n &", 21 * " ",
		print "&".join(a.rjust(16) for a in sorted(names)),
		print "&\tguess &\t\t\tconfidence\\\\"
	prev = "foo.bar"
	# loop over texts to be classified
	for text in sorted(fragments):
		if perbook and getauthor(text) != getauthor(prev):
			print "\n &", 21 * " ",
			print " &".join("\\rotatebox{45}{%s}" % a.split(" - ")[-1].split(".")[0].replace("&","\\&") for a in sorted(fragments[text])), "\\\\"
		if verbose: print text.split(" - ")[-1].split(".")[0][:25].replace("&","\\&").ljust(25),
		inter = {}
		# loop over possible authors
		for author in sorted(fragments[text]):
			inter[author] = sum(map(sumfunc, filter(condition, fragments[text][author].items()))) / normalization(text, author)
		if verbose:
			for author in sorted(inter):
				if inter[author] == max(inter.values()): l,r = "\\textbf{","}"
				else: l, r = "".ljust(8), " "
				if isinstance(inter[author], float): print ("& %s%.2f%s" % (l,inter[author],r)).rjust(16),
				elif isinstance(inter[author], int): print ("& %s%d%s" % (l,inter[author],r)).rjust(16),
				else: print "& %s%s" % (l,repr(inter[author]).rjust(8),r),
		actualauthor = getauthor(text)
		guess = max(inter, key=inter.get)
		results.setdefault(actualauthor, []).append(guess)
		if verbose and not perbook:
			print "&",
			print green+"correct:" if getauthor(guess) == actualauthor else red+"wrong:  ",
			print getauthor(guess).ljust(10), gray,
			try: confidence = (100 * (max(inter.values()) - sorted(inter.values())[-2]) / float(max(inter.values())))
			except ZeroDivisionError: confidence = 0.0
			except IndexError: confidence = 0.0
			print "& %s%5.2f%s " % ((red if confidence < 50 else green), confidence, gray)
		elif verbose: print "\\\\"
		prev = text
	if verbose: print

	if topfragments: print "top fragments"
	for name in sorted(names) if topfragments else ():
		for text in sorted(fragments):
			if not getauthor(text) == name: continue
			print text
			for label in ("(ROOT", "(S ", "(NP ", "(VP ", "(PP "):
				guess = max(fragments[text], key=lambda x: sum(sumfunc(a) for a in fragments[text][x].items() if condition(a)) / norm(x))
				try:
					frag = max((a[0] for a in fragments[text][guess].iteritems() if condition(a) and a[0].startswith(label)), key=lambda x: (sumfunc((x,fragments[text][guess][x])), fragments[text][guess][x]))
				except ValueError: pass
				else:
					f1 = Tree(frag)
					f2 = Tree(frag)
					print "%2d" % fragments[text][guess][frag], " ".join(a.replace(" ", "_")[:-1] for a in re.findall(r" \)|[^ )]+\)", frag)),
					try: f2.un_chomsky_normal_form()
					except: print f1.pprint(margin=9999, parens=("[", " ]"))
					else: print f2.pprint(margin=9999, parens=("[", " ]"))
		print
	if perbook: return
	if topfragments: print

	if conftable:
		print "Confusion matrix"
		ref  = [a for a in results for b in results[a]]
		test = [getauthor(b) for a in results for b in results[a]]
		cf = ConfusionMatrix(ref, test)
		print '\t\t&%s\\\\' % "\t& ".join(sorted(set(test)))
		for a in sorted(set(ref)):
			print a.ljust(15),
			for b in sorted(set(test)):
				c = "& "
				if a == b: c = ("& \\textbf{%d}" % cf[a,b])
				elif cf[a,b]: c = ("& %d" % cf[a,b])
				print c.rjust(10),
			print r"\\"
		print

	avg = sum(1 for a in results for b in results[a] if a == getauthor(b)) / float(sum(map(len, results.values())))
	if breakdown:
		print "Accuracy"
		z=[]
		for a in sorted(results):
			acc = sum(1 for b in results[a] if a == getauthor(b)) / float(len(results[a]))
			print getauthor(a).ljust(16), "&   ",
			print "%.2f \\%% \\\\" % (100 * acc)
			z.append(acc)
		print "macro average:".ljust(16), "&   %6.2f \\%% \\\\" % (100 * sum(z)/float(len(z)))
		print "micro average:".ljust(16), "&   %6.2f \\%% \\\\" % (100 * avg)
	else: print "average:".ljust(16), "&   %6.2f \\%% \\\\" % (100 * avg)

def readtest(inputdir, folds, chunks, devortest):
	fragments = {}
	m = 0
	pattern = "%s/*.%s*" % (inputdir, devortest)
	files = glob(pattern)
	assert files, pattern
	for a in files:
		fold = int(a.rsplit(".", 2)[1])
		chunk = int(a.rsplit(devortest, 1)[1])
		possibleauthor, work = a.split("/")[-1].split("_")
		if fold < folds and chunk < chunks:
			if work not in fragments: fragments[work] = {}
			fragments[work][possibleauthor] = dict(
				(a, int(b)) for a, b in (line.rsplit("\t", 1)
					for line in open(a)))
			m += 1
	print "read %d %s files" % (m, devortest)
	assert fragments
	return fragments

def readtrain(pattern, sents=None):
	authors = sorted(glob(pattern))
	authorsets = dict((a.rsplit("/", 1)[-1], set(open(a).read().splitlines())) for a in authors)
	print "read %d train files" % len(authors)
	for a in sorted(authorsets): print a, len(authorsets[a]),
	print
	sentsinwork  = dict((a.split("/")[-1], float(len(authorsets[a.split("/")[-1]]))) for a in authors)
	wordsinwork = dict((a.split("/")[-1], terms(open(a).read())) for a in authors)
	nodesinwork  = dict((a.split("/")[-1], nodes(open(a).read())) for a in authors)
	return authorsets, sentsinwork, wordsinwork, nodesinwork

def combine(a, b):
	assert a.keys() == b.keys(), (a.viewkeys() - b.viewkeys(), b.viewkeys() - a.viewkeys())
	assert all(a[x].keys() == b[x].keys() for x in a)
	for t in a:
		for aa in a[t]:
			b[t][aa].update((x, y) for x,y in a[t][aa].items())
	return b

def normalize(a):
	for t in a:
		for u in a[t]:
			total = float(sum(a[t][u].values()))
			a[t][u] = dict((x, y / total) for x, y in a[t][u].items())
	return a

def removecommon(fragments):
	# remove common fragments
	new = {}
	for text, ft in fragments.iteritems():
		for author in ft:
			u = set(a for aa, fta in ft.iteritems() if aa != author for a in fta)
			new.setdefault(text, {})[author] = dict((a, b) for a,b in ft[author].items() if a not in u)
	return new

def mergetest(fragments, spliton=".", n=0):
	""" merge test sets. a numeric id is expected after "spliton".
	if n is given, merge test chunks into partitions of length n,
	otherwise everything is merged into a single chunk."""
	new = {}; m = 0
	tmp = {}
	for text in fragments:
		pre, post = text.rsplit(spliton, 1)
		if n: m = int(post) / n
		for author in fragments[text]:
			newtext = "%s%s%d" % (pre, spliton, m)
			tmp.setdefault(newtext, set()).add(text)
			dest = new.setdefault(newtext, {}).setdefault(author, {})
			# if the frequencies are of the test text:
			#for a,b in fragments[text][author].iteritems(): dest[a] += b
			# if they come from the reference text:
			dest.update(fragments[text][author])
	return new

def perbook():
	nothresh = lambda _: True
	norm = lambda _: 1
	sumfunc = lambda _: 1
	sumfunc = lambda (x, y): truenodes(x)
	evaluate(readtest("perbook"), sumfunc, nothresh, norm, verbose=True, perbook=True)

def federalist():
	authorsets, sentsinwork, wordsinwork, nodesinwork = readtrain("fedsplits/*.*.train")
	ngrams = removecommon(readtest("fedngrams", 1))
	frag = removecommon(readtest("fedfragments", 1))
	nothresh = lambda _: True
	norm = lambda x, y: float(len(frag[x][y])) #nodesinwork[y] / sentsinwork[y]
	sumfunc = lambda (x,y): 3
	evaluate(ngrams,   sumfunc, nothresh, norm, verbose=True)
	sumfunc = lambda (x,y): len(fragcontentwordsre.findall(x))
	evaluate(frag,   sumfunc, nothresh, norm, verbose=True)
	sumfunc = lambda (x,y): len(fragcontentwordsre.findall(x)) if x.startswith("(") else 3
	evaluate(combine(ngrams,   frag),   sumfunc, nothresh, norm, verbose=True)

def main(devortest):
	assert devortest in ("dev", "test")
	authorsets, sentsinwork, wordsinwork, nodesinwork = readtrain("splits/*.*.train")
	print "trigrams:",
	ngramdata = readtest("ngrams", 4, 25, devortest)
	ngrams = removecommon(ngramdata.copy())
	ngrams100 = removecommon(mergetest(ngramdata.copy(), n=5, spliton=devortest))
	ngrams500 = removecommon(mergetest(ngramdata.copy(), spliton=devortest))
	print "fragments:",
	fragdata = readtest("fragments", 4, 25, devortest)
	frag = removecommon(fragdata.copy())
	frag100 = removecommon(mergetest(fragdata.copy(), n=5, spliton=devortest))
	frag500 = removecommon(mergetest(fragdata.copy(), spliton=devortest))
	print len(ngrams), len(ngrams100), len(ngrams500)
	print len(frag), len(frag100), len(frag500)
	assert len(ngrams) == len(frag) == 500
	assert len(ngrams100) == len(frag100) == 100
	assert len(ngrams500) == len(frag500) == 20
	assert all(len(a) == 5 for a in ngrams.values())
	assert all(len(a) == 5 for a in ngrams100.values())
	assert all(len(a) == 5 for a in ngrams500.values())
	assert all(len(a) == 5 for a in frag.values())
	assert all(len(a) == 5 for a in frag100.values())
	assert all(len(a) == 5 for a in frag500.values())
	nothresh = lambda _: True
	freqthresh = lambda (x,y): y > 2
	fragthresh = lambda (x,y): y > 2 or not x.startswith("(")
	norm = lambda x, y: nodesinwork[y] / sentsinwork[y]

	breakdown = False; conftable = False
	sumfunc = lambda (x,y): len(fragcontentwordsre.findall(x)) if x.startswith("(") else 3
	print "trigrams   (20 sents)",
	evaluate(ngrams, sumfunc, nothresh, norm, verbose=False, breakdown=breakdown, conftable=conftable)
	print "fragments  (20 sents)",
	evaluate(frag, sumfunc, nothresh, norm, verbose=False, breakdown=breakdown, conftable=conftable)
	print "combined   (20 sents)",
	evaluate(combine(ngrams, frag), sumfunc, nothresh, norm, verbose=False, breakdown=breakdown, conftable=conftable)
	
	print "\ntrigrams  (100 sents)",
	evaluate(ngrams100, sumfunc, nothresh, norm, verbose=False, breakdown=breakdown, conftable=conftable)
	print "fragments (100 sents)",
	evaluate(frag100, sumfunc, nothresh, norm, verbose=False, breakdown=breakdown, conftable=conftable)
	print "combined  (100 sents)",
	evaluate(combine(ngrams100, frag100), sumfunc, nothresh, norm, verbose=False, breakdown=breakdown, conftable=conftable)
	
	print "\ntrigrams  (500 sents)",
	evaluate(ngrams500, sumfunc, nothresh, norm, verbose=False, breakdown=breakdown)
	print "fragments (500 sents)",
	evaluate(frag500, sumfunc, nothresh, norm, verbose=False, breakdown=breakdown)
	print "combined  (500 sents)",
	evaluate(combine(ngrams500, frag500), sumfunc, nothresh, norm, verbose=False, topfragments=False, breakdown=breakdown)

if __name__ == '__main__':
	from sys import argv
	if argv[1] == "federalist": federalist()
	else: main(argv[1])

