from pathlib import Path
from typing import List

import config
from contentType.Info import InfoFile
from contentType.Item import Item
from contentType.Style import Style


class Package:

	info: InfoFile
	items: List[ Item ]
	styles: List[ Style ]

	def __init__(self):
		self.info = InfoFile()
		self.items = []
		self.styles = []

	def GetItem( self, name: str ) -> Item:
		for item in self.items:
			if item.identifier == name:
				return item
