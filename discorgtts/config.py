from pathlib import Path
from collections import ChainMap

import toml

LOCAL_CONFIG = Path(__file__).parent.parent / 'config.toml'


def create_default_config():
    server_config = {'channel_id': '000000000000000000',
                     'discord_voice_token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                     'bind_ip': '0.0.0.0',
                     'bind_port': '0000',
                     'language': 'eu',
                     'logging': 'DEBUG',
                     'encoder_sample_rate': '48000',
                     'encoder_channel': '1',
                     'buffer_size': '4096',
                     'max_connections': '5'}

    client_config = {'host_address': '0.0.0.0',
                     'username': 'root',
                     'port': '0000',
                     'logging': 'DEBUG'}

    full_config = {'server': server_config,
                   'client': client_config}

    toml_config = toml.dumps(full_config)
    return toml_config


def create_default_config_file():
    with open(LOCAL_CONFIG, 'w') as file:
        file.write(create_default_config())


def load_config_file():
    if LOCAL_CONFIG.exists():
        with open(LOCAL_CONFIG, 'r') as file:
            return toml.loads(file.read())
    raise Exception(f'{LOCAL_CONFIG} Does not exist.')


def make_backup_config_file():
    if LOCAL_CONFIG.exists():
        back_up_config_file = LOCAL_CONFIG.with_suffix('.bak')
        with open(back_up_config_file, 'w') as file:
            data = load_config_file()
            file.write(toml.dumps(data))
