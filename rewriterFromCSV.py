#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
from vocabulary import *
from flight import Flight

class RewriterFromCSV(object):

	def __init__(self, voc, df):
		"""
		Translate a dataFile using a given vocabulary
		"""
		self.vocabulary = voc
		self.dataFile = df

	def open(self):
		try:
			self.source = open(self.dataFile, 'r')
			self.source.readline()#pass first line (column names)
		except:
			raise Exception("Error while loading the dataFile %s"%(self.dataFile))

	def readFlight(self):
		line = self.source.readline()
		if len(line) == 0:
			return None
		line = line.strip()
		while line == "" or line[0] == "#":
			line = self.source.readline()
			if len(line) == 0:
				return None
			line = line.strip()
		return Flight(line,self.vocabulary)

	def readFlights(self):
		flights = []
		line = self.source.readline()
		while line != "":
			line = line.strip()
			while line == "" or line[0] == "#":
				line = self.source.readline()
				if len(line) == 0:
					return flights
				line = line.strip()
			flights.append(Flight(line,self.vocabulary))
			line = self.source.readline()
		return flights

	def readLineAndRewrite(self):
		f = self.readFlight()
		if f:
			return f.rewrite()
		return None

	def close(self):
		self.source.close()



if __name__ == "__main__":
 	if len(sys.argv)  < 3:
 		print("Usage: python flight.py <vocfile> <dataFile>")
 	else:
 		if os.path.isfile(sys.argv[1]): 
 			voc = Vocabulary(sys.argv[1])
	 		if os.path.isfile(sys.argv[2]): 
	 			rw = RewriterFromCSV(voc, sys.argv[2])
	 			rw.readAndRewrite()
	 		else:
	 			print("Data file %s not found"%(sys.argv[2]))
	 	else:
	 		print("Voc file %s not found"%(sys.argv[2]))
