from flask import Blueprint, request

from ckan.plugins import toolkit
from ckan import model

from ckan.views.dataset import CreateView, _get_package_type, _get_pkg_template, _setup_template_variables
from flask.views import MethodView

g = toolkit.g
get_action = toolkit.get_action
check_access = toolkit.check_access
NotFound = toolkit.ObjectNotFound
NotAuthorized = toolkit.NotAuthorized
abort = toolkit.abort
_ = toolkit._
h = toolkit.h
render = toolkit.render


import logging
log = logging.getLogger(__name__)

dataset_copy = Blueprint('dataset_copy', __name__, url_defaults={u'package_type': u'dataset'})


class CopyView(MethodView):

    def _prepare(self, id, data=None):
        context = {
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'auth_user_obj': g.userobj,
            u'save': u'save' in request.form
        }
        return context

    def post(self, package_type, id):
        return CreateView().post(package_type)

    def get(self, package_type, id, data=None, errors=None, error_summary=None):
        context = self._prepare(id, data)
        package_type = _get_package_type(id) or package_type
        try:
            pkg_dict = get_action(u'package_show')(
                dict(context, for_view=True), {
                    u'id': id
                }
            )
            context[u'for_edit'] = True
            old_data = get_action(u'package_show')(context, {u'id': id})
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
            return abort(404, _(u'Dataset not found'))
        # are we doing a multiphase add?
        if data.get(u'state', u'').startswith(u'draft'):
            g.form_action = h.url_for(u'{}.new'.format(package_type))
            g.form_style = u'new'

            return CreateView().get(
                package_type,
                data=data,
                errors=errors,
                error_summary=error_summary
            )

        pkg = context.get(u"package")

        try:
            check_access(u'package_update', context)
        except NotAuthorized:
            return abort(
                403,
                _(u'User %r not authorized to edit %s') % (g.user, id)
            )
        # convert tags if not supplied in data
        if data and not data.get(u'tag_string'):
            data[u'tag_string'] = u', '.join(
                h.dict_list_reduce(pkg_dict.get(u'tags', {}), u'name')
            )
        errors = errors or {}
        form_snippet = _get_pkg_template(
            u'package_form', package_type=package_type
        )
        form_vars = {
            u'data': data,
            u'errors': errors,
            u'error_summary': error_summary,
            u'action': u'edit',
            u'dataset_type': package_type,
            u'form_style': u'edit'
        }

        _setup_template_variables(
            context, {u'id': id}, package_type=package_type
        )

        # we have already completed stage 1
        form_vars[u'stage'] = [u'active']
        if data.get(u'state', u'').startswith(u'draft'):
            form_vars[u'stage'] = [u'active', u'complete']

        copy_template = 'datasetcopy/copy.html'
        return render(
            copy_template,
            extra_vars={
                u'form_vars': form_vars,
                u'form_snippet': form_snippet,
                u'dataset_type': package_type,
                u'pkg_dict': pkg_dict,
                u'pkg': pkg,
            }
        )


dataset_copy.add_url_rule('/dataset/copy/<id>', view_func=CopyView.as_view('dataset_copy'))
