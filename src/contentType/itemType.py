from typing import Dict, Any, List

from srctools import Property

from contentType import BaseType


class ItemType( BaseType ):

	identifier: str
	authors: List[str]
	description: str
	icon: str
	instance: Dict[str, str]
	infoUrl: str
	tags: List[str]
	style: Dict[str, str]

	def __init__(
			self,
			identifier: str,
			style: Dict[str, str] = None
	):
		self.identifier = identifier
		self.style = { 'ANY_STYLE': f'ANY_' }

	def CountEntities( self ) -> int:
		pass

	def Serialize( self ) -> Dict[ str, Any ]:
		pass

	def GetInfoEntry( self ) -> Property:
		return Property(
			name='Item',
			value=[
				Property( name='ID', value=self.identifier),
				Property( name='unstyled', value='1' if len( self.style ) > 1 else '0' ),
				Property(
					name='Styles',
					value=[
						Property(name=key, value=value) for key, value in self.style.items()
					]
				)
			]
		)

	def GetPropertiesEntry( self ) -> Property:
		return Property(
			name='Properties',
			value=[
				Property( name='Authors', value=', '.join(self.authors) ),
				Property( name='Tags', value='; '.join(self.tags) ),
				Property( name='Description', value=[ Property( name='', value=line ) for line in self.description.splitlines() ] ),
				# all_name
				# all_icon
				Property( name='infoURL', value=self.infoUrl ),
				Property( name='Ent_count', value=str( self.CountEntities() ) ),
				Property( name='Icon', value=[ Property(name='0', value=self.icon) ] )
			]
		)
