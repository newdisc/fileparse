
import hashlib
import re
import os
from shutil import copy2, move
from perfile import PerFile

class SHADict(PerFile):
	sha_re = re.compile(r"^(.*).sha256$")
	
	def __init__(self, baseroot, duplroot):
		self.shalkp = dict()
		self.baseroot = baseroot
		self.duplroot = duplroot

	@staticmethod
	def safecrdir(dname):
		if (False == os.path.isdir(dname)):
			print "Creating: ", dname
			os.makedirs(dname)

	@staticmethod
	def calculateSha( filename ):
		if ( not os.path.isfile(filename) ):
			return None
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

	def processFile(self, root, srcfile, context):
		if (re.match(SHADict.sha_re, srcfile)):
			return
		fullname = os.path.join(root, srcfile)
		existName = self.isDup(fullname)
		if None != existName:
			print "\nDuplicate: ", fullname, " of ", existName
			duproot = root.replace(self.baseroot,self.duplroot)
			dupfn = os.path.join(duproot, srcfile)
			SHADict.safecrdir(duproot)
			if (not os.path.isfile(dupfn)):
				print "\nMoving: ", fullname, " to ", dupfn
				move(fullname, dupfn)
			else:
				print "\nExists: ", dupfn

