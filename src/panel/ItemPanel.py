from typing import List

import wx
import wx.lib.ticker

import widgets
from contentType.Item import Item
from packageManager import PackageManager
from widgets import TextButton

if __name__ == '__main__':
	from localization import loc


class ItemPanel( wx.Panel ):

	book: wx.BookCtrl
	master: 'Root'
	item: Item
	_infoTab: 'InfoTab'
	_descTab: 'DescriptionTab'
	_instanceTab: 'InstanceTab'
	_itemVarTab: 'ItemVarTab'
	_propertyTab: 'PropertyTab'
	_connTab: 'ConnectionTab'

	def __init__( self, master: wx.BookCtrl ):
		super( ItemPanel, self ).__init__(
			parent=master,
			name='PNL_ITEM_MAIN'
		)
		self.book = wx.BookCtrl(self)
		self.master = master.GetParent()
		self._infoTab = InfoTab( self.book )
		self.book.AddPage( self._infoTab, loc('root.book.itempage.book.info.title') )
		self._descTab = DescriptionTab(self.book)
		self.book.AddPage( self._descTab, loc('root.book.itempage.book.description.title') )
		self._instanceTab = InstanceTab( self.book )
		self.book.AddPage( self._instanceTab, loc('root.book.itempage.book.instances.title') )
		self._itemVarTab = ItemVarTab( self.book )
		self.book.AddPage( self._itemVarTab, loc('root.book.itempage.book.itemvar.title') )
		self._propertyTab = PropertyTab( self.book )
		self.book.AddPage( self._propertyTab, loc('root.book.itempage.book.property.title') )
		self._connTab = ConnectionTab( self.book )
		self.book.AddPage( self._connTab, loc('root.book.itempage.book.connection.title') )
		sizer = wx.BoxSizer()
		sizer.Add( self.book, wx.SizerFlags(1).Expand() )
		self.SetSizer( sizer )

	def OnItemSelection( self, name: str ):
		self.SaveItem()
		self.item = PackageManager.instance.package.GetItem(f'ITEM_{name.upper()}_BPM')
		self.LoadItem()

	def SaveItem( self ):
		pass

	def LoadItem( self ):
		self._infoTab.infoUrl = self.item.infoUrl
		self._infoTab.tags = self.item.tags

		self._descTab.desc = self.item.description


class InfoTab(wx.Panel):

	icon: wx.FilePickerCtrl
	calcEntCount: TextButton
	calcBrushCount: TextButton
	authors: wx.TextCtrl
	tags: List[str]  # TODO: This should be a thing in its own tab? the implementation may be funky and need space
	infoUrl: str
	panel: ItemPanel

	def __init__( self, master: wx.BookCtrl ):
		super( InfoTab, self ).__init__(
			parent=master,
			name='PNL_ITEM_INFO'
		)
		self.panel = master.GetParent()

		leftSizer = wx.BoxSizer(wx.VERTICAL)
		rightSizer = wx.BoxSizer(wx.VERTICAL)

		# icon path
		self.icon = wx.FilePickerCtrl(
			parent=self,
			wildcard='*.png'
		)
		leftSizer.Add( self.icon )

		# calc ent count
		self.calcEntCount = widgets.TextButton(
			parent=self,
			label=loc('root.book.itempage.book.info.cec.label')
		)

		# main sizer
		sizer = wx.BoxSizer()
		sizer.Add( leftSizer, wx.SizerFlags( 1 ).Expand() )
		sizer.Add( rightSizer, wx.SizerFlags( 1 ).Expand() )
		self.SetSizer( sizer )

	def LoadItem( self ):
		self.icon.SetPath( self.panel.item.icon )
		self.tags = self.panel.item.tags
		self.infoUrl = self.panel.item.infoUrl
		self.authors.SetValue( ', '.join( self.panel.item.authors ) )


class DescriptionTab(wx.Panel):

	desc: wx.TextCtrl
	panel: ItemPanel

	def __init__( self, master: wx.BookCtrl ):
		super( DescriptionTab, self ).__init__(
			parent=master,
			name='PNL_ITEM_DESCRIPTION'
		)
		self.panel = master.GetParent()

		sizer = wx.BoxSizer( wx.VERTICAL )

		self.desc = wx.TextCtrl(
			parent=self,
			size=wx.Size( 480, 300 ),
			value='',
			style=wx.TE_MULTILINE
		)

		sizer.Add( self.desc, wx.SizerFlags(1).Expand() )

		self.Bind( wx.EVT_TEXT, self.OnDescChange, self.desc )

	def OnDescChange( self, evt: wx.CommandEvent ):
		pass

	def LoadItem( self ):
		self.desc.SetValue( self.panel.item.description )


class InstanceTab(wx.Panel):

	panel: ItemPanel

	def __init__( self, master: wx.BookCtrl ):
		super( InstanceTab, self ).__init__(
			parent=master,
			name='PNL_ITEM_INSTANCE'
		)
		self.panel = master.GetParent()

	def LoadItem( self ):
		pass


class ConnectionTab(wx.Panel):

	panel: ItemPanel

	def __init__( self, master: wx.BookCtrl ):
		super( ConnectionTab, self ).__init__(
			parent=master,
			name='PNL_ITEM_CONNECTION'
		)
		self.panel = master.GetParent()

	def LoadItem( self ):
		pass


class ItemVarTab(wx.Panel):

	panel: ItemPanel

	def __init__( self, master: wx.BookCtrl ):
		super( ItemVarTab, self ).__init__(
			parent=master,
			name='PNL_ITEM_ITEMVAR'
		)
		self.panel = master.GetParent()

	def LoadItem( self ):
		pass


class PropertyTab(wx.Panel):

	panel: ItemPanel

	def __init__( self, master: wx.BookCtrl ):
		super( PropertyTab, self ).__init__(
			parent=master,
			name='PNL_ITEM_PROPERTY'
		)
		self.panel = master.GetParent()

	def LoadItem( self ):
		pass
