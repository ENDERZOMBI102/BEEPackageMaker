from typing import List

from contentType.Info import Info
from contentType.Item import Item
from contentType.Style import Style

class Package:

	info: Info
	items: List[ Item ]
	styles: List[ Style ]

	def __init__(self):
		pass
		
	def ExportToBaguettery(self):
		pass
		
	def ExportToSaismee(self):
		pass
		
	def ExportToPackage(self):
		pass
	
	
	@staticmethod
	def ImportFromBaguettery():
		pass
		
	@staticmethod
	def ImportFromSaismee():
		pass
		
	@staticmethod
	def ImportFromFinalPackage():
		pass