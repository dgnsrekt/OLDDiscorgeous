import click

import config


@click.group()
@click.option('--bind_ip')  # XXX: <- add default that calls config mod
@click.option('--bind_port')  # XXX: <- add default that calls config mod
@click.pass_context
def main(context, filename, bind_ip, bind_port):
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


@main.command('chat-ssh')
@click.pass_context
def sshchatclient(context):
    click.echo('running sshclient')


@main.command('chat-local')
@click.pass_context
def localchatclient(context):
    click.echo('running sshclient')


@main.command('create-config')
def createconfig():
    '''Create a default config file'''
    click.echo('creating blank configuration file.')
    config.create_default_config_file()


if __name__ == '__main__':

    logo = """
 __ __      __    __  __       __       __  __     __    __  __      __    ___
|_ /  \|\/|/  \  |  \|__)|\  /|_ |\ |  |  \|_ \  /|_ |  /  \|__)|\/||_ |\ | |
|  \__/|  |\__/  |__/| \ | \/ |__| \|  |__/|__ \/ |__|__\__/|   |  ||__| \| |
    """
    print(logo)

    main()
