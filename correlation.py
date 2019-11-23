import sys
from vocabulary import *
from rewriterFromCSV import *
from flight import Flight
from coverage import computeCoverage, normalizeCoverage, printCoverage

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python %s <vocfile> <dataFile>" % sys.argv[0])
		sys.exit(1)

	if not os.path.isfile(sys.argv[1]):
		print("Data file %s not found" % (sys.argv[2]))
		sys.exit(1)
	voc = Vocabulary(sys.argv[1])

	if not os.path.isfile(sys.argv[2]):
		print("Voc file %s not found" % (sys.argv[2]))
		sys.exit(1)
	rw = RewriterFromCSV(voc, sys.argv[2])

	correlations = dict()
	rw.open()
	flights = rw.readFlights()
	#	flights = map(lambda x:x.rewrite() ,flights)
	rw.close()

	filteredFlights = list(filter(lambda x: x.match([["DepDelay", "long"]], 0.999), flights))

	coverage = computeCoverage(filteredFlights)
	coverage = normalizeCoverage(coverage, voc)
	printCoverage(coverage, voc)
	print("%d filtered flights" % (len(filteredFlights)))

	# filteredFlights = map(lambda x: x.rewrite(), filteredFlights)

#	for part in voc.getPartitions()[:5]:
#		for partelt in part.getModalities():
#	nbPart = 2
#	t = [0 for _ in range(nbPart)]
#	partitions = voc.getPartitions()
#	for i in range(0,nbPart):#voc.getNbPartitions()):
#		for j in range(0,partitions[i].getNbModalities()):
#			t[i]=j
#			print(t)
