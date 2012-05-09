import os
out = None
outdir = "fed"
init = False
n = None
os.mkdir(outdir)
authors = ("Jay", "Hamilton", "Madison",
	"Hamilton And Madison", "Hamilton Or Madison")
for a in authors: os.mkdir("%s/%s" % (outdir, a))
for a in open("federalist.txt").readlines():
	if a.startswith("FEDERALIST"):
		if out: out.close()
		init = True
		n = int(a.split("No.")[1])
	elif a.startswith("End of the Project Gutenberg EBook"): break
	if init:
		if a.strip().title() in authors:
			if out: out.close()
			out = open("%s/%s/%d.%s.txt" % (
				outdir, a.strip().title(), n, a.strip()), "w")
			init = False
	elif out: out.write(a)
else: assert False, "expected end of ebook marker!"
