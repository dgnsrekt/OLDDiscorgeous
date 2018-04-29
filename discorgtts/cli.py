import click


@click.group()
def main():
    pass


@main.command('server')
def server():
    click.echo('running server')


@main.command('client')
def client():
    click.echo('running client')


@main.command('sshclient')
def server():
    click.echo('running sshclient')


if __name__ == '__main__':
    main()
