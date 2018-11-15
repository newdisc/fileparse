
from dirwalk import DirWalk, EchoProcessor
from shadict import SHADict
from shaverify import SHAVerify
from ymd import YMD
from bkpnsha import BackupWithSha
import sys
import os
import argparse

parser = argparse.ArgumentParser(description="Backup files @Source into Time Ordered @Destination")
parser.add_argument("-s", "--source", help="Source Directory", required=True)
parser.add_argument("-d", "--destination", help="Source Directory", default=os.getcwd())
parser.add_argument("--verify", help="Verify checksums", required=False, default=False, action='store_true')
parser.add_argument("-m", "--move", help="Move on backup dir", required=False, default=None)
args = parser.parse_args()

print "Backing up ", args.source, " at ", args.destination, " and verifying ", args.verify, " and moving " , args.move


if  __name__ == '__main__':
	shad = DirWalk(args.source, 
		[ YMD("YYYY","MM","DT")
		  ,SHADict(args.source, args.move)
		  #,SHAVerify() # only run when no source specified 
		  ,BackupWithSha(args.source, args.destination, args.move)
		  ,EchoProcessor()
		])
	shad.walkDir()
