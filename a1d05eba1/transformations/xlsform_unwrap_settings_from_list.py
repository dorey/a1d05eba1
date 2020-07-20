'''
xlsform_unwrap_settings_from_list:

if settings is a list, pull out the first item.
settings is always a dict
'''

from .transformer import Transformer
from ..utils.kfrozendict import kfrozendict

class UnwrapSettingsFromList(Transformer):
    '''
    when loaded in from an XLSForm, settings is in a 1-item-list

    this will pull the 1st item out of the settings list and update
    the content.settings

    before:
      settings:
        [{'default_language': 'Latin'}]

    after:
      settings:
        {'default_language': 'Latin'}
    '''
    def fw(self, content):
        if 'settings' in content:
            settings = content['settings']
            return content.copy(settings=[settings,])

    def rw(self, content):
        if 'settings' in content:
            settings = content['settings']
            if isinstance(settings, (list, tuple)):
                if len(settings) > 0:
                    settings = settings[0]
                else:
                    settings = {}
            return content.copy(settings=settings)
        return content.copy(settings=kfrozendict())

TRANSFORMER = UnwrapSettingsFromList()
