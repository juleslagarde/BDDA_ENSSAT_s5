import sys
from vocabulary import *
from rewriterFromCSV import *
from flight import Flight
import json

def printN(n, i):
	pass

def compute(rewriter):
	rw.open()
	flight = rewriter.readFlight()
	n = 0
	counter = dict()
	while flight:
		categ = flight.categorise()
		if categ in counter:
			counter[categ]+=1
		else:
			counter[categ]=1
		flight = rewriter.readFlight()
		n += 1
		if n % 100000 == 0:
			print(n)
	rw.close()
	return counter

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Usage: python %s <vocfile> <dataFile> <output.json>"%sys.argv[0])
		sys.exit(1)
	
	if not os.path.isfile(sys.argv[1]): 
		print("Data file %s not found"%(sys.argv[2]))
		sys.exit(1)
	voc = Vocabulary(sys.argv[1])

	if not os.path.isfile(sys.argv[2]): 
		print("Voc file %s not found"%(sys.argv[2]))
		sys.exit(1)
	rw = RewriterFromCSV(voc, sys.argv[2])
	fOut = open(sys.argv[3], "w+")
	result = compute(rw)
	result["desc"] = voc.getDescription()
	jsonOut = json.dumps(result)
	fOut.write(jsonOut)
	fOut.close()

	output = open(sys.argv[3], "w")
#	for part in voc.getPartitions()[:5]:
#		for partelt in part.getModalities():
#	nbPart = 2
#	t = [0 for _ in range(nbPart)]
#	partitions = voc.getPartitions()
#	for i in range(0,nbPart):#voc.getNbPartitions()):
#		for j in range(0,partitions[i].getNbModalities()):
#			t[i]=j
#			print(t)
