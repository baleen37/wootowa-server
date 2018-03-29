import click
# from wootowa import storage
from wootowa.app import create_app, get_config
from wootowa.storage import dal


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', is_flag=True)
def runserver(d):
    click.echo(f'Run server')
    if d:
        config_obj = get_config('wootowa.config.Config')
    else:
        config_obj = get_config('wootowa.config.Production')

    # init db
    dal.db_init(config_obj.SQLALCHEMY_DATABASE_URI)

    app = create_app(config_obj)
    app.run('0.0.0.0')


@cli.command()
def initdb():
    click.echo('Initialized the database')


@cli.command()
def dropdb():
    click.echo('Dropped the database')


if __name__ == '__main__':
    cli()
