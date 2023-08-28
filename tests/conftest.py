# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""Configuration and fixtures for unit test suite."""
import pathlib

import pytest

pytest_plugins = ['aiida.manage.tests.pytest_fixtures']  # pylint: disable=invalid-name


@pytest.fixture
def filepath_tests() -> pathlib.Path:
    """Return the absolute filepath to the ``tests`` directory.

    :return: Path to the ``tests`` directory.
    """
    return pathlib.Path(__file__).resolve().parent
