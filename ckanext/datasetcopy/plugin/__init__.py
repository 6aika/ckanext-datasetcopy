import os

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.datasetcopy
from ckan.lib.plugins import DefaultTranslation


try:
    plugins.toolkit.requires_ckan_version("2.9")
except plugins.toolkit.CkanVersionException:
    from ckanext.datasetcopy.plugin.pylons_plugin import MixinPlugin
else:
    from ckanext.datasetcopy.plugin.flask_plugin import MixinPlugin


class DatasetcopyPlugin(MixinPlugin, plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    if toolkit.check_ckan_version(min_version='2.5.0'):
        plugins.implements(plugins.ITranslation, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, '../templates')

    # ITranslation
    def i18n_directory(self):
        u'''Change the directory of the .mo translation files'''
        return os.path.join(
            os.path.dirname(ckanext.datasetcopy.__file__),
            'i18n'
        )