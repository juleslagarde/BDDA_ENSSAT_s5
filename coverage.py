import sys
from vocabulary import *
from rewriterFromCSV import *
from flight import Flight


def computeCoverage(flights):
	"""
	compute coverage on a list
	:param flights: list of Flight
	:return:
	"""
	n = 0
	N = len(flights[0].rewrite())
	sum_vector = [0 for _ in range(0, N)]
	for flight in flights:
		if n % 1000 == 0:
			print(n)
		rewrite = flight.rewrite()
		for i in range(0, N):
			sum_vector[i] += rewrite[i]
		n += 1
	return sum_vector


def computeCoverageLBL(rewriter):
	"""
	compute coverage line by line
	:param rewriter:
	:return:
	"""
	rw.open()
	rewrite = rewriter.readLineAndRewrite()
	N = len(rewrite)
	n = 0
	sum_vector = [0 for _ in range(0, N)]
	while rewrite:
		print(n)
		for i in range(0, N):
			sum_vector[i] += rewrite[i]
		rewrite = rewriter.readLineAndRewrite()
		n += 1
	rw.close()
	return sum_vector


def normalizeCoverage(coverage, voc):
	"""
	compute normalized coverage line by line
	:param rewriter:
	:return:
	"""
	i = 0
	for part in voc.getPartitions():
		num_modalities = part.getNbModalities()
		total_part = 0
		for m in range(0, num_modalities):
			total_part += coverage[i + m]
		if total_part != 0:
			for m in range(0, num_modalities):
				coverage[i + m] /= total_part
		i += num_modalities
	return coverage


def printCoverage(coverage, voc):
	i = 0
	for part in voc.getPartitions():
		for partelt in part.getModalities():
			print(part.getAttName() + " " + partelt.getName() + " : " + str(coverage[i]))
			i += 1


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python %s <vocfile> <dataFile>" % sys.argv[0])
	else:
		if os.path.isfile(sys.argv[1]):
			voc = Vocabulary(sys.argv[1])
			if os.path.isfile(sys.argv[2]):
				rw = RewriterFromCSV(voc, sys.argv[2])

				coverage = computeCoverageLBL(rw)
				coverage = normalizeCoverage(coverage, voc)
				printCoverage(coverage, voc)

			else:
				print("Data file %s not found" % (sys.argv[2]))
		else:
			print("Voc file %s not found" % (sys.argv[2]))
