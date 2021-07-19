from abc import ABCMeta, abstractmethod
from pathlib import Path

from package import Package


class AbstractIOManager(meta=ABCMeta):

	@abstractmethod
	def Serialize( self, package: Package ):
		pass

	@abstractmethod
	def Deserialize( self, package: Path ):
		pass
