
import os
import sys
import xbmc
import xbmcaddon

__addon__ = xbmcaddon.Addon('script.module.osmcsetting.networking')

# Custom modules
sys.path.append(xbmc.translatePath(os.path.join(__addon__.getAddonInfo('path'), 'resources', 'lib')))

import resources.lib.xmltodict as xmltodict


class AdvancedSettingsEditor(object):


	def __init__(self, logging_function=None):

		if logging_function is None:
			self.log = self.null_log

		else:
			self.log = logging_function


	def null_log(self):

		pass


	def parse_advanced_settings(self):
		''' Parses the advancedsettings.xml file. Returns a dict with ALL the details. '''

		user_data = xbmc.translatePath( 'special://userdata')
		loc       = os.path.join(user_data,'advancedsettings.xml')

		null_doc  = {'advancedsettings': {}}

		self.log('advancedsettings file exists = %s' % os.path.isfile(loc))

		if os.path.isfile(loc):

			with open(loc, 'r') as f:
				lines = f.readlines()
			
			if not lines:
				self.log('advancedsettings.xml file is empty')
				return null_doc

			with open(loc, 'r') as f:
				doc = xmltodict.parse(f)

			return doc

		else:
			return null_doc


	def validate_advset_dict(self, dictionary, reject_empty=False):
		''' Checks whether the provided dictionary is fully populated with MySQL settings info.
			If reject_empty is False, then Blank dictionaries are rejected, but dictionaries with no video or music database dicts are passed.
			If reject_empty is True,  then Blank dictionaries are rejected, AND dictionaries with no video or music database dicts are also rejected.'''

		main = dictionary.get('advancedsettings', {})

		if not main:

			return False, 'empty'

		sql_subitems = ['name', 'host', 'port', 'user', 'pass']

		if 'videodatabase' in main:
			# fail if the items aren't filled in or are the default up value
			for item in sql_subitems:
				subitem = main.get('videodatabase',{}).get(item, False)
				if not subitem or subitem == '___ : ___ : ___ : ___':
					return False, 'missing mysql'

		if 'musicdatabase' in main:
			for item in sql_subitems:
				subitem = main.get('musicdatabase',{}).get(item, False)
				if not subitem or subitem == '___ : ___ : ___ : ___':
					return False, 'missing mysql'

		if reject_empty:
			if not any('musicdatabase' in main, 'videodatabase' in main):
				return False, 'empty db fields'

		return True, 'complete'


	def write_advancedsettings(self, loc, dictionary):
		''' Writes the supplied dictionary back to the advancedsettings.xml file '''

		with open(loc, 'w') as f:
			xmltodict.unparse(  input_dict = dictionary, 
								output = f, 
								pretty = True)
