from ckan.plugins import toolkit, IConfigurer, SingletonPlugin, implements

class cnraSchema(SingletonPlugin):
    implements(IConfigurer)

    def update_config(self, config):
        toolkit.add_public_directory(config, "static")
        toolkit.add_template_directory(config, "templates")       
 
        config['scheming.presets'] = """
ckanext.scheming:presets.json
"""

        config['scheming.dataset_schemas'] = """
ckanext.cnra_schema:schemas/dataset.yaml
"""
