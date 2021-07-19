from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Instance:
	pass


@dataclass
class Item:
	identifier: str
	description: str
	versions: Dict[str, Instance]





@dataclass
class Track:
	identifier: str  # get this from the name ( MUSIC_PGKNAME_GROUP_SHORTSNAME ?)
	name: str
	shortName: str
	sortKey: int
	group: str
	icon: str
	iconLarge: str
	authors: List[str]
	description: str
	sample: str  # make the user choose what this is from soundFile directly
	loopLenght: float  # calculate this from the soundFile
	soundFile: str  # path of the track file/ByteIO of it




@dataclass
class Package:
	name: str
	identifier: str
	description: str
	dependencies: List[str]
	items: List[Item]
	brushTemplates: List[BrushTemplate]
	styles: List[Style]
	tracks: List[Track]


