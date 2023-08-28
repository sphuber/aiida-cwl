# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""Tests for the examples."""
import os
import pathlib

import pytest

from aiida_cwl.runner import run


@pytest.fixture(autouse=True)
def chdir(request, filepath_tests):
    """Change the working directory to the example directory for the duration of the test."""
    dirpath_examples = filepath_tests.parent / 'examples'
    dirpath_example = dirpath_examples / request.node.name.removeprefix('test_')

    cwd = pathlib.Path.cwd()

    try:
        os.chdir(dirpath_example)
        yield
    finally:
        os.chdir(cwd)


@pytest.fixture
def run_example():
    """Run the example of the current working directory."""
    dirpath = pathlib.Path.cwd()
    filepath_document = dirpath / 'tool.cwl'
    filepath_parameters = dirpath / 'parameters.yml'

    return run(filepath_document, filepath_parameters)


@pytest.mark.usefixtures('aiida_profile')
def test_01_cli_tool(run_example):
    """Test example ``01_cli_tool``."""
    results, node = run_example
    assert node.is_finished_ok
    assert results['stderr'].get_content() == ''
    assert results['stdout'].get_content() == 'Hello world!\n'


@pytest.mark.usefixtures('aiida_profile')
def test_02_input_arguments(run_example):
    """Test example ``02_input_arguments``."""
    results, node = run_example
    assert node.is_finished_ok
    assert results['stderr'].get_content() == ''
    assert results['stdout'].get_content() == '-f -i=42 --example-string hello --file==example_file\n'


@pytest.mark.usefixtures('aiida_profile')
def test_03_input_files(run_example):
    """Test example ``03_input_files``."""
    results, node = run_example
    assert node.is_finished_ok
    assert results['stderr'].get_content() == ''
    assert results['stdout'].get_content() == ''


@pytest.mark.usefixtures('aiida_profile')
def test_04_stdout(run_example):
    """Test example ``04_stdout``."""
    results, node = run_example
    assert node.is_finished_ok
    assert results['stderr'].get_content() == ''
    assert results['stdout'].get_content() == 'Hello world!\n'


@pytest.mark.usefixtures('aiida_profile')
def test_05_parameter_references(run_example):
    """Test example ``05_parameter_references``."""
    results, node = run_example
    assert node.is_finished_ok
    assert results['stderr'].get_content() == ''
    assert results['stdout'].get_content() == ''
    assert results['file_txt'].get_content() == ''
