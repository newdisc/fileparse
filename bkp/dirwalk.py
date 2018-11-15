
import os
import sys
import time
from shutil import copy2, move

from perfile import PerFile

class DirWalk:
	def __init__(self, root, processors):
		self.root = root
		self.processors = processors

	@staticmethod
	def safecrdir(dname):
		if (False == os.path.isdir(dname)):
			print "Creating: ", dname
			os.makedirs(dname)

	def walkDir(self):
		i = 0
		allstart = time.clock()
		for root, dirs, srcfiles in os.walk(self.root):
			print "\n------------------------------------------", root
			start = time.clock()
			for srcfile in srcfiles:
				i = i+1
                                context = dict()
                                for processor in self.processors:
					processor.processFile(root, srcfile, context)
				sys.stdout.write('.')
				if (0 == i%10):
					sys.stdout.flush()
			print "\nTime for ", root, (time.clock() - start)
			sys.stdout.flush()
		print "\nTime for all: ", (time.clock() - allstart)

class EchoProcessor(PerFile):
	def processFile(self, root, filename, context):
		print "Process File: ", filename

if  __name__ == '__main__':
	shad = DirWalk(".", { EchoProcessor() })
	shad.detectDups(".")
#import re
	#print str(sys.argv[1])
	#shad.detectDups(sys.argv[1])
#		sha_re = re.compile(r"^(.*).sha256$")
#				if (re.match(sha_re, srcfile)):
#					continue
#				fullname = os.path.join(root, srcfile)
#				existName = self.isDup(fullname)
#				if None != existName:
#					print "\nDuplicate: ", fullname, " of ", existName
#					duproot = root.replace("backup/","dup/")
#					dupfn = os.path.join(duproot, srcfile)
					#DirWalksafecrdir(duproot)
#					if (not os.path.isfile(dupfn)):
#						print "\nMoving: ", fullname, " to ", dupfn
#						move(fullname, dupfn)
#					else:
#						print "\nExists: ", dupfn
