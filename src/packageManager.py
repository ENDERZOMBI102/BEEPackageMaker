from typing import List, Dict, Any, Optional

import config
from contentType.item import Item
from exceptions import PackageNotFound
from package import Package


class PackageManager:

	instance: 'PackageManager'
	_currentPackage: Package
	packages: List[Package]

	def CreatePackage( self, name: str ) -> None:
		self.packages.append( Package(name) )

	def SwitchTo( self, name: str ) -> None:
		"""
		Tries to switch to another package.
		\t
		:raises PackageNotFound: If the requested package isn't found.
		:param name: The name of the package to switch to.
		"""
		pkg = self.FindPackage(name)
		if pkg is None:
			raise PackageNotFound(name)
		self._currentPackage = pkg

	def FindPackage( self, name: str ) -> Optional[Package]:
		"""
		Checks if a package is present
		\t
		:param name: package's name
		"""
		for package in self.packages:
			if package.name == name:
				return package
		return None

	def GetName( self ) -> Optional[str]:
		"""
		getter for the name of the currently selected package
		"""
		return getattr(self._currentPackage, 'name', None)

	def GetItem( self, name: str ) -> Optional[Item]:
		"""
		Getter for an item in the current package.
		\t
		:param name: name of the item
		"""
		for item in getattr(self._currentPackage, 'items', []):
			if item.name == name:
				return item
		return None

	def GetItemID( self, name: str ) -> str:
		"""
		Get a formatted id for an item name
		:param name:
		:return:
		"""
		return f'ITEM_{self.GetName().upper()}_{name.upper()}_BPM'

	def GetStyleID( self, name: str ) -> str:
		"""
		Get a formatted id for a style name
		:param name:
		:return:
		"""
		return f'STYLE_{self.GetName().upper()}_{name.upper()}_BPM'
