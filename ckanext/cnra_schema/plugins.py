from ckan.plugins import toolkit, IConfigurer, ITemplateHelpers, SingletonPlugin, implements
import json
from markupsafe import Markup


class cnraSchema(SingletonPlugin):
    implements(IConfigurer)
    implements(ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_public_directory(config, "static")
        toolkit.add_template_directory(config, "templates")       
 
        config['scheming.presets'] = """
ckanext.scheming:presets.json
"""

        config['scheming.dataset_schemas'] = """
ckanext.cnra_schema:schemas/dataset.yaml
"""

    # define a dict of custom template functions for this schema
    def get_helpers(self):
        return {
            'confirmjson': _json_decode_recode_string,
        }

# escape a possible JSON string, or else return ""
def _json_decode_recode_string(string):
    try:
        return Markup(json.dumps(json.loads(string)))
    except ValueError:
        return json.dumps(None)
