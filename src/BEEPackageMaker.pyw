import json
import logging
import os
import sys
import traceback
from pathlib import Path
from sys import argv
from types import TracebackType
from typing import Type

import srctools.logger
import wx

import config
import timeTest
import utilities
from packageManager import PackageManager
from ui import Root
import localization

if __name__ == '__helo__':
	from localization import loc


class App(wx.App):

	root: Root
	logger: logging.Logger
	ShouldExit: bool = False
	ShouldRestart: bool = False
	instanceChecker = wx.SingleInstanceChecker('BPM')

	def OnPreInit( self ):
		# check if there's another instance running
		if self.instanceChecker.IsAnotherRunning():
			self.ShouldExit = True
			return
		# initialize logging
		# overwrite stdout log level if on launched from source
		if not utilities.frozen():
			os.environ[ 'SRCTOOLS_DEBUG' ] = '1'
		# use a window to show the uncaught exception to the user
		srctools.logger.init_logging(
			filename='./logs/latest.log' if utilities.frozen() else './../logs/latest.log',
			main_logger='BEE Manipulator',
			on_error=self.OnError
		)
		self.logger = srctools.logger.get_logger( 'BEE Manipulator' )
		# if we started with --dev parameter, set loglevel to debug
		if '--dev' in argv:
			utilities.env = 'dev'
		if '--flags' in argv:
			flagIndex = argv.index( '--flags' ) + 1
			if not argv[ flagIndex ].startswith( '--' ):
				config.dynConfig.parseFlags( argv[ flagIndex ] )
		# check configs
		self.logger.info( 'Checking config file..' )
		if config.check():
			self.logger.info( 'Valid config file found!' )
		else:
			self.logger.error( 'Invalid or inesistent config file detected!' )
			self.logger.info( 'Creating new config file...' )
			config.createConfig()
			self.logger.info( 'Config file created!' )
		# populate the config dict
		config.currentConfigData = config.default_config
		with open( config.configPath, 'r' ) as file:
			for section, value in json.load( file ).items():
				if section != 'nextLaunch':
					config.currentConfigData[ section ] = value
				else:
					if len( value.keys() ) > 0:
						self.logger.info( 'Seems that we may have crashed last time, lets overwrite things!' )
						config.currentConfigData = {**config.currentConfigData, **value}
					else:
						self.logger.info( 'Nothing to overwrite for this launch!' )
					config.currentConfigData[ 'nextLaunch' ] = {}
		# folders
		Path( f'{config.resourcesPath}cache/' ).mkdir( exist_ok=True )
		Path( f'{config.load("exportedPackagesDir")}' ).mkdir( exist_ok=True )
		# start localizations
		localization.Localize()
		self.logger.info( f'current lang: {loc( "currentLang" )}' )

	def OnInit( self ):
		if self.ShouldExit:
			return False
		# set app name
		self.logger.debug( "setting application name.." )
		self.SetAppName( "BEE Package Maker" )
		self.SetAppDisplayName( "BEE Package Maker" )
		self.logger.debug( "setted app name" )
		# start ui
		self.logger.info( f'Starting BEE Package Maker v{config.version}!' )
		PackageManager.instance = PackageManager()
		self.logger.info( 'starting ui!' )
		self.root = Root()
		return True

	def OnExit(self):
		with open( config.configPath, 'w' ) as file:
			json.dump( config.currentConfigData, file, indent=4 )
		if config.dynConfig[ 'continueLoggingOnUncaughtException' ]:
			import logging
			logging.shutdown()
		if self.ShouldRestart:
			os.system( sys.executable )
		return True

	def OnError( self, etype: Type[BaseException], value: BaseException, tb: TracebackType ):
		try:
			wx.MessageBox(
				message=''.join( traceback.format_exception( etype, value, tb ) ),
				caption='BPM Error!',
				style=wx.OK | wx.CENTRE | wx.STAY_ON_TOP | wx.ICON_ERROR
			)
		except Exception:
			wx.SafeShowMessage( title='BPM Error!', text=''.join( traceback.format_exception( etype, value, tb ) ) )
		try:
			if self.root is not None:
				self.root.Destroy()
		except AttributeError:
			# the root ui has already been destroyed
			pass


if __name__ == '__main__':
	# use file dir as working dir
	path: Path = None
	if utilities.frozen():
		path = Path( sys.executable ).resolve()
		print( f"BPM exe path: {path.parent.resolve()}" )
	else:
		path = Path( __file__ ).resolve()
		print( 'BPM is running in a developer environment.' )
		print( f"BPM source path: {path.parent}" )
	os.chdir( path.parent )
	timeStartup = '--time' in argv
	if timeStartup:
		timeTest.start()
	app = App()
	if timeStartup:
		timeTest.stop()
	app.MainLoop()