import os
from pathlib import Path
from typing import Union, Dict

import wx
from srctools.logger import get_logger

import aboutWindow
import config
import utilities
from packageManager import PackageManager
from panel.ItemPanel import ItemPanel

if __name__ == '__main__':
	from localization import loc


logger = get_logger('Root Window')
_menuIndex: int = 0


def newMenuIndex() -> int:
	global _menuIndex
	_menuIndex += 1
	return _menuIndex - 1


class Root(wx.Frame):

	itemList: wx.ListBox
	book: wx.BookCtrl
	menus: Dict[str, wx.MenuItem]
	itemPanel: ItemPanel

	def __init__(self):
		# set the utilities.root pointer to the object of this class
		super(Root, self).__init__(
			parent=None,
			title=loc( 'root.title', version=config.version.__str__() ),
			size=wx.Size( width=600, height=500 )
		)
		try:
			self.SetPosition( wx.Point( config.load( 'mainWindowPos' ) ) )
		except config.ConfigError:
			self.CenterOnScreen()
		if utilities.icon is not None:
			self.SetIcon( utilities.icon )
		self.SetSize( width=600, height=500 )
		self.SetMinSize( wx.Size( width=600, height=500 ) )
		logger.info( f'internet connected: {utilities.isonline()}' )

		# create the menu bar
		self.menus = {}
		menuBar = wx.MenuBar()
		# file menu
		fileMenu = wx.Menu()
		self.menus['openPortalDirItem'] = fileMenu.Append( newMenuIndex(), loc( 'root.menu.file.openportaldir.name' ) + '\tCtrl-P', loc( 'root.menu.file.openportaldir.description' ) )
		self.menus['openBeeDirItem'] = fileMenu.Append( newMenuIndex(), loc( 'root.menu.file.openbeedir.name' ) + '\tCtrl-B', loc( 'root.menu.file.openbeedir.description' ) )
		self.menus['exitItem'] = fileMenu.Append( newMenuIndex(), loc( 'root.menu.file.exit.name' ), loc( 'root.menu.file.exit.description' ) )
		menuBar.Append( fileMenu, loc('root.menu.file.title') )

		# item menu
		itemMenu = wx.Menu()
		self.menus['addItemItem'] = itemMenu.Append( newMenuIndex(), loc( 'root.menu.item.additem.name' ) + '\tCtrl-X', loc( 'root.menu.item.additem.description' ) )
		self.menus['removeItemItem'] = itemMenu.Append( newMenuIndex(), loc( 'root.menu.item.removeitem.name' ), loc( 'root.menu.item.removeitem.description' ) )
		menuBar.Append( itemMenu, loc('root.menu.item.title') )

		# package menu
		packageMenu = wx.Menu()
		self.menus[ 'savePackageItem' ] = packageMenu.Append( newMenuIndex(), loc('root.menu.package.save.name'), loc('root.menu.package.save.description') )
		packageExportSubMenu = wx.Menu()
		self.menus['exportToBEE36Item'] = packageExportSubMenu.Append( newMenuIndex(), loc('root.menu.package.export.beemod36.name'), loc('root.menu.package.export.beemod36.description') )
		self.menus['exportToBEEItem'] = packageExportSubMenu.Append( newMenuIndex(), loc( 'root.menu.package.export.beemod.name' ), loc( 'root.menu.package.export.beemod.description' ) )
		self.menus['exportToSaismeeItem'] = packageExportSubMenu.Append(newMenuIndex(), loc('root.menu.package.export.saismee.name'), loc('root.menu.package.export.saismee.description') )
		self.menus['exportToBaguetteryItem'] = packageExportSubMenu.Append(newMenuIndex(), loc('root.menu.package.export.baguettery.name'), loc('root.menu.package.export.baguettery.description') )
		packageMenu.AppendSubMenu( packageExportSubMenu, loc('root.menu.package.export.name') )
		packageImportSubMenu = wx.Menu()
		self.menus[ 'importFromBEE36Item' ] = packageImportSubMenu.Append( newMenuIndex(), loc('root.menu.package.export.beemod36.name' ), loc( 'root.menu.package.import.beemod36.description' ) )
		self.menus[ 'importFromBEEItem' ] = packageImportSubMenu.Append( newMenuIndex(), loc( 'root.menu.package.export.beemod.name' ),loc('root.menu.package.import.beemod.description' ) )
		self.menus[ 'importFromSaismeeItem' ] = packageImportSubMenu.Append( newMenuIndex(), loc('root.menu.package.export.saismee.name' ), loc( 'root.menu.package.import.saismee.description' ) )
		self.menus[ 'importFromBaguetteryItem' ] = packageImportSubMenu.Append( newMenuIndex(), loc('root.menu.package.export.baguettery.name' ), loc( 'root.menu.package.import.baguettery.description' ) )
		packageMenu.AppendSubMenu( packageImportSubMenu, loc( 'root.menu.package.import.name' ) )
		menuBar.Append( packageMenu, loc('root.menu.package.title') )

		# help menu bar
		helpMenu = wx.Menu()
		self.menus['aboutItem'] = helpMenu.Append( newMenuIndex(), loc( 'root.menu.help.about.name' ), loc( 'root.menu.help.about.description' ) )
		# self.menus['aboutItem'].SetBitmap( wx.Bitmap( f'{config.resourcesPath}icons/menu_bm.png' ) )
		self.menus['wikiItem'] = helpMenu.Append( newMenuIndex(), loc( 'root.menu.help.wiki.name' ), loc( 'root.menu.help.wiki.description' ) )
		# self.menus['wikiItem'].SetBitmap( wx.Bitmap( f'{config.resourcesPath}icons/menu_github.png' ) )
		self.menus['githubItem'] = helpMenu.Append( newMenuIndex(), loc( 'root.menu.help.github.name' ), loc( 'root.menu.help.github.description' ) )
		# self.menus['githubItem'].SetBitmap( wx.Bitmap( f'{config.resourcesPath}icons/menu_github.png' ) )
		self.menus['discordItem'] = helpMenu.Append( newMenuIndex(), loc( 'root.menu.help.discord.name' ), loc( 'root.menu.help.discord.description' ) )
		# self.menus['discordItem'].SetBitmap( wx.Bitmap( f'{config.resourcesPath}icons/menu_discord.png' ) )
		menuBar.Append( helpMenu, loc('root.menu.help.title') )

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
		self.itemPanel = ItemPanel(self.book)
		self.book.AddPage( self.itemPanel, loc('root.book.itempage.title')  )

		mainSizer = wx.BoxSizer()
		mainSizer.Add( self.itemList, wx.SizerFlags(1).Expand() )
		mainSizer.Add( self.book, wx.SizerFlags(4).Expand() )
		mainSizer.SetSizeHints( self )
		self.SetSizer( mainSizer )

		# menu bar events
		# file menu
		self.Bind( wx.EVT_MENU, self.openp2dir, self.menus[ 'openPortalDirItem' ] )
		self.Bind( wx.EVT_MENU, self.openBEEdir, self.menus[ 'openBeeDirItem' ] )
		self.Bind( wx.EVT_MENU, self.OnClose, self.menus[ 'exitItem' ] )
		# items menu
		self.Bind( wx.EVT_MENU, self.OnAddItem, self.menus[ 'addItemItem' ] )
		self.Bind( wx.EVT_MENU, self.OnRemoveItem, self.menus[ 'removeItemItem' ] )
		# package menu
		self.Bind( wx.EVT_MENU, self.OnSave, self.menus[ 'savePackageItem' ])
		self.Bind( wx.EVT_MENU, self.OnExport, self.menus[ 'exportToBEE36Item' ])
		self.Bind( wx.EVT_MENU, self.OnExport, self.menus[ 'exportToBEEItem' ] )
		self.Bind( wx.EVT_MENU, self.OnExport, self.menus[ 'exportToSaismeeItem' ] )
		self.Bind( wx.EVT_MENU, self.OnExport, self.menus[ 'exportToBaguetteryItem' ] )
		self.Bind( wx.EVT_MENU, self.OnImport, self.menus[ 'importFromBEE36Item' ] )
		self.Bind( wx.EVT_MENU, self.OnImport, self.menus[ 'importFromBEEItem' ] )
		self.Bind( wx.EVT_MENU, self.OnImport, self.menus[ 'importFromSaismeeItem' ] )
		self.Bind( wx.EVT_MENU, self.OnImport, self.menus[ 'importFromBaguetteryItem' ] )
		# help menu
		self.Bind( wx.EVT_MENU, self.OpenAboutWindow, self.menus[ 'aboutItem' ] )
		self.Bind( wx.EVT_MENU, self.OpenWiki, self.menus[ 'wikiItem' ] )
		self.Bind( wx.EVT_MENU, self.OpenGithub, self.menus[ 'githubItem' ] )
		self.Bind( wx.EVT_MENU, self.OpenDiscord, self.menus[ 'discordItem' ] )
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
		else:
			self.itemPanel.OnItemSelection( evt.GetString() )

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
				message=loc( 'root.dialog.newitem.message' ),
				value=loc( 'root.dialog.newitem.defvalue' )
			)
			diag.ShowModal()
			if diag.GetValue() not in ['', ' ']:
				if diag.GetValue() == loc( 'root.dialog.newitem.defvalue' ):
					return
				if diag.GetValue() not in self.itemList.GetItems():
					self.itemList.Delete( self.itemList.FindString( loc('root.itemlist.empty') ) )
					self.itemList.Insert( diag.GetValue(), 0 )
					self.itemList.Select( 0 )
					return

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

	# package menu
	def OnSave( self, evt: wx.CommandEvent ):
		pass

	def OnExport( self, evt: wx.CommandEvent ):
		if evt.GetId() == self.menus[ 'exportToBEE36Item' ].GetId():
			PackageManager.instance.ExportToPackageOld()
		elif evt.GetId() == self.menus[ 'exportToBEEItem' ].GetId():
			PackageManager.instance.ExportToPackage()
		elif evt.GetId() == self.menus[ 'exportToSaismeeItem' ].GetId():
			PackageManager.instance.ExportToSaismee()
		else:  # this is self.menus[ 'exportToBaguetteryItem' ]
			PackageManager.instance.ExportToBaguettery()

	def OnImport( self, evt: wx.CommandEvent ):
		if evt.GetId() == self.menus[ 'importFromBEE46Item' ].GetId():
			PackageManager.instance.ImportFromPackageOld()
		elif evt.GetId() == self.menus[ 'importFromBEEItem' ].GetId():
			PackageManager.instance.ImportFromPackage()
		elif evt.GetId() == self.menus[ 'importFromSaismeeItem' ].GetId():
			PackageManager.instance.ImportFromSaismee()
		else:  # this is self.menus[ 'importFromBaguetteryItem' ]
			PackageManager.instance.ImportFromBaguettery()

	# help menu
	@staticmethod
	def OpenAboutWindow( evt: wx.CommandEvent ):
		aboutWindow.init()

	@staticmethod
	def OpenWiki( evt: wx.CommandEvent ):
		utilities.openUrl( 'https://github.com/ENDERZOMBI102/BEEPackageMaker/wiki' )

	@staticmethod
	def OpenGithub( evt: wx.CommandEvent ):
		utilities.openUrl( 'https://github.com/ENDERZOMBI102/BEEPackageMaker' )

	@staticmethod
	def OpenDiscord( evt: wx.CommandEvent ):
		utilities.openUrl( 'https://discord.gg/hnGFJrz' )
