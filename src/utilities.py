import importlib
import os
import sys
import webbrowser
from io import BytesIO
from pathlib import Path
from sys import platform
from types import ModuleType
from typing import Union, Callable

import wx
from requests import get, RequestException
from semver import VersionInfo

if __name__ == '__main__':
	from localization import loc
import config
from srctools.logger import get_logger

logger = get_logger("utils")
icon: wx.Icon = None
"""BEE Package Maker icon as wx.Icon object"""


class wxStyles:
	TITLEBAR_ONLY_BUTTON_CLOSE = wx.DEFAULT_FRAME_STYLE ^ wx.MINIMIZE_BOX ^ wx.MAXIMIZE_BOX


class UpdateInfo:

	version: VersionInfo
	url: str
	description: str

	def __init__(self, ver: VersionInfo, url: str, desc: str):
		self.version = ver
		self.url = url
		self.description = desc


def init():
	global icon
	icon = wx.Icon(f'{config.resourcesPath}icons/icon.png' )


def isonline():
	"""
	Simple function that checks if the pc is online or not
	\t
	:return: True if it is else False
	"""
	try:
		logger.debug('checking connection..')
		get('https://www.google.com/')
		get('https://github.com/')
		return True
	except RequestException:
		return False


def checkUpdate(url: str, curVer: VersionInfo) -> UpdateInfo:
	"""
	A function that check for updates, this doesn't include prereleases
	\t
	:param url: the api/repo github url
	:param curVer: current version
	:return: an object of class VersionInfo
	"""
	logger.debug(f'checking url..')
	if 'api.github' not in url:
		logger.debug(f'converting url..')
		url = genReleasesApiUrl(url)  # convert normal github repo url to github api url
	logger.debug(f'url valid!')
	logger.debug(f'checking updates on url: {url}')
	data: dict = get( url ).json()  # get the latest release data
	if not isinstance(data, list):
		return UpdateInfo( None, None, None )
	usePrereleases: bool = config.load('usePrereleases')
	for ver in data:
		if ver['draft'] is True:
			continue
		if ( ver['prerelease'] is True ) and ( usePrereleases is False ):
			continue
		data = ver
		break
	if isinstance(data, list):
		return UpdateInfo( None, None, None )
	# variables
	releaseUrl: str = None
	releaseVer: VersionInfo = None
	releaseDesc: str = None
	# special edge-case
	ov = data['tag_name'] if 'BEEmod' not in url else data['tag_name'].replace('2.4', '4', 1)
	# if the most recent release is not a greater one,
	# we just return a UpdateInfo object with every value setted to None
	# else we return a "complete" UpdateInfo object
	if VersionInfo.parse( ov ) > curVer:
		releaseUrl = getReleaseUrl(data)
		releaseVer = VersionInfo.parse( ov )
		releaseDesc = data['body']
	return UpdateInfo( releaseVer, releaseUrl, releaseDesc )


def genReleasesApiUrl(url: str = None) -> str:
	"""
	A function that makes a github api latest release url from a repo url
	aram url: repo url to be transformed
	\t
	:return: the github api url
	"""
	splitUrl = url.split('/')  # slit the url in various segments
	return f'https://api.github.com/repos/{splitUrl[3]}/{splitUrl[4]}/releases'  # return the formed url


def getReleaseUrl(data) -> str:
	"""
	A function that return the correct release for the platform
	\t
	:param data: the latest release data
	:return: the asset url
	"""
	# if there's a single asset, we can't fail
	if len(data['assets']) == 1:
		return data['assets'][0]['browser_download_url']
	# cycle in the assets
	for asset in data['assets']:
		# get the correct url for the OS we're on
		if 'mac' in asset['name'] and 'darwin' in platform:
			return asset['browser_download_url']
		elif 'win' in asset['name'] and 'win' in platform:
			return asset['browser_download_url']
	raise Exception("how this happened?, you're on linux?")


def frozen() -> bool:
	"""
	if BM is in a frozen state (exe), returns True
	\t
	:return: true if it is, otherwise false
	"""
	if getattr(sys, 'frozen', False):
		return True
	else:
		return False


def removeDir(path):
	"""
	remove a folder, including all the files/folders it contains
	:param path: removes a given directory
	"""
	try:
		config.dynConfig['logDeletions']
	except KeyError:
		config.dynConfig['logDeletions'] = True
	# cycle in all subfolders/files
	for file in Path( path ).glob('*'):
		if file.is_dir():
			# RECURSION POWA
			removeDir( file )
		else:
			# remove the file
			os.remove( file )
			if config.dynConfig['logDeletions']:
				logger.debug(f'deleting {file.resolve()}')
	# remove all directories
	for file in Path( path ).glob('*'):
		os.rmdir( file )
		if config.dynConfig['logDeletions']:
			logger.debug(f'deleting {file.resolve()}')
	# and finally, remove the given directory
	os.rmdir( path )


def tmpDirPath() -> str:
	fdr = Path( config.tmpFolderPath )
	if not fdr.exists():
		fdr.mkdir()
	return str( fdr )


def __getbee() -> Union[None, str]:
	# gets the BEE path
	if Path(f'{defBeePath}/BEE2/BEE2.exe').exists():
		return f'{defBeePath}/BEE2/BEE2.exe'  # the exe file exists, bee has been installed, but the BPM config was probably deleted
	return None


def notImplementedYet():
	"""
	shows a dialog that says that this feature its not implemented
	"""
	wx.GenericMessageDialog(
		parent=wx.GetActiveWindow(),
		message=loc('popup.notimplemented.text'),
		caption=loc('popup.notimplemented.title'),
		style=wx.ICON_INFORMATION | wx.STAY_ON_TOP | wx.OK
	).ShowModal()


def parseValue( param: str ) -> Union[str, int, float, None, bool]:
	if ( param == '' ) or ( param in ['none', 'None'] ):
		return None
	elif param.isdecimal():
		return int( param )
	elif param in 'trueTrueyesYes':
		return True
	elif param in 'falseFalsenoNo':
		return False
	for char in param:
		if char not in '0123456789.':
			return param
	return float( param )


def openUrl(url: str):
	"""
	Opens an url with the default browser
	\t
	:param url: the url to open
	"""
	logger.info(f'opening "{url}" with default browser')
	webbrowser.open(url)


defBeePath = str( Path( str( Path( os.getenv('appdata') ).parent ) + '/Local/Programs/').resolve() ).replace(r'\\', '/')
env = 'dev'
