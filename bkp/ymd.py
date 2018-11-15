#! /usr/bin/python

import os
import re
import PIL.Image
import PIL.ExifTags
import pprint
import datetime
from perfile import PerFile


class YMD(PerFile):
	YMD = "YMD"
	patterns = [
		re.compile(r"VID_(....)(..)(..)_.*.mp4"),
		re.compile(r"IMG-(....)(..)(..)-WA.*.jpg"),
		re.compile(r"IMG_(....)(..)(..)_.*.jpg"),
		re.compile(r"MOD_(....)(..)(..)_.*"),
	]
	datepatterns = [
		re.compile(r".*\.MOV$"),
		re.compile(r".*\.png$"),
		re.compile(r".*\.gif$"),
		re.compile(r".*\.mp4$")
	]

	def __init__(self, yr, mn, dt):
		self.year = yr
		self.month = mn
		self.date = dt

	@staticmethod
	def getFromFileName( filename, root ):
		for pat in YMD.patterns:
			match = re.match(pat, filename)
			if (None == match):
				#print "Did not match : ", pat.pattern
				continue
			#print "Match: Pattern: ", pat.pattern
			return YMD( match.group(1), match.group(2), match.group(3) )
		for pat in YMD.datepatterns:
			match = re.match(pat, filename)
			if (None == match):
				#print "Did not match : ", pat.pattern
				continue
			#print "Match: Pattern: ", pat.pattern
			t=os.path.getmtime(os.path.join(root, filename))
			dt=datetime.datetime.fromtimestamp(t)
			return YMD( "%.4d" % dt.year, "%.2d" % dt.month, "%.2d" % dt.day)
		return None

	@staticmethod
	def getFromFileExif( filename ):
		try:
			img = PIL.Image.open(filename)
			exif_data = img._getexif()
		except Exception as e:
			print "Error getting Exif Data: ", filename, " - ", e
			return None
		if (None == exif_data):
			#print "No EXIF data"
			return None
		exif = {
			PIL.ExifTags.TAGS[k]: v
			for k, v in img._getexif().items()
			if k in PIL.ExifTags.TAGS
		}
		edt = None
		if ( 'DateTime' in exif ):
			edt = exif['DateTime']
		if ( None == edt ):
			if ( 'DateTimeOriginal' in exif ):
				edt = exif['DateTimeOriginal']
			else:
				return None
		#print edt
		match = re.match(r"(....):(..):(..) .*", edt)
		return YMD( match.group(1), match.group(2), match.group(3) )
		#print "===== %04d" % (exif['DateTime'].year) 

	@staticmethod
	def getYMD( root, file ):
		fullname = os.path.join(root, file)
		#print "File: ", file
		fnymd = YMD.getFromFileName( file, root )
		if (None != fnymd):
			#print( fnymd.year )
			return fnymd
			#pprint.pprint( fnymd )
		fnymd = YMD.getFromFileExif(fullname)
		#if (None != fnymd):
		#pprint.pprint( fnymd )
		#print( fnymd.month )
		return fnymd

	#def __str__(self):
		#print "" + self.year + self.month + self.date
	#	return "%s.%s.%s - %s(%r)" % (self.year, self.month, self.date, self.__class__, self.__dict__) #self.year + self.month + self.date
	def processFile(self, root, srcfile, context):
		#print "YMD"
		fullname = os.path.join(root, srcfile)
		context[YMD.YMD] = YMD.getYMD(root, srcfile)
