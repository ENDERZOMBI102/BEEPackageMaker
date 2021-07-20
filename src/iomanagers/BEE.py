from pathlib import Path

from iomanagers import AbstractIOManager
from package import Package


class BeeIOManager(AbstractIOManager):

	def Serialize( self, package: Package ):
		pass

	def Deserialize( self, package: Path ):
		pass
