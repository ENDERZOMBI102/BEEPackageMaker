import wx


class TemplateManager:

	window: 'TemplateManagerWindow'

	def __init__(self):
		self.window = TemplateManagerWindow()

	def ShowManager( self, *args ):
		self.window.Show()


class TemplateManagerWindow(wx.Frame):

	def __init__(self):
		super(TemplateManagerWindow, self).__init__(
			parent=wx.GetActiveWindow(),
			title='Manage Templates'
		)
		self.Bind( wx.EVT_CLOSE, lambda evt: self.Show(False), self )


class Template:
	pass
