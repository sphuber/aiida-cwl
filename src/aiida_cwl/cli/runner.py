# -*- coding: utf-8 -*-
"""Command to run a CWL workflow."""
import pathlib

from aiida.cmdline.utils import decorators, echo
import click

from .root import cmd_root


@cmd_root.command('runner')
@click.argument('document', type=click.Path(path_type=pathlib.Path))
@click.argument('parameters', type=click.Path(path_type=pathlib.Path))
@decorators.with_dbenv()
def cmd_runner(document, parameters):
    """Run a CWL command line tool."""
    from ..runner import run

    results, node = run(document, parameters)

    if node.is_finished_ok:
        echo.echo_success(f'{node.process_label}<{node.pk}> finished successfully.')
        echo.echo(f'Results: {results}')
        echo.echo(f'Stdout: {results["stdout"].get_content()}')
    else:
        echo.echo_error(f'{node.process_label}<{node.pk}> failed.')
        echo.echo_error(node.exit_message or 'no exit message available')
        echo.echo(f'Stderr: {results["stderr"].get_content()}')
        echo.echo(f'Stdout: {results["stdout"].get_content()}')
