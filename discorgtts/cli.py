import click

from pathlib import Path
import config
import os
from multiprocessing import Pool

SERVER_IN_FILEPATH = Path(__file__).parent / 'server_in.py'
SERVER_OUT_FILEPATH = Path(__file__).parent / 'server_out.py'

print(SERVER_IN_FILEPATH.exists())
print(SERVER_OUT_FILEPATH.exists())
SERVER_PROCESSES = (f'{SERVER_OUT_FILEPATH}', f'{SERVER_IN_FILEPATH}')


def run_process(process):
    os.system(f'python3 {process}')


@click.group()
@click.option('--bind_ip')  # XXX: <- add default that calls config mod
@click.option('--bind_port')  # XXX: <- add default that calls config mod
@click.pass_context
def main(context, bind_ip, bind_port):
    context.obj = {
        'BIND_IP': bind_ip,
        'BIND_PORT': bind_port
    }
    pass


@main.command('server')
@click.option('--accent')  # XXX: <- add default that calls config mod
@click.pass_context
def server(context, accent):

    # XXX: Args BIND_IP, BIND_PORT, FILE_NAME
    # XXX: Accent -> Random, 'UK', 'US', 'AU'
    # XXX: Discord -> Channel_id,
    click.echo('server')
    click.echo(accent)
    print(context.obj)
    pool = Pool(processes=2)
    pool.map(run_process, SERVER_PROCESSES)


@main.command('chat-ssh')
@click.pass_context
def sshchatclient(context):
    click.echo('running sshclient')


@main.command('chat-local')
@click.pass_context
def localchatclient(context):
    click.echo('running sshclient')


@main.command('create-config')  # TODO: Change to configuration This
def createconfig():
    '''Create a default config file'''
    click.echo('creating blank configuration file.')
    config.create_default_config_file()
# TODO: This will create a file if it doesnt exists
# TODO: also if a flag is set it will change the option in the toml file
# TODO: --clean-config-file : Creates a default config moves last config to .bak


if __name__ == '__main__':

    logo = """
 __ __      __    __  __       __       __  __     __    __  __      __    ___
|_ /  \|\/|/  \  |  \|__)|\  /|_ |\ |  |  \|_ \  /|_ |  /  \|__)|\/||_ |\ | |
|  \__/|  |\__/  |__/| \ | \/ |__| \|  |__/|__ \/ |__|__\__/|   |  ||__| \| |
    """
    print(logo)

    main()
