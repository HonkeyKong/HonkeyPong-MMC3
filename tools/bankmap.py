#!/usr/bin/python

# bankmap.py - Ophis Label Assembly Generator
# Copyright 2015 Ryan D. Souders (HonkeyKong), All Rights Reserved.
# Generates Ophis-compatible assembly code from map files,
# exported at assemble-time using the -m switch in Ophis, shown below.
# ophis sourcefile.oph -m sourcefile.map
# The resulting .oph file can then be included in your programs
# to allow addressing of code and data in swappable program banks
# without the need to manually track the offsets of said code and data.
# This is intended for use in software written for systems that use 
# memory-mapping hardware, such as the Nintendo Entertainment System.

import sys, os, time

class load():

	mapFile = None
	mapSrc = None
	
	def __init__(self, fileName):
		self.mapFile = open(fileName, 'r')
		
	def writeASM(self):
		self.mapSrc = open("%s.oph" % self.mapFile.name, 'w')
		mapDict = {}
		self.mapSrc.write("; Auto-generated at %s\n\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
		for line in self.mapFile.readlines():
			if (not "*" in line): # discard anonymous labels, they'll only fuck things up.
				maplabel = line.split('|')[:2]
				mapDict[str(maplabel[1]).strip(' ')] = str(maplabel[0]).strip(' ')
		for key in mapDict:
			self.mapSrc.write(".alias %s %s\n" % (key, mapDict[key]))
		self.mapSrc.close()
		if(quietMode == False):
			print "Source map written to %s" % self.mapSrc.name

	def __exit__(self):
		self.mapFile.close()
#end map class 

if __name__ == "__main__":

	quietMode = False

	if (len(sys.argv) < 2):
		print "Usage: bankmap.py mapFile [options]"
		print "Generates Ophis-compatible assembly code from exported label maps generated at assemble-time with '-m outputFile' switch."
		print "Options:"
		print "-q or --quiet: Suppresses log messages."

	elif (len(sys.argv) >= 2):
		for arg in sys.argv:
			if (arg == "--quiet") or (arg == "-q"):
				quietMode = True
		srcMap = load(sys.argv[1])
		srcMap.writeASM()