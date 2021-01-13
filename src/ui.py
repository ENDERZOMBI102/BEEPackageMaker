import os
from pathlib import Path
from typing import Union

import wx
from srctools.logger import get_logger

import config
import utilities

if __name__ == '__main__':
	from localization import loc


logger = get_logger('Root Window')


class Root(wx.Frame):

	itemSelector: wx.Choice
	pnl: wx.Panel

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

		self.SetMenuBar( menuBar )
		self.CreateStatusBar()
		self.SetStatusText( loc( 'root.statusbar.text' ).replace( '{username}', config.steamUsername() ) )

		self.pnl = wx.Panel(self)

		rightSizer = wx.BoxSizer(wx.VERTICAL)
		leftSizer = wx.BoxSizer(wx.VERTICAL)

		self.itemSelector = wx.Choice(
			parent=self.pnl,
			pos=wx.Point(3, 4)
		)
		self.itemSelector.Append( loc('root.itemlist.additem') )
		rightSizer.Add( self.itemSelector )

		sizer = wx.BoxSizer()
		sizer.Add( leftSizer )
		sizer.Add( rightSizer )
		self.pnl.SetSizer( sizer )

		# menu bar events
		# file menu
		self.Bind( wx.EVT_MENU, self.openp2dir, openPortalDirItem )
		self.Bind( wx.EVT_MENU, self.openBEEdir, openBeeDirItem )
		self.Bind( wx.EVT_MENU, self.OnClose, exitItem )

		# normal events
		self.Bind( wx.EVT_CHOICE, self.OnItemSelection, self.itemSelector )

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

	# menu items callbacks
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

	def OnItemSelection( self, evt: wx.CommandEvent ):
		if evt.GetString() == loc('root.itemlist.additem'):
			diag = wx.TextEntryDialog(
				parent=self,
				caption=loc('root.dialog.newitem.title'),
				message=loc('root.dialog.newitem.message')
			)
			diag.ShowModal()
			self.itemSelector.Insert( diag.GetValue(), 0 )
			self.itemSelector.Select(0)




