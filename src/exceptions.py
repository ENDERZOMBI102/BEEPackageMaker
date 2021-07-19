class ItemAlreadyExistError(ValueError):

	def __init__(self, item: str):
		super(ItemAlreadyExistError, self).__init__(
			f'Item {item} already exists!'
		)


class PackageNotFound(Exception):
	def __init__( self, name: str ):
		super( PackageNotFound, self ).__init__( f'No package named {name} exists.' )

