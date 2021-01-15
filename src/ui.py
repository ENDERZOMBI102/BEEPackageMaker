import os
from pathlib import Path
from typing import Union, overload, Any, Dict

import wx
from srctools.logger import get_logger

import config
import utilities
from contentType.Item import Item
from contentType.Package import Package

if __name__ == '__main__':
	from localization import loc


logger = get_logger('Root Window')


class Root(wx.Frame):

	itemList: wx.ListBox
	book: wx.BookCtrl
	package: Package

	def __init__(self):
		# set the utilities.root pointer to the object of this class
		super(Root, self).__init__(
			parent=None,
			title=f'BEE Package Maker {str(config.version)}',
			size=wx.Size( width=600, height=500 )
		)
		Root.instance = self
		try:
			self.SetPosition( wx.Point( config.load( 'mainWindowPos' ) ) )
		except config.ConfigError:
			self.CenterOnScreen()
		self.SetSize( width=600, height=500 )
		self.SetMinSize( wx.Size( width=600, height=500 ) )
		logger.info( f'internet connected: {utilities.isonline()}' )

		# create the menu bar
		menuBar = wx.MenuBar()
		# file menu
		fileMenu = wx.Menu()
		openPortalDirItem = fileMenu.Append( 0, loc( 'root.menu.file.openportaldir.name' ) + '\tCtrl-P', loc( 'root.menu.file.openportaldir.description' ) )
		openBeeDirItem = fileMenu.Append( 1, loc( 'root.menu.file.openbeedir.name' ) + "\tCtrl-B", loc( 'root.menu.file.openbeedir.description' ) )
		exitItem = fileMenu.Append( 3, loc( 'root.menu.file.exit.name' ), loc( 'root.menu.file.exit.description' ) )
		menuBar.Append( fileMenu, loc('root.menu.file.name') )

		# item menu
		itemMenu = wx.Menu()
		addItemItem = itemMenu.Append( 4, loc( 'root.menu.item.additem.name' ), loc( 'root.menu.item.additem.description' ) )
		removeItemItem = itemMenu.Append( 5, loc( 'root.menu.item.removeitem.name' ), loc( 'root.menu.item.removeitem.description' ) )
		menuBar.Append( itemMenu, loc('root.menu.item.name') )

		# help menu bar
		helpMenu = wx.Menu()
		aboutItem: wx.MenuItem = helpMenu.Append( 13, loc( 'root.menu.help.about.name' ), loc( 'root.menu.help.about.description' ) )
		aboutItem.SetBitmap( wx.Bitmap( f'{config.assetsPath}icons/menu_bm.png' ) )
		wikiItem: wx.MenuItem = helpMenu.Append( 14, loc( 'root.menu.help.wiki.name' ), loc( 'root.menu.help.wiki.description' ) )
		wikiItem.SetBitmap( wx.Bitmap( f'{config.assetsPath}icons/menu_github.png' ) )
		githubItem: wx.MenuItem = helpMenu.Append( 15, loc( 'root.menu.help.github.name' ), loc( 'root.menu.help.github.description' ) )
		githubItem.SetBitmap( wx.Bitmap( f'{config.assetsPath}icons/menu_github.png' ) )
		discordItem: wx.MenuItem = helpMenu.Append( 16, loc( 'root.menu.help.discord.name' ), loc( 'root.menu.help.discord.description' ) )
		discordItem.SetBitmap( wx.Bitmap( f'{config.assetsPath}icons/menu_discord.png' ) )
		menuBar.Append( helpMenu, loc('root.menu.help.name') )

		self.SetMenuBar( menuBar )
		self.CreateStatusBar()
		self.SetStatusText( loc( 'root.statusbar.text', username=config.steamUsername() ) )

		self.itemList = wx.ListBox(
			parent=self,
			choices=[ loc('root.itemlist.empty') ],
			size=wx.Size( 100, self.GetSize().GetHeight() - 80 )
		)
		self.itemList.SetMinSize( wx.Size( 100, self.GetSize().GetHeight() - 80 ) )

		self.book = wx.BookCtrl(
			parent=self,
			size=wx.Size( self.GetSize().GetWidth() - 100, self.GetSize().GetHeight() - 80)
		)
		self.book.SetMinSize( wx.Size( self.GetSize().GetWidth() - 100, self.GetSize().GetHeight() - 80) )
		self.book.AddPage( ItemPanel(self.book, 'Item'), loc('root.book.itempage.name')  )

		mainSizer = wx.BoxSizer()
		mainSizer.Add( self.itemList, wx.SizerFlags(1).Expand() )
		mainSizer.Add( self.book, wx.SizerFlags(4).Expand() )
		mainSizer.SetSizeHints( self )
		self.SetSizer( mainSizer )

		# menu bar events
		# file menu
		self.Bind( wx.EVT_MENU, self.openp2dir, openPortalDirItem )
		self.Bind( wx.EVT_MENU, self.openBEEdir, openBeeDirItem )
		self.Bind( wx.EVT_MENU, self.OnClose, exitItem )
		# items menu
		self.Bind( wx.EVT_MENU, self.OnAddItem, addItemItem )
		self.Bind( wx.EVT_MENU, self.OnRemoveItem, removeItemItem )

		# normal events
		self.Bind( wx.EVT_LISTBOX, self.OnItemSelection, self.itemList )

		# window events
		self.Bind( wx.EVT_CLOSE, self.OnClose, self )


		self.Show()

	# wx event callbacks
	def OnClose( self, evt: Union[wx.CloseEvent, wx.MenuEvent] ):
		"""
		called when the window/application is about to close
		:param evt: placeholder
		"""
		# get the window position and save it
		pos = list( self.GetPosition().Get() )
		logger.debug( f'saved main window position: {pos}' )
		config.save( pos, 'mainWindowPos' )
		config.save( None, 'placeholderForSaving' )
		self.Destroy()

	# item list callback

	def OnItemSelection( self, evt: wx.CommandEvent ):
		if self.itemList.GetString( self.itemList.GetSelection() ) == loc('root.itemlist.empty'):
			self.itemList.Deselect(0)

	# menu items callbacks

	# file menu
	@staticmethod
	def openp2dir( evt: wx.CommandEvent ):
		"""
		opens the Portal 2 directory with the default file explorer
		:param evt: placeholder
		"""
		os.startfile( config.portalDir() )

	@staticmethod
	def openBEEdir( evt: wx.CommandEvent ):
		"""
		opens the BEE2.4 directory with the default file explorer
		:param evt: placeholder
		"""
		os.startfile(
			Path( config.load( 'beePath' ) ).parent
			if config.load( 'beePath' ).lower().endswith( '.exe' )
			else Path( config.load( 'beePath' ) )
		)

	# items menu
	def OnAddItem( self, evt: wx.CommandEvent ):
		while True:
			diag = wx.TextEntryDialog(
				parent=self,
				caption=loc( 'root.dialog.newitem.title' ),
				message=loc( 'root.dialog.newitem.message' )
			)
			diag.ShowModal()
			if diag.GetValue() not in ['', ' ']:
				if diag.GetValue() not in self.itemList.GetItems():
					self.itemList.Delete( self.itemList.FindString( loc('root.itemlist.empty') ) )
					self.itemList.Insert( diag.GetValue(), 0 )
					self.itemList.Select( 0 )
					break

	def OnRemoveItem( self, evt: wx.CommandEvent ):
		if self.itemList.GetSelection() == wx.NOT_FOUND:
			diag = wx.MessageDialog(
				parent=self,
				caption=loc( 'root.dialog.no_selection.title' ),
				message=loc( 'root.dialog.no_selection.message' )
			)
			diag.ShowModal()
		elif self.itemList.GetString( self.itemList.GetSelection() ) == loc('root.itemlist.empty'):
			diag = wx.MessageDialog(
				parent=self,
				caption=loc( 'root.dialog.invalid_action.title' ),
				message=loc( 'root.dialog.invalid_action.message', subject=f'"{loc("root.itemlist.empty")}" Item', action='removed' )
			)
			diag.ShowModal()
		else:
			self.itemList.Delete( self.itemList.GetSelection() )
			if len( self.itemList.GetItems() ) == 0:
				self.itemList.Append( loc('root.itemlist.empty') )


class ItemPanel(wx.Panel):

	def __init__(self, master: wx.BookCtrl, item: str):
		super(ItemPanel, self).__init__(
			parent=master,
			name=item
		)

