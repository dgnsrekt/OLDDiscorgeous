from pathlib import Path
from collections import ChainMap

import toml


class Configuration:
    CONFIG_PATH = Path(__file__).parent.parent / 'config.toml'

    SERVER_DEFAULT = {'channel_id': '000000000000000000',
                      'discord_voice_token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                      'server_ip': '0.0.0.0',
                      'server_port': '0000',
                      'language': 'en-us',
                      'logging': 'DEBUG',
                      'encoder_sample_rate': '48000',
                      'encoder_channel': '1',
                      'max_connections': '5'}

    CLIENT_DEFAULT = {'host_address': '0.0.0.0',
                      'username': 'root',
                      'client_ip': '0.0.0.0',
                      'client_port': '0000',
                      'logging': 'DEBUG'}

    CONFIG_DEFAULT = {'server': SERVER_DEFAULT,
                      'client': CLIENT_DEFAULT}

    def __init__(self):
        self.settings = self.load_config_file()

    @property
    def server_settings(self):
        return self.settings['server']

    @property
    def client_settings(self):
        return self.settings['client']

    def load_config_file(self):
        try:
            with open(Configuration.CONFIG_PATH, 'r') as file:
                return toml.loads(file.read())

        except FileNotFoundError:
            self.create_default_config_file()
            with open(Configuration.CONFIG_PATH, 'r') as file:
                return toml.loads(file.read())

    def force_overwrite_default_settings(self):
        self.create_default_config_file()

    def create_default_config_file(self):
        with open(Configuration.CONFIG_PATH, 'w') as file:
            default_toml = toml.dumps(Configuration.CONFIG_DEFAULT)
            file.write(default_toml)
            print('Config file created with default settings.')
            print(f'{Configuration.CONFIG_PATH}')

    def update_config_file(self, settings):
        assert isinstance(settings, dict), 'Must be a dictionary.'

        server_new = settings.get('server', None)
        client_new = settings.get('client', None)

        server_current = self.settings['server']
        client_current = self.settings['client']

        if server_new:
            server_update = dict(ChainMap(server_new, server_current))
        else:
            server_update = server_current

        if client_new:
            client_update = dict(ChainMap(client_new, client_current))
        else:
            client_update = client_current

        settings_update = toml.dumps({'server': server_update,
                                      'client': client_update})
        with open(Configuration.CONFIG_PATH, 'w') as file:
            file.write(settings_update)

    def __repr__(self):
        return str(self.settings)


def test():
    con = Configuration()
    print(con)
