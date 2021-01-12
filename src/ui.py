import wx

if __name__ == '__main__':
	from localization import loc


class Root(wx.Frame):

	def __init__(self):
		super(Root, self).__init__(
			parent=None,
			title='BEE Package Maker',
			size=wx.Size(500, 600),
		)

		menuBar = wx.MenuBar()
		fileMenu = wx.Menu( title='file' )
		fileMenu.Append(0, loc('root.menu.file.exit.name') )
		menuBar.Append( fileMenu, loc('root.menu.file.name') )


		self.SetMenuBar( menuBar )

		self.CenterOnScreen()
		self.Show()
