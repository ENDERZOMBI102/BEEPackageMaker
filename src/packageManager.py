from typing import List, Optional

from abstract.manager import AbstractManager
from contentType.item import Item
from exceptions import PackageNotFound
from package import Package


class PackageManager(AbstractManager):
	_currentPackage: Package
	packages: List[Package]

	def Init( self ) -> None:
		pass

	def Stop( self ) -> None:
		pass

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
		""" Getter for the name of the currently selected package """
		return getattr(self._currentPackage, 'name', None)

	def GetItem( self, name: str = None, identifier: str = None ) -> Optional[Item]:
		"""
		Getter for an item in the current package.
		\t
		:param name: Name of the item
		:param identifier: Identifier of the item
		"""
		for item in getattr(self._currentPackage, 'items', []):
			if name is not None and item.name == name:
				return item
			if identifier is not None and item.identifier == identifier:
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

	def GetCurrent( self ) -> Optional[Package]:
		"""	Getter for the current package """
		return self._currentPackage

	def CreateItem( self, name: str ) -> None:
		"""
		Creates an item object with the specified name and adds it to the current package.
		\t
		:param name: Name of the item.
		:return: The created item.
		"""
		item = Item()
		item.name = name
		item.identifier = self.GetItemID(name)
		self._currentPackage.items.append( item )


manager: PackageManager = PackageManager()
