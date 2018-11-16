
import hashlib
import re
import os
from shutil import copy2, move
from perfile import PerFile
#from bkpnsha import BackupWithSha

class SHADict(PerFile):
	SHAEXT = ".sha256"
	SHASUM = "SHA256SUM"
	sha_re = re.compile(r"^(.*).sha256$")
	
	def __init__(self, baseroot, duplroot):
		self.shalkp = dict()
		self.baseroot = baseroot
		self.duplroot = duplroot
		if (None != self.duplroot):
			self.duplroot = self.duplroot + os.sep + "dup" #BackupWithSha.DUP
			SHADict.safecrdir(self.duplroot)

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
	def getShaAssoc( datafile ):
		shafiledata = None
		if ( os.path.isfile(datafile + SHADict.SHAEXT) ):
			with open(datafile + SHADict.SHAEXT, 'r') as myfile:
				shafiledata = myfile.read().replace('\n', '')
		return shafiledata

	@staticmethod
	def getSha( datafile ):
		shafiledata = SHADict.getShaAssoc(datafile)
		if (None != shafiledata):
			return shafiledata
		return SHADict.calculateSha( datafile )

	@staticmethod
	def writeSha(fname, shadig):
		with open(fname, "w") as text_file:
			text_file.write(shadig)

	def isDup(self, fullfilename, context):
		shasum = SHADict.getSha(fullfilename)
		if shasum in self.shalkp:
			return self.shalkp[shasum]
		else:
			context['SHA256SUM'] = shasum # sha256sum is set only when not a dup
			self.shalkp[shasum] = fullfilename
		return None

	def processFile(self, root, srcfile, context):
		#print "\nSHADict"
		if (re.match(SHADict.sha_re, srcfile)):
			return
		fullname = os.path.join(root, srcfile)
		existName = self.isDup(fullname, context)
		if None != existName:
			print "\nDuplicate: ", fullname, " of ", existName
		if ( None != existName and None != self.duplroot):
			duproot = root.replace(self.baseroot,self.duplroot)
			dupfn = os.path.join(duproot, srcfile)
			SHADict.safecrdir(duproot)
			if (not os.path.isfile(dupfn) and os.access(duproot, os.W_OK) ):
				#print "\nMoving: ", fullname, " to ", dupfn
				move(fullname, dupfn)
			else:
				print "\nExists: ", dupfn

