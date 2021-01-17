import wx


class TextButton(wx.Window):

	txt: wx.TextCtrl
	btn: wx.Button

	def __init__( self, parent: wx.Window, label='', value='', name='' ):
		super( TextButton, self ).__init__(
			parent=parent,
			name=name
		)

		sizer = wx.BoxSizer()

		self.txt = wx.TextCtrl(
			parent=self,
			value=value
		)
		sizer.Add( self.txt )

		self.btn = wx.Button(
			parent=self,
			label=label
		)
		sizer.Add( self.btn )
		self.SetSizer( sizer )
		self.Show()
