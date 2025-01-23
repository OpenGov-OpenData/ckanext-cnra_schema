from flask import Blueprint, make_response

import ckanext.cnra_schema.cnra_schema_utils as utils

cnra_schema = Blueprint('cnra_schema', __name__)


def metadata_download(package_id):
    response = make_response()
    response.headers[u'content-type'] = u'application/octet-stream'
    return utils.metadata_download(package_id, response)


cnra_schema.add_url_rule(
    '/metadata_download/<package_id>',
    view_func=metadata_download
)


def get_blueprints():
    return [cnra_schema]
