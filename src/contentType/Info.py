from pprint import pprint
from typing import List, Dict, Any

from srctools import Property

from contentType import BaseType
from contentType.Item import Item


class InfoFile:

	name: str
	description: str
	dependencies: List[str] = None
	identifier: str

	def __init__(self):
		self.name = 'Test'
		self.identifier = 'TEST_PACKAGE'
		self.description = 'A description'
		self.dependencies = None

	def Serialize( self, contents: List[ BaseType ] ) -> Property:

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

		for item in contents:
			serialized_data += item.GetInfoEntry()

		return serialized_data


if __name__ == '__main__':
	info = InfoFile()
	info.name = 'Test'
	info.identifier = 'TEST_PACKAGE'
	info.description = 'A description'
	info.dependencies = None
	pprint( [ x for x in info.Serialize( [ Item( identifier='TEST_PKG_ITM' ) ] ).export() ] )
