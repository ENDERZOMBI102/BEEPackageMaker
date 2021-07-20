from dataclasses import dataclass
from typing import Dict

from exportManager import ExportManager
from contentType import PackageComponent


@dataclass
class Style(PackageComponent):

	identifier: str
	styleVars: Dict[str, object]

	def Export( self, manager: ExportManager ) -> None:
		pass
