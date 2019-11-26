import sys
from vocabulary import *
from rewriterFromCSV import *
from flight import Flight


def computeCoverage(flights, partitions=None):
	"""
	compute coverage on a list
	:param flights: list of Flight
	:return:
	"""
	n = 0
	N = len(flights[0].rewrite(partitions))
	sum_vector = [0 for _ in range(0, N)]
	for flight in flights:
		# if n % 1000 == 0:
		# 	print(n)
		rewrite = flight.rewrite(partitions)
		for i in range(0, N):
			sum_vector[i] += rewrite[i]
		n += 1
	return list(map(lambda x: x/len(flights), sum_vector))


# def computeCoverageLBL(rewriter):
# 	"""
# 	compute coverage line by line
# 	:param rewriter:
# 	:return:
# 	"""
# 	rw.open()
# 	rewrite = rewriter.readLineAndRewrite()
# 	N = len(rewrite)
# 	n = 0
# 	sum_vector = [0 for _ in range(0, N)]
# 	while rewrite:
# 		print(n)
# 		for i in range(0, N):
# 			sum_vector[i] += rewrite[i]
# 		rewrite = rewriter.readLineAndRewrite()
# 		n += 1
# 	rw.close()
# 	return sum_vector / n # divide each value by n



# def normalizeCoverageReal(coverage, voc):
# 	"""
# 	compute normalized coverage line by line
# 	:param rewriter:
# 	:return:
# 	"""
# 	i = 0
# 	for part in voc.getPartitions():
# 		num_modalities = part.getNbModalities()
# 		total_part = 0
# 		for m in range(0, num_modalities):
# 			total_part += coverage[i + m]
# 		if total_part != 0:
# 			for m in range(0, num_modalities):
# 				coverage[i + m] /= total_part
# 		i += num_modalities
# 	return coverage


def printCoverage(coverage, voc, partitions=None):
	if partitions is None:
		partitions = voc.getPartitions()
	else:
		partitions = list(map(lambda x: voc.getPartition(x), partitions))

	i = 0
	for part in partitions:
		for modName in part.getModNames():
			print(part.getAttName() + " " + modName + " : " + str(coverage[i]))
			i += 1


def prettifyCoverage(coverage, voc, partitions=None):
	if partitions is None:
		partitions = voc.getPartitions()
	else:
		partitions = list(map(lambda x: voc.getPartition(x), partitions))
	coverageP = []
	i = 0
	for part in partitions:
		for modName in part.getModNames():
			coverageP.append({"name": part.getAttName() + " : " + modName, "value": coverage[i]})
			i += 1
	return coverageP


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python %s <vocfile> <dataFile>" % sys.argv[0])
	else:
		if not os.path.isfile(sys.argv[1]):
			print("Voc file %s not found" % (sys.argv[2]))
			sys.exit(1)
		voc = Vocabulary(sys.argv[1])

		if not os.path.isfile(sys.argv[2]):
			print("Data file %s not found" % (sys.argv[2]))
			sys.exit(1)

		rw = RewriterFromCSV(voc, sys.argv[2])

		coverage = computeCoverage(rw)
		printCoverage(coverage, voc)
