
import abc

class PerFile(object):
	__metaclass__ = abc.ABCMeta
	@abc.abstractmethod
	def processFile(self, root, filename, context):
		pass
