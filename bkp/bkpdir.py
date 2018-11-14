#! /usr/bin/python

import argparse
import os
import re
import PIL.Image
import PIL.ExifTags
import hashlib
import pprint
from ymd import YMD
import sys
import time
from shutil import copy2, move

def getSha( filename, forcecalc ):
	shafiledata = None
	if ( not(forcecalc) and os.path.isfile(filename + ".sha256") ):
		with open(filename + ".sha256", 'r') as myfile:
			shafiledata = myfile.read().replace('\n', '')
		return shafiledata
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

def verifySha(basedir):
	i=0
	sha_re = re.compile(r".*.sha256");
	allstart = time.clock()
	for root, dirs, files in os.walk(basedir):
		print "\n------------------------------------------"
		start = time.clock()
		#print "Dirs: ", dirs
		#print "Files: ", files
		for file in files:
			i = i+1
			if re.match(sha_re, file):
				#print "Shasum file"
				#sys.stdout.write('i')
				#print "i"
				continue
			fullname = os.path.join(root, file)
			shaname = fullname + ".sha256"
			shafiledata = None
			if ( os.path.isfile(shaname) ):
				with open(shaname, 'r') as myfile:
					shafiledata = myfile.read().replace('\n', '')
			else:
				sys.stdout.write('!')
				#print "!"
				continue
			shasm = getSha(fullname, True)
			if (shafiledata != shasm):
				print "<>", fullname
				sys.stdout.write('<>')
			sys.stdout.write('.')
			if (0 == i%10):
				sys.stdout.flush()
		#your code here    
		print "\nRoot: ", root, " took ", (time.clock() - start)
		sys.stdout.flush()
	print "\nAll: ", root, " took ", (time.clock() - allstart)

def writeSha(fname, shadig):
	with open(fname, "w") as text_file:
		text_file.write(shadig)

def bkpSD(srcdir, destdir, procmove):
	i=0
	sha_re = re.compile(r".*.sha256");
	doc_re = re.compile(os.sep + r"doc" + os.sep)
	dup_re = re.compile(os.sep + r"dup" + os.sep)
	junk_re = re.compile(os.sep + r"junk" + os.sep)
	vid_re = re.compile(r"\.mkv$|\.mp4$|\.THM$|\.avi$|\.MOV$")
	allstart = time.clock()
	for root, dirs, files in os.walk(srcdir):
		print "\n------------------------------------------"
		start = time.clock()
		#print "Dirs: ", dirs
		#print "Files: ", files
		for srcfile in files:
			i = i+1
			srcfulln = os.path.join(root, srcfile)
			#print srcfulln
			if re.match(sha_re, srcfile):
				#print "Shasum file"
				#sys.stdout.write('i')
				#print "i"
				continue
			fnymd = YMD.getYMD(root, srcfile)
			if ( None == fnymd ): 
				print "\nCould not determine file date ", srcfulln
				continue
			dtype = "backup"
			if ( re.search(vid_re, srcfile) ):
				dtype = "vid"
			if ( re.search(doc_re, root) ):
				dtype = "doc"
			if ( re.search(dup_re, root) ):
				dtype = "dup"
			if ( re.search(junk_re, root) ):
				dtype = "junk"
			destdfull = os.path.join(destdir, dtype, fnymd.year, fnymd.month)
			safecrdir(destdfull)
			destfile = os.path.join(destdfull, srcfile)
			destshaname = destfile + ".sha256"
			shasm = getSha(srcfulln, False)
			shafiledata = getSha(destfile, False);#shasm
                        shamatch = True
			if (None != shafiledata and shafiledata != shasm):
				shamatch = False
			if ( not os.path.isfile(destshaname) ):
				print "Creating sha256 file", destshaname
				writeSha(destshaname, shasm)
                        if (None != procmove and shamatch and not(os.path.isfile(os.path.join(procmove, "processed", srcfile))) ):
				print "Moving ", srcfulln
				move(srcfulln,os.path.join(procmove, "processed"))
			if (not shamatch):
				print "<>", srcfulln
				sys.stdout.write('<>')
				continue #Do NOT copy / overwrite file
			if ( False == os.path.isfile(destfile) and None == shafiledata ): #Only shafile prevents copying - preserving dup/junk classifies
				print "Copying ", srcfulln
				copy2(srcfulln, destfile)
			sys.stdout.write('.')
			if (0 == i%10):
				sys.stdout.flush()
			#if (1<=i):
			#	break;
		#your code here    
		print "\nRoot: ", root, " took ", (time.clock() - start)
		sys.stdout.flush()
		#if (1<=i):
		#	break;
	print "\nAllSrc: ", srcdir, " took ", (time.clock() - allstart)

parser = argparse.ArgumentParser(description="Backup files @Source into Time Ordered @Destination")
parser.add_argument("-s", "--source", help="Source Directory", required=True)
parser.add_argument("-d", "--destination", help="Source Directory", default=os.getcwd())
parser.add_argument("--verify", help="Verify checksums", required=False, default=False, action='store_true')
parser.add_argument("-m", "--move", help="Move on backup dir", required=False, default=None)
args = parser.parse_args()

print "Backing up ", args.source, " at ", args.destination, " and verifying ", args.verify, " and moving " , args.move

#my $pat = "IMG-(2018)(04)(15)-WA0065.jpg";#"IMG_(2018)(06)(09)_200728.jpg";
# os.path.getmtime(path)

def safecrdir(dname):
	if (False == os.path.isdir(dname)):
		print "Creating: ", dname
		os.makedirs(dname)
	#else:
		#print "Exists: ", dname

if (args.verify):
	verifySha(args.destination)
	print "Done Verification"
	exit(0)

safecrdir(os.path.join(args.destination, "backup"))
safecrdir(os.path.join(args.destination, "doc"))
safecrdir(os.path.join(args.destination, "dup"))
safecrdir(os.path.join(args.destination, "junk"))
safecrdir(os.path.join(args.destination, "vid"))

if (args.move):
	safecrdir(os.path.join(args.move, "processed"))
        

bkpSD(args.source, args.destination, args.move)

#exit(0)

#i=0
#sha_re = re.compile(r".*.sha256");
#for root, dirs, files in os.walk(args.source):
#	print "------------------------------------------"
#	print "Root: ", root
	#print "Dirs: ", dirs
	#print "Files: ", files
#	for file in files:
#		if re.match(sha_re, file):
#			print "Shasum file"
#			continue
#		fullname = os.path.join(root, file)
#		shaname = fullname + ".sha256"
#		shafiledata = None
#		if ( os.path.isfile(shaname) ):
#			with open(shaname, 'r') as myfile:
#				shafiledata = myfile.read().replace('\n', '')
#		fnymd = None #YMD.getYMD(root, file)
#		if (None == fnymd):
			#pprint.pprint( fnymd )
#			print "Did NOT find Date/Month/Year"
#		print "ShaSum : ", getSha(fullname)
#		if (None != shafiledata):
#			print "ShaOrig: ", shafiledata
#		if (None != fnymd):
#			i = i+1
#		if (1<=i):
#			break
#	if (1<=i):
#		break


#with open('data.txt', 'r') as myfile:
#    data=myfile.read().replace('\n', '')
#		for pat in YMD.patterns:
#			match = re.match(pat, file)
#			if (None == match):
#				#print "Did not match : ", pat.pattern
#				continue
#			print "Match: Pattern: ", pat.pattern
#			img = PIL.Image.open(os.path.join(root, file))
#			exif_data = img._getexif()
#			if (None == exif_data):
#				print "No EXIF data"
#				break;
#			i = i+1
#			exif = {
#				PIL.ExifTags.TAGS[k]: v
#				for k, v in img._getexif().items()
#				if k in PIL.ExifTags.TAGS
#			}
#			print exif['DateTime']
#			#print "+++++ %04d" % (exif['DateTime'].year) 
#			print "ShaSum : ", getSha(os.path.join(root, file))
