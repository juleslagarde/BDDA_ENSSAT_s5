import sys
from vocabulary import *
from rewriterFromCSV import *
from flight import Flight
from coverage import computeCoverage, printCoverage, prettifyCoverage


def assoc(v, flights):
	filteredFlights = list(filter(lambda x: x.match(v, 0), flights))
	cover1 = computeCoverage(filteredFlights)
	cover2 = computeCoverage(flights)
	dep = []
	for x, y in zip(cover1, cover2):
		if y != 0 and x != 0:
			dep.append(0 if x / y <= 1 else 1 - y / x)
		else:
			dep.append(0)
	return dep


def distance(v1, v2, voc: Vocabulary):
	"""
	un terme est un tuple dont le 1er élément est le nom de la partition et le 2ème le nom de la modalité
	:param v1: un terme
	:param v2: un autre terme
	:param voc: le vocabulaire permettant d'interprété les termes
	:return:
	"""
	assert v1[0] == v2[0]
	part = voc.getPartition(v1[0])
	modNames = part.getModNames()
	i1, i2 = modNames.index(v1[1]), modNames.index(v2[1])
	assert i1 != -1 and i2 != -1
	N = len(modNames)
	if part.loop:
		max = int(N / 2)
		dist = abs(i1 - i2) / max
		if dist > 1:
			i1, i2 = (i1 - max) % N, (i2 - max) % N  # rotation
			dist = abs(i1 - i2) / max
			assert dist <= 1
		return dist
	else:
		return abs(i1 - i2) / (N - 1)


def searchAtypical(v, flights, voc: Vocabulary):
	partName, m1 = v
	maxMod = ""
	maxVal = 0
	cover = computeCoverage(flights, [partName])
	modNames = voc.getPartition(partName).getModNames()
	i1 = modNames.index(m1)
	assert i1 != -1
	for m2 in modNames:
		i2 = modNames.index(m2)
		val = min(distance(v, (partName, m2), voc), cover[i2], 1-cover[i1])
		if val >= maxVal:
			maxVal = val
			maxMod = m2
	return maxMod, maxVal


def getAssociativity(voc, dataFileName=None, filter=None):
	if filter is None:
		filter = ["DepDelay", "long"]
	if dataFileName is None:
		dataFileName = "2008short.csv"
	rw = RewriterFromCSV(voc, "Data/"+dataFileName)
	rw.open()
	flights = rw.readFlights()
	#	flights = map(lambda x:x.rewrite() ,flights)
	rw.close()
	# test atypical
	# for part in voc.getPartitions():
	# 	partName = part.getAttName()
	# 	for modName in part.getModNames():
	# 		print("atypical(%s, %s) = %s" % (
	# 			partName, modName, searchAtypical((partName, modName), flights, voc)))
	# sys.exit(1)
	assoc1 = assoc([filter], flights)
	assoc1 = prettifyCoverage(assoc1, voc)
	modName, value = searchAtypical(filter, flights, voc)
	atypic = {"name": filter[0] + " : " + modName, "value": value}
	return {"assoc": assoc1, "atypic": atypic}


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python %s <vocfile> <dataFile>" % sys.argv[0])
		sys.exit(1)

	if not os.path.isfile(sys.argv[1]):
		print("Voc file %s not found" % (sys.argv[2]))
		sys.exit(1)
	voc = Vocabulary(sys.argv[1])

	# test distance
	# for part in voc.getPartitions():
	# 	partName = part.getAttName()
	# 	for modName1 in part.getModNames():
	# 		for modName2 in part.getModNames():
	# 			print("%s : dist(%s, %s) = %s" % (
	# 			partName, modName1, modName2, distance((partName, modName1), (partName, modName2), voc)))
	# sys.exit(1)


	if not os.path.isfile("Data/"+sys.argv[2]):
		print("Data file %s not found" % (sys.argv[2]))
		sys.exit(1)

	print(getAssociativity(voc, sys.argv[2], None))
