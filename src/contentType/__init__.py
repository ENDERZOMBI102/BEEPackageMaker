from abc import ABCMeta, abstractmethod

from exportManager import ExportManager


class PackageComponent(metaclass=ABCMeta):

	@abstractmethod
	def Export( self, manager: ExportManager ) -> None:
		pass
