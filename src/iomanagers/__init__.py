from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Literal

from package import Package


managerType = Literal['BEE', 'Baguettery', 'Saismee']


class AbstractIOManager(meta=ABCMeta):

	@abstractmethod
	def Serialize( self, package: Package ) -> None:
		pass

	@abstractmethod
	def Deserialize( self, package: Path ) -> None:
		pass
