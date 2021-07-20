from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from exportManager import ExportManager
from contentType import PackageComponent


class Item(PackageComponent):
	# metadata
	name: str
	identifier: str
	description: str
	infoUrl: str
	icon: Path
	authors: str
	tags: List[str]
	# components
	# a dict with styleId : Instance
	styled: Dict[ str, 'Instance' ]

	def __init__(self):
		pass

	def Export( self, manager: ExportManager ) -> None:
		pass


@dataclass
class Instance:
	pass
