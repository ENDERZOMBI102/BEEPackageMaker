from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Literal


managerType = Literal['BEE', 'Baguettery', 'Saismee']


class AbstractIOManager(metaclass=ABCMeta):

	@abstractmethod
	def Serialize( self, package: 'Package' ) -> None:
		pass

	@abstractmethod
	def Deserialize( self, package: Path ) -> None:
		pass
