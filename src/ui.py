import wx
from srctools.logger import get_logger

import config
import utilities

if __name__ == '__main__':
	from localization import loc


LOGGER = get_logger('Root Window')


class Root(wx.Frame):

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
		LOGGER.info( f'internet connected: {utilities.isonline()}' )

		# create the menu bar
		menuBar = wx.MenuBar()
		# file menu
		fileMenu = wx.Menu( title='file' )

		fileMenu.Append(0, loc('root.menu.file.exit.name') )
		menuBar.Append( fileMenu, loc('root.menu.file.name') )

		self.SetMenuBar( menuBar )
		self.CreateStatusBar()
		self.SetStatusText( loc( 'root.statusbar.text' ).replace( '{username}', config.steamUsername() ) )

		# menu bar events
		# file menu
		self.Bind( wx.EVT_MENU, self.openp2dir, openPortalDirItem )
		self.Bind( wx.EVT_MENU, self.openBEEdir, openBeeDirItem )
		self.Bind( wx.EVT_MENU, self.exit, exitItem )

		self.Bind( wx.EVT_CLOSE, self.OnClose, self )

		self.Show()

	# wx event callbacks
	def OnClose( self, evt: wx.CloseEvent ):
		"""
		called when the window/application is about to close
		:param evt: placeholder
		"""
		# get the window position and save it
		pos = list( self.GetPosition().Get() )
		LOGGER.debug( f'saved main window position: {pos}' )
		config.save( pos, 'mainWindowPos' )
		config.save( None, 'placeholderForSaving' )
		self.Destroy()

