
import hashlib
import re
import os
from shutil import copy2, move
from perfile import PerFile
from shadict import SHADict
from ymd import YMD

class BackupWithSha(PerFile):
	DUP = "dup"
	JNK = "junk"
	DOC = "doc"
	PRC = "proc"
	sha_re = re.compile(r".*.sha256")
	vid_re = re.compile(r"\.mkv$|\.mp4$|\.THM$|\.avi$|\.MOV$")
	doc_re = None
	dup_re = None
	junk_re = None

	def __init__(self, baseroot, duplroot, procroot):
		self.baseroot = baseroot
		self.duplroot = duplroot
		self.procroot = procroot
		if (None != self.procroot):
			self.procroot = os.path.join(self.procroot, BackupWithSha.PRC)
		if ( r"/" == os.sep): # Unix
			BackupWithSha.doc_re = re.compile(os.sep + BackupWithSha.DOC + os.sep)
			BackupWithSha.dup_re = re.compile(os.sep + BackupWithSha.DUP + os.sep)
			BackupWithSha.junk_re = re.compile(os.sep + BackupWithSha.JNK + os.sep)
		else: 
			BackupWithSha.doc_re = re.compile(r"\\" + BackupWithSha.DOC + r"\\")
			BackupWithSha.dup_re = re.compile(r"\\" + BackupWithSha.DUP + r"\\")
			BackupWithSha.junk_re = re.compile(r"\\" + BackupWithSha.JNK + r"\\")
	
	def getBackupFolder(self, root, srcfile, context):
		ymd = context[YMD.YMD]
		dtype = "backup"
		if ( re.search(BackupWithSha.vid_re, srcfile) ):
			dtype = "vid"
		if ( re.search(BackupWithSha.doc_re, root) ):
			dtype = BackupWithSha.DOC
		if ( re.search(BackupWithSha.dup_re, root) ):
			dtype = BackupWithSha.DUP
		if ( re.search(BackupWithSha.junk_re, root) ):
			dtype = BackupWithSha.JNK
		#destdfull = os.path.join(destdir, dtype, fnymd.year, fnymd.month)
		bkproot = os.path.join(self.duplroot, dtype, ymd.year, ymd.month)
		return bkproot


	def processFile(self, root, srcfile, context):
		#print "\nBackkupWithSha"
		if (re.match(SHADict.sha_re, srcfile)):
			return
		if (SHADict.SHASUM not in context):
			return # A duplicate, ignore
		fullname = os.path.join(root, srcfile)
		if (YMD.YMD not in context or None == context[YMD.YMD]):
			print "Could not determine date of file :", fullname
			return # Date could not be determined. Skip file
		#print context[YMD.YMD]
		bkproot = self.getBackupFolder(root, srcfile, context)
		bkpfn = os.path.join(bkproot, srcfile)
		bkpfnsha = bkpfn + SHADict.SHAEXT
		bkpsha = SHADict.getSha(bkpfn)
		shasum = SHADict.getSha(fullname)
		if (bkpsha == None):
			print "Backing up file: ", fullname, " to ", bkpfn
			SHADict.safecrdir(bkproot)
			SHADict.writeSha(bkpfnsha, shasum)
		if (bkpsha == None and False == os.path.isfile(bkpfn)):
			print "Copying ", fullname
			copy2(fullname, bkpfn)
		if (bkpsha != None and bkpsha != shasum):
			print "Non matching shasums - please check : ", fullname, " to ", bkpfn
			return
		if (None == self.procroot):
			return
		prcroot = root.replace(self.baseroot,self.procroot)
		prcfn = os.path.join(prcroot, srcfile)
		if (not os.path.isfile(prcfn) and os.access(self.procroot, os.W_OK) ):
			print "\nMoving (processed): ", fullname, " to ", prcfn
			SHADict.safecrdir(prcroot)
			move(fullname, prcfn)
		else:
			print "\nNon-Writeable: ", prcfn
	
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

#python bkpmain.py -s E:\archive\tst -d E:\archive\tstnew -m E:\archive\tstnew\prc
