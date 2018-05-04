from multiprocessing import Pool
from pathlib import Path
import os

from config import Configuration

import click

SERVER_IN_FILEPATH = Path(__file__).parent / 'server_in.py'
SERVER_OUT_FILEPATH = Path(__file__).parent / 'server_out.py'
SERVER_PROCESSES = (f'{SERVER_OUT_FILEPATH}', f'{SERVER_IN_FILEPATH}')

_config = Configuration()


def run_process(process):
    os.system(f'python3 {process}')


@click.group()
def main():
    pass


@main.command('server')
def server():
    click.echo('running server...')
    pool = Pool(processes=2)
    pool.map(run_process, SERVER_PROCESSES)


@main.command('chat-ssh')
def sshchatclient():
    click.echo('running sshclient')


@main.command('chat-local')
def localchatclient():
    click.echo('running sshclient')


def client_settings():
    store_settings = dict()
    for key, value in _config.client_settings.items():
        store_settings[key] = click.prompt(f'{key}:', default=value)
    return {'client': store_settings}


def server_settings():
    store_settings = dict()
    for key, value in _config.server_settings.items():
        store_settings[key] = click.prompt(f'{key}:', default=value)
    return {'server': store_settings}


def create_config_file():
    '''Creates a blank default config file'''
    click.echo('creating blank configuration file.')
    config.create_default_config_file()


@main.command('settings')  # TODO: Change to configuration This
@click.option('--server', is_flag=True, help='Sets server settings in configfile.')
@click.option('--client', is_flag=True, help='Sets client settings in configfile.')
@click.option('--default', is_flag=True, help='Returns settings back to default in configfile.')
def settings(server, client, default):
    if not any((server, client, default)):
        click.echo('run setting --help for options')
    if server:
        new_server_settings = server_settings()
        _config.update_config_file(new_server_settings)
    if client:
        new_client_settings = client_settings()
        _config.update_config_file(new_client_settings)
    if default:
        _config.force_overwrite_default_settings()


if __name__ == '__main__':

    logo = """
 __ __      __    __  __       __       __  __     __    __  __      __    ___
|_ /  \|\/|/  \  |  \|__)|\  /|_ |\ |  |  \|_ \  /|_ |  /  \|__)|\/||_ |\ | |
|  \__/|  |\__/  |__/| \ | \/ |__| \|  |__/|__ \/ |__|__\__/|   |  ||__| \| |
    """
    print(logo)

    main()
