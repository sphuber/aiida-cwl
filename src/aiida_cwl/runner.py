# -*- coding: utf-8 -*-
"""Module with utilities to run CWL documents through AiiDA."""
import ast
import functools
import pathlib
import re
import typing as t
from typing import TYPE_CHECKING

from pycwl import DocumentParseError, SchemaValidationError, parse_command_line_tool
import yaml

PATTERN_PARAMETER_REFERENCE = re.compile(r'^\s*\$\((.*)\)\s*')

if TYPE_CHECKING:
    from aiida.orm import Data, ProcessNode


def run(document: pathlib.Path, parameters: pathlib.Path) -> tuple[dict[str, 'Data'], 'ProcessNode']:
    """Run a CWL command line tool."""
    from aiida_shell import launch_shell_job

    try:
        tool = parse_command_line_tool(document.read_text())
    except (DocumentParseError, SchemaValidationError) as exception:
        raise ValueError(exception) from exception

    try:
        with open(parameters, encoding='utf-8') as handle:
            parameters_dict = yaml.safe_load(handle)
    except yaml.YAMLError as exception:
        raise ValueError(exception) from exception

    arguments, files = prepare_inputs(tool.inputs, parameters_dict)
    outputs = prepare_outputs(tool.outputs, parameters_dict)

    return launch_shell_job(tool.command, arguments=tool.base_arguments + arguments, nodes=files, outputs=outputs)


def prepare_inputs(input_parameters, parameters: dict[str, t.Any]):
    """Analyze the input specification and apply the concrete parameters on the placeholders.

    :returns: Tuple of a list of command line arguments for the tool and a dictionary of input files.
    """
    arguments: list[str] = []
    files: dict[str, str] = {}

    for parameter in sorted(input_parameters, key=lambda p: p.binding.position):

        try:
            value = parameters[parameter.identifier]
        except KeyError:
            continue

        arguments.extend(parameter.format_arguments(value))
        try:
            files.update(**parameter.format_file_binding(value))
        except AttributeError:
            pass

    return arguments, files


def prepare_outputs(output_parameters, parameters: dict[str, t.Any]) -> list[str]:
    """Analyze the output specification and apply the concrete parameters on the placeholders.

    :returns: List of output files that should be captured.
    """
    outputs: list[str] = []

    for output in output_parameters:

        if output.type == 'File':
            parameter = resolve_parameter_reference(output.binding.glob, parameters)
            outputs.append(parameter)
        elif output.type == 'stdout':
            # The ``stdout`` is always captured and attached as the ``stdout`` output node.
            pass
        else:
            raise ValueError(f'the type `{output.type}` is not supported.')

    return outputs


def resolve_parameter_reference(parameter: str, parameters: dict[str, t.Any]) -> t.Any:
    """Resolve any references in the given ``parameters`` using the ``parameters`` mapping.

    The syntax of a valid parameter reference is any string enclosed by ``$()``. If found in ``parameter``, the string
    will be replaced by the corresponding value taken from the ``parameters`` mapping.
    """
    if (matches := PATTERN_PARAMETER_REFERENCE.search(parameter)) is None:
        return parameter

    reference = matches.group(1)
    parts: list[t.Any] = []

    def extract_parts(expression, parts):
        if isinstance(expression, ast.Subscript):
            parts.append(expression.slice.value)  # type: ignore[attr-defined]
            extract_parts(expression.value, parts)
        elif isinstance(expression, ast.Attribute):
            parts.append(expression.attr)
            extract_parts(expression.value, parts)
        elif isinstance(expression, ast.Name):
            parts.append(expression.id)
        else:
            raise RuntimeError(expression)

    extract_parts(ast.parse(reference).body[0].value, parts)  # type: ignore[attr-defined]

    # The parts are added in reverse order, so we revert them and then pop the first key, which should be ``inputs``.
    parts.reverse()
    parts.pop(0)

    try:
        value = functools.reduce(lambda s, part: s.get(part), parts, parameters)  # type: ignore[arg-type,return-value]
    except AttributeError as exception:
        raise ValueError(
            f'the parameter reference `{parameter}` is not defined in the input parameters: {parameters}'
        ) from exception

    return value
