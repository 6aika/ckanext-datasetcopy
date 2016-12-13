import logging

import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.plugins

from ckan.common import _, request, c
from ckan.controllers.package import PackageController

log = logging.getLogger(__name__)

render = base.render
abort = base.abort

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
check_access = logic.check_access
get_action = logic.get_action

lookup_package_plugin = ckan.lib.plugins.lookup_package_plugin

class DatasetcopyController(PackageController):

    def _copy_template(self):
        return 'datasetcopy/copy.html'

    def copy_package(self, id, data=None, errors=None, error_summary=None):
        package_type = self._get_package_type(id)
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'auth_user_obj': c.userobj,
                   'save': 'save' in request.params}

        if context['save'] and not data:
            return self._save_new(context, package_type=package_type)
        try:
            c.pkg_dict = get_action('package_show')(dict(context,
                                                         for_view=True),
                                                    {'id': id})
            context['for_edit'] = True
            old_data = get_action('package_show')(context, {'id': id})
            # old data is from the database and data is passed from the
            # user if there is a validation error. Use users data if there.
            if data:
                old_data.update(data)
            data = old_data

            # Remove fields which can not be copied
            if 'id' in data.keys():
                del data['id']
            if 'resources' in data.keys():
                del data['resources']
            if 'name' in data.keys():
                del data['name']

        except (NotFound, NotAuthorized):
            abort(404, _('Dataset not found'))
        # are we doing a multiphase add?
        if data.get('state', '').startswith('draft'):
            c.form_action = h.url_for(controller='package', action='new')
            c.form_style = 'new'
            return self.new(data=data, errors=errors,
                            error_summary=error_summary)

        c.pkg = context.get("package")
        c.resources_json = h.json.dumps(data.get('resources', []))

        try:
            check_access('package_update', context)
        except NotAuthorized:
            abort(403, _('User %r not authorized to edit %s') % (c.user, id))
        # convert tags if not supplied in data
        if data and not data.get('tag_string'):
            data['tag_string'] = ', '.join(h.dict_list_reduce(
                c.pkg_dict.get('tags', {}), 'name'))
        errors = errors or {}
        form_snippet = self._package_form(package_type=package_type)
        form_vars = {'data': data, 'errors': errors,
                     'error_summary': error_summary, 'action': 'edit',
                     'dataset_type': package_type,
                     }
        c.errors_json = h.json.dumps(errors)

        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        # we have already completed stage 1
        form_vars['stage'] = ['active']
        if data.get('state', '').startswith('draft'):
            form_vars['stage'] = ['active', 'complete']

        copy_template = self._copy_template()
        return render(copy_template,
                      extra_vars={'form_vars': form_vars,
                                  'form_snippet': form_snippet,
                                  'dataset_type': package_type})
