import json
import logging
from logging import Logger
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
from cli import parsedArguments
from packageManager import PackageManager
from ui import Root
import localization

if __name__ == '__helo__':
	from localization import loc


class WxLogHandler( wx.Log ):
	""" Handle WX logging, and redirect it to Python's log system. """

	# lookup table to convert WX log levels to stdlib equivalents.
	levelLookupTable = {
		wx.LOG_Debug: logging.DEBUG,
		wx.LOG_Error: logging.ERROR,
		wx.LOG_FatalError: logging.FATAL,
		wx.LOG_Info: logging.INFO,
		wx.LOG_Max: logging.DEBUG,
		wx.LOG_Message: logging.INFO,
		wx.LOG_Progress: logging.DEBUG,
		wx.LOG_Status: logging.INFO,
		wx.LOG_Trace: logging.DEBUG,
		wx.LOG_User: logging.DEBUG,
		wx.LOG_Warning: logging.WARNING,
	}

	def __init__( self ) -> None:
		super().__init__()
		self.logger: Logger = srctools.logger.get_logger( 'wxPython' )

	# noinspection PyPropertyAccess
	def DoLogRecord( self, level: int, msg: str, info: wx.LogRecordInfo ) -> None:
		""" Pass the WX log system into the Python system. """
		# Filename and function name are bytes, ew.
		self.logger.handle(
			self.logger.makeRecord(
				'wxPython',
				self.levelLookupTable.get( level, logging.INFO ),
				info.filename.decode( 'utf8', 'ignore' ),
				info.line,
				msg,
				(),  # It's already been formatted so no args are needed.
				None,  # Exception info, not compatible.
				info.func.decode( 'utf8', 'ignore' ),
			)
		)


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
		self.logger = srctools.logger.init_logging(
			filename='./logs/latest.log' if utilities.frozen() else './../logs/latest.log',
			main_logger='BEE Package Maker',
			on_error=self.OnError
		)
		# log wx logging to python's logging module
		wx.Log.SetActiveTarget( WxLogHandler() )
		# if we started with --dev parameter, set loglevel to debug
		if parsedArguments.dev:
			config.overwrite( 'logLevel', 'DEBUG' )
			config.overwrite( 'logWindowVisibility', True )
			utilities.devEnv = True
		if parsedArguments.flags is not None:
			# add all flags
			config.dynConfig.parseFlags( parsedArguments.flags )
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
		# TODO: ADD THIS FOLDER TO CONFIG + EDIT THE utilities.tmpDirPath TO POINT TO THIS
		Path( f'{config.resourcesPath}/cache/' ).mkdir( exist_ok=True )
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
	print( f'BPM is running in a {"packed" if utilities.frozen() else "developer"} enviroment.' )
	timeTest.start()
	app = App()
	if parsedArguments.time:
		timeTest.stop()
	app.MainLoop()
