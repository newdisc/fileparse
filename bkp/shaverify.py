
import hashlib
import re
import os
from shutil import copy2, move
from perfile import PerFile
from shadict import SHADict

class SHAVerify(PerFile):
	sha_re = re.compile(r"^(.*).sha256$")

	def processFile(self, root, srcfile, context):
		#print "\nShaVerify"
		if (re.match(SHADict.sha_re, srcfile)):
			return
		fullname = os.path.join(root, srcfile)
		shasum = SHADict.getShaAssoc(fullname)
		shaact = SHADict.calculateSha(fullname)
		if (shasum != shaact):
			print "\nSHA differ: ", fullname
			#print "SHA differ: \n", shasum, "\n", shaact
	
	def dummy(self, root, srcfile, context):
		fullname = os.path.join(root, srcfile)
		shasum = SHADict.getSha(fullname)
		existName = self.isDup(fullname, context)
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

