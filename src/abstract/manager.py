from abc import ABCMeta, abstractmethod


class AbstractManager(metaclass=ABCMeta):

	@abstractmethod
	def Init( self ) -> None:
		pass

	@abstractmethod
	def Stop( self ) -> None:
		pass
