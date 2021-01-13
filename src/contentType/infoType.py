from pprint import pprint
from typing import List, Dict, Any

from srctools import Property

from contentType import BaseType
from contentType.itemType import ItemType


class InfoFile:

	name: str
	description: str
	dependencies: List[str] = None
	content: List[ BaseType ]
	identifier: str

	def __init__(self):
		pass

	def Serialize( self ) -> Property:

		serialized_data = Property(
			name=None,
			value=[
				Property(name='ID', value=self.identifier),
				Property( name='Name', value=self.name ),
				Property( name='Desc', value=self.description )
			]
		)
		if self.dependencies is not None:
			serialized_data += Property(
				name='Prerequisites',
				value=[ Property( name='Package', value=dep ) for dep in self.dependencies ]
			)

		for item in self.content:
			serialized_data += item.GetInfoEntry()

		return serialized_data


if __name__ == '__main__':
	info = InfoFile()
	info.name = 'Test'
	info.identifier = 'TEST_PACKAGE'
	info.description = 'A description'
	info.dependencies = None
	info.content = [ ItemType( identifier='TEST_PKG_ITM', folder='.') ]
	pprint( [ x for x in info.Serialize().export() ] )
