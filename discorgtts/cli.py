import click


@click.group()
@click.option('-f', '--filename')  # XXX: <- add default that calls config mod
@click.option('--bind_ip')  # XXX: <- add default that calls config mod
@click.option('--bind_port')  # XXX: <- add default that calls config mod
@click.pass_context
def main(context, filename, bind_ip, bind_port):
    context.obj = {
        'FILENAME': filename,
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


@main.command('client')
@click.pass_context
def client(context):
    # XXX:HOST_ADDRESS, USERNAME, PORT
    click.echo('running client')


@main.command('client-ssh')
@click.pass_context
def clientssh(context):
    click.echo('running sshclient')


@main.command('chat-client-ssh')
@click.pass_context
def sshchatclient(context):
    click.echo('running sshclient')


if __name__ == '__main__':

    logo = """
 __ __      __    __  __       __       __  __     __    __  __      __    ___
|_ /  \|\/|/  \  |  \|__)|\  /|_ |\ |  |  \|_ \  /|_ |  /  \|__)|\/||_ |\ | |
|  \__/|  |\__/  |__/| \ | \/ |__| \|  |__/|__ \/ |__|__\__/|   |  ||__| \| |
    """
    print(logo)

    main()
