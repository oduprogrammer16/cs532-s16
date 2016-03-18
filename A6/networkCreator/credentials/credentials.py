
from abc import ABCMeta, abstractmethod


class Credentials:
	"""Base class for a set of credentials for an api.
	"""
	__metaclass__ = ABCMeta


	@abstractmethod
	def read_configuration_file(self,configurationFileName,**arguments):
		"""Reads the configueration file.
		Args:
			configurationFileName: the name of the configueration file.
			arguments: Any number of arguments needed in the class 
		"""
		pass

	@abstractmethod
	def __str__(self):
		"""Creates a string based on the configration.
		"""
		pass

	@abstractmethod
	def write_to_configuration_file(self,fileName,format):
		"""Writes data to a configuration file. 
		Args: 
			fileName: theName of the file. 
			format: How the data should be written.
		"""
		pass