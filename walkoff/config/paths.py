from os.path import join
from os.path import abspath
from os.path import sep
import json

walkoff_internal = abspath(__file__).rsplit(sep, 2)[0]

ext_json = join(walkoff_internal, 'config', 'external_paths.json')
with open(ext_json, 'r') as f:
    walkoff_external = json.load(f)["walkoff_external"]
    walkoff_external = abspath(walkoff_external)
    if walkoff_external == "":
        raise ValueError("walkoff_external path has not been defined, run 'walkoff setup' first.")


data_path = join(walkoff_external, 'walkoff_data')

installed_apps_path = join(walkoff_external, 'walkoff_apps')
installed_interfaces_path = join(walkoff_external, 'walkoff_interfaces')

base_apps_path = join(walkoff_internal, 'appbase')
base_interfaces_path = join(walkoff_internal, 'interfacebase')

api_path = join(walkoff_internal, 'api')
case_db_path = join(data_path, 'events.db')

templates_path = join(walkoff_internal, 'templates')
client_path = join(walkoff_internal, 'client')
config_path = join(data_path, 'config')
db_path = join(data_path, 'db')
default_appdevice_export_path = join(data_path, 'appdevice.json')
default_case_export_path = join(data_path, 'cases.json')
device_db_path = join(data_path, 'devices.db')
keywords_path = join(walkoff_internal, 'keywords')
logging_config_path = join(data_path, 'log', 'logging.json')

walkoff_schema_path = join(data_path, 'walkoff_schema.json')
workflows_path = join(walkoff_external, 'walkoff_workflows')

keys_path = join(walkoff_external, '.certificates')
certificate_path = join(keys_path, 'walkoff.crt')
private_key_path = join(keys_path, 'walkoff.key')
zmq_private_keys_path = join(keys_path, 'private_keys')
zmq_public_keys_path = join(keys_path, 'public_keys')

