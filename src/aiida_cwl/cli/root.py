# -*- coding: utf-8 -*-
"""Command line interface ``aiida-cwl``."""
from aiida.cmdline.groups.verdi import VerdiCommandGroup
import click


@click.group('aiida-cwl', cls=VerdiCommandGroup, context_settings={'help_option_names': ['-h', '--help']})
def cmd_root():
    """CLI for the ``aiida-cwl`` plugin."""
