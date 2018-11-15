
from dirwalk import DirWalk, EchoProcessor
from shadict import SHADict
import sys

if  __name__ == '__main__':
	shad = DirWalk(sys.argv[1], {SHADict(sys.argv[1], sys.argv[2]), EchoProcessor()})
	shad.walkDir()
