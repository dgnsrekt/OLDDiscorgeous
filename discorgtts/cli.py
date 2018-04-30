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
@click.pass_context
def server(context):
    # XXX: Args BIND_IP, BIND_PORT, FILE_NAME
    # XXX: Accent -> Random, 'UK', 'US', 'AU'
    # XXX: Discord -> Channel_id,
    click.echo('erver')
    print(context.obj)


@main.command('client')
def client():
    # XXX:HOST_ADDRESS, USERNAME, PORT
    click.echo('running client')


@main.command('sshclient')
def sshclient():
    click.echo('running sshclient')


@main.command('chat')
def chatclient():
    click.echo('running sshclient')


if __name__ == '__main__':
    main()
