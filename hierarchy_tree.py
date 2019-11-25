import sys
from collections import OrderedDict
from typing import List

from vocabulary import *
from rewriterFromCSV import *
from flight import Flight
import json


def printN(n, i):
	pass


def countCategory(rw, partOrder):
	rw.open()
	flight = rw.readFlight()
	n = 0
	counter = dict()
	while flight:
		categ = flight.categorise(partOrder)
		if categ in counter:
			counter[categ] += 1
		else:
			counter[categ] = 1
		flight = rw.readFlight()
		n += 1
		if n % 100000 == 0:
			print(n)
	rw.close()
	return counter


def convertToHierarchy(counts: dict, voc: Vocabulary, partOrder: List[str]) -> dict:
	counts = sorted(counts.items(), key=lambda x: x[0])
	children = "children"
	tree = {"name": "US Flights (2008)", children: []}
	for cat, val in counts:
		node = tree
		assert len(cat) == len(partOrder)
		for i, num in zip(range(len(cat)), cat):
			partName = partOrder[i]
			modName = voc.getPartition(partName).getModNames()[int(num)]
			nodeName = partName + "=" + modName
			lastChild = None
			if len(node[children]) > 0:
				lastChild = node[children][len(node[children]) - 1]
				if lastChild["name"] == nodeName:
					nextNode = lastChild
				else:
					nextNode = {"name": nodeName, children: []}
					node[children].append(nextNode)
			else:
				nextNode = {"name": nodeName, children: []}
				node[children].append(nextNode)
			node = nextNode
		node["value"] = val
	return tree


def getHierarchyTree(voc, dataFileName, partOrder):
	if partOrder is None:
		partOrder = ['Origin', 'Dest', 'DayOfWeek', 'DepTime', 'ArrTime', 'AirTime', 'ArrDelay', 'DepDelay', 'Distance',
					 'Month', 'DayOfMonth']
	if dataFileName is None:
		dataFileName = "2008short.csv"
	rw = RewriterFromCSV(voc, "Data/" + dataFileName)
	result = countCategory(rw, partOrder)
	# result["desc"] = voc.getDescription()
	result = convertToHierarchy(result, voc, partOrder)
	return result


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Usage: python %s <vocfile> <dataFile> <output.json>" % sys.argv[0])
		sys.exit(1)

	if not os.path.isfile(sys.argv[1]):
		print("Data file %s not found" % (sys.argv[2]))
		sys.exit(1)
	voc = Vocabulary(sys.argv[1])

	if not os.path.isfile(sys.argv[2]):
		print("Voc file %s not found" % (sys.argv[2]))
		sys.exit(1)

	partOrder = ['Origin', 'Dest', 'DayOfWeek', 'DepTime', 'ArrTime', 'AirTime', 'ArrDelay', 'DepDelay', 'Distance',
				 'Month', 'DayOfMonth']
	print(partOrder)
	fOut = open(sys.argv[3], "w+")
	jsonOut = getHierarchyTree(voc, partOrder)
	# print(jsonOut)
	fOut.write(jsonOut)
	fOut.close()

#	for part in voc.getPartitions()[:5]:
#		for partelt in part.getModalities():
#	nbPart = 2
#	t = [0 for _ in range(nbPart)]
#	partitions = voc.getPartitions()
#	for i in range(0,nbPart):#voc.getNbPartitions()):
#		for j in range(0,partitions[i].getNbModalities()):
#			t[i]=j
#			print(t)
