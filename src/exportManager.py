from typing import Dict

from abstract.manager import AbstractManager
from iomanagers import managerType, AbstractIOManager


class ExportManager(AbstractManager):

	managers: Dict[managerType, AbstractIOManager]

	def Init( self ) -> None:
		from iomanagers.BEE import BeeIOManager
		self.managers = dict( BEE=BeeIOManager() )

	def Stop( self ) -> None:
		pass

	def Export( self ) -> None:
		pass


manager: ExportManager = ExportManager()
