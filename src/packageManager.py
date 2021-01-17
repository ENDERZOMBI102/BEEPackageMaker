from pathlib import Path
from typing import List, Dict, Any

import config
from contentType.Package import Package


class PackageManager:

	instance: 'PackageManager'
	package: Package
	packageList: List[Package]

	def __init__(self):
		self.package = Package()

	def ExportToBaguettery( self ) -> None:
		folder = Path( f'{config.load( "exportedPackagesDir" )}/{self.package.info.name}_bag' )
		folder.mkdir( exist_ok=True )

	def ExportToSaismee( self ) -> None:
		folder = Path( f'{config.load( "exportedPackagesDir" )}/{self.package.info.name}_sai' )
		folder.mkdir( exist_ok=True )

	def ExportToPackage( self ) -> None:
		folder = Path( f'{config.load( "exportedPackagesDir" )}/{self.package.info.name}_bee' )
		folder.mkdir( exist_ok=True )

	def ExportToPackageOld( self ) -> None:
		folder = Path( f'{config.load( "exportedPackagesDir" )}/{self.package.info.name}_b36' )
		folder.mkdir( exist_ok=True )

	def ImportFromBaguettery( self ) -> None:
		pass

	def ImportFromSaismee( self ) -> None:
		pass

	def ImportFromPackage( self ) -> None:
		pass

	def ImportFromPackageOld( self ) -> None:
		pass
