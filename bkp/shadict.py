#! /usr/bin/python

from ymd import YMD
import hashlib
import re
from shutil import copy2, move

class SHADict:
	def __init__(self):
		self.shalkp = dict()

	@staticmethod
	def calculateSha( filename ):
		if ( not os.path.isfile(filename) ):
			return None
		shafiledata = None
		BLOCKSIZE = 65536
		hasher = hashlib.sha256()
		with open(filename, 'rb') as afile:
			buf = afile.read(BLOCKSIZE)
			while len(buf) > 0:
				hasher.update(buf)
				buf = afile.read(BLOCKSIZE)
		return hasher.hexdigest()

	@staticmethod
	def getSha( datafile ):
		shafiledata = None
		if ( os.path.isfile(datafile + ".sha256") ):
			with open(datafile + ".sha256", 'r') as myfile:
				shafiledata = myfile.read().replace('\n', '')
			return shafiledata
		return SHADict.calculateSha( datafile )

	def isDup(self, fullfilename):
		shasum = SHADict.getSha(fullfilename)
		if shasum in self.shalkp:
			return self.shalkp[shasum]
		else:
			self.shalkp[shasum] = fullfilename
		return None

	@staticmethod
	def safecrdir(dname):
		if (False == os.path.isdir(dname)):
			print "Creating: ", dname
			os.makedirs(dname)



	def detectDups(self, directory):
		sha_re = re.compile(r"^(.*).sha256$");
		i = 0
		for root, dirs, srcfiles in os.walk(directory):
			print "\n------------------------------------------"
			start = time.clock()
			for srcfile in srcfiles:
				if (re.match(sha_re, srcfile)):
					continue
				i = i+1
				fullname = os.path.join(root, srcfile)
				existName = self.isDup(fullname)
				if None != existName:
					print "\nDuplicate: ", fullname, " of ", existName
					duproot = root.replace("backup/","dup/")
					dupfn = os.path.join(duproot, srcfile)
					SHADict.safecrdir(duproot)
					if (not os.path.isfile(dupfn)):
						print "\nMoving: ", fullname, " to ", dupfn
						move(fullname, dupfn)
					else:
						print "\nExists: ", dupfn

if  __name__ == '__main__':
	import sys
	import os
	import time
	shad = SHADict()
	#shad.detectDups()
	print str(sys.argv[1])
	shad.detectDups(sys.argv[1])

