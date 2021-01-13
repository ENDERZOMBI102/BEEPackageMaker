from typing import Any, Dict

from srctools import Property


class BaseType:

	def Serialize( self ) -> Dict[str, Any]:
		pass

	def GetInfoEntry( self ) -> Property:
		pass
