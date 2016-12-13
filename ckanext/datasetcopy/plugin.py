import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class DatasetcopyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')

    # IRoutes

    def before_map(self, map):
        map.connect('/dataset/copy/:id',
                    controller='ckanext.datasetcopy.controller:DatasetcopyController',
                    action='copy_package')

        return map