# -*- coding: utf-8 -*-

import click
from wappylyzer import Wappylyzer

WAPPYLYZER_VERSION = '0.1'

@click.group()
@click.version_option(WAPPYLYZER_VERSION)
def cli():
    pass

@cli.command(help='Update apps.json file from Wappalyzer.')
@click.option('-d', '--dest', 'dest_file', type=str, required=False, default='apps.json')
def update(dest_file):
    Wappylyzer.update(dest_file)

@cli.command(help='Analyze target URL.')
@click.option('-d', '--dest', 'dest_file', type=str, required=False, default='apps.json')
@click.option('-u', '--url', 'url', type=str, required=True)
def analyze(dest_file, url):
    w = Wappylyzer(dest_file)
    w.analyze_from_url(url)

if __name__ == '__main__':
    cli()
