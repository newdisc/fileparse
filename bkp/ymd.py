#! /usr/bin/python

import os
import re
import PIL.Image
import PIL.ExifTags
import pprint


class YMD:
	patterns = [
		re.compile(r"VID_(....)(..)(..)_.*.mp4"),
		re.compile(r"IMG-(....)(..)(..)-WA.*.jpg"),
		re.compile(r"IMG_(....)(..)(..)_.*.jpg"),
		re.compile(r"MOD_(....)(..)(..)_.*"),
	]

	def __init__(self, yr, mn, dt):
		self.year = yr
		self.month = mn
		self.date = dt

	@staticmethod
	def getFromFileName( filename ):
		for pat in YMD.patterns:
			match = re.match(pat, filename)
			if (None == match):
				#print "Did not match : ", pat.pattern
				continue
			#print "Match: Pattern: ", pat.pattern
			return YMD( match.group(1), match.group(2), match.group(3) )
		return None

	@staticmethod
	def getFromFileExif( filename ):
		try:
			img = PIL.Image.open(filename)
			exif_data = img._getexif()
		except:
			return None;
		if (None == exif_data):
			#print "No EXIF data"
			return None;
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
		fnymd = YMD.getFromFileName( file )
		if (None != fnymd):
			#print( fnymd.year )
			return fnymd
			#pprint.pprint( fnymd )
		fnymd = YMD.getFromFileExif(fullname)
		#if (None != fnymd):
			#pprint.pprint( fnymd )
			#print( fnymd.month )
		return fnymd


