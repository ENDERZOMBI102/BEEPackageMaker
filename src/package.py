from typing import List

from contentType.item import Item
from contentType.style import Style


class Package:
	# metadata
	name: str
	identifier: str
	description: str
	# components
	items: List[Item]
	styles: List[Style]

	def __init__( self, name: str ):
		self.name = name


