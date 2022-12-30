import ckan.plugins as p


class MixinPlugin(p.SingletonPlugin):
    p.implements(p.IRoutes, inherit=True)

    # IRoutes

    def before_map(self, map):
        map.connect('/dataset/copy/:id',
                    controller='ckanext.datasetcopy.controller:DatasetcopyController',
                    action='copy_package')

        return map
