import click
from flask import Flask
from myApp import my_app

app = Flask(__name__)


def upper(ctx, param, value):
    if value is not None:
        return value.upper()


@app.cli.command('hello', help='Test script')
@click.option('--name', default='World', callback=upper, help='Input your name')
def test_command(name):
    click.echo(f'Hello, {name}!')


@app.cli.command('root_path', help='Show root path')
def root_path():
    click.echo(my_app.root_path)
