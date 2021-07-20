import wx

from abstract.manager import AbstractManager


class TemplateManager(AbstractManager):

	window: 'TemplateManagerWindow'

	def Init( self ) -> None:
		self.window = TemplateManagerWindow()

	def Stop( self ) -> None:
		pass

	def ShowManager( self, *args ):
		self.window.Show()


manager: TemplateManager = TemplateManager()


class TemplateManagerWindow(wx.Frame):

	def __init__(self):
		super(TemplateManagerWindow, self).__init__(
			parent=wx.GetActiveWindow(),
			title='Manage Templates'
		)
		self.Bind( wx.EVT_CLOSE, lambda evt: self.Show(False), self )


class Template:
	pass
