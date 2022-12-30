import ckan.plugins as p
from ckanext.datasetcopy.views import dataset_copy


class MixinPlugin(p.SingletonPlugin):
    p.implements(p.IBlueprint)

    def get_blueprint(self):
        return dataset_copy
