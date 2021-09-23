#!/usr/bin/env python

from urllib.parse import urljoin

import requests
import typer
import validators

import fizzbuzz_lib
from constants import (CLASSIC_FIZZBUZZ_PREFIX, N_ARGS_NAME, SEP_ARGS_NAME,
                       STREAM_PATH)


CLASSIC_FIZZBUZZ_COMMAND = 'cfb'
CLASSIC_FIZZBUZZ_FROM_WEB_COMMAND = 'cfbw'

app = typer.Typer(
    help='Run FizzBuzz variants'
)

n_arg = typer.Argument(..., help='The maximum number of the sequence')
sep_arg = typer.Option(
    ' ', help='A separator of each element. A trailing separator will always remain.',
    show_default='SPACE')


@app.command(name=CLASSIC_FIZZBUZZ_COMMAND)
def classic_fizzbuzz(n: int = n_arg, sep: str = sep_arg):
    """Run the classsic FizzBuzz
    """
    typer.echo_via_pager(fizzbuzz_lib.classic_fizzbuzz_as_gen_text(n, sep))


def get_baseurl(value: str):
    value = f'http://{value}'
    if validators.url(value) is not True:
        raise typer.BadParameter('must be in the form [host]:[port][/path]')
    return value


@app.command(name=CLASSIC_FIZZBUZZ_FROM_WEB_COMMAND)
def classic_fizzbuzz_from_web(
    n: int = n_arg, sep: str = sep_arg,
    baseurl: str = typer.Option(
        'localhost:8000',
        help='The full url of the server. Must be in the form [host]:[port][/path]',
        callback=get_baseurl),
    stream: bool = typer.Option(True, help='Whether to use streaming or not')
):
    """Get classic FizzBuzz results from the web
    """
    if stream:
        url = urljoin(f'{baseurl}', f'/{CLASSIC_FIZZBUZZ_PREFIX}/{STREAM_PATH}')
    else:
        url = urljoin(f'{baseurl}', f'/{CLASSIC_FIZZBUZZ_PREFIX}/')
    r = requests.get(url, params={N_ARGS_NAME: n, SEP_ARGS_NAME: sep}, stream=stream)
    typer.echo_via_pager(str(s, r.encoding) for s in r.iter_content(chunk_size=127))


if __name__ == '__main__':
    app()
