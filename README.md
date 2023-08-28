# `aiida-cwl`

AiiDA plugin turning AiiDA into a Common Worfklow Language (CWL) engine.

[![PyPI version](https://badge.fury.io/py/aiida-cwl.svg)](https://badge.fury.io/py/aiida-cwl)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/aiida-cwl.svg)](https://pypi.python.org/pypi/aiida-cwl/)
[![Build Status](https://github.com/sphuber/aiida-cwl/workflows/ci/badge.svg?event=push)](https://github.com/sphuber/aiida-cwl/actions)
[![Docs status](https://readthedocs.org/projects/aiida-cwl/badge)](http://aiida-cwl.readthedocs.io/)

This plugin is currently in development and a pre-alpha stage.
The plugin does not support the complete Common Workflow Language spec.
To get an idea of what functionality is supported, please refer to the examples.


## Installation

The recommended method of installation is through the [`pip`](https://pip.pypa.io/en/stable/) package installer for Python:

    pip install aiida-cwl


## Usage

To use `aiida-cwl`, a configured AiiDA profile is required.
The `verdi` CLI of AiiDA provides a command that attempts to automatically create one:

    verdi quicksetup

Please refer to the [AiiDA's documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/get_started.html) for more detailed instructions.
Once an AiiDA profile is available, there are two ways of running a CWL workflow:

* Application programming interface (API) in Python
* Command line interface (CLI)

### API

The `aiida-cwl` provides a Python API to run CWL documents.
The `aiida_cwl.run` function requires the filepath to the workflow definition file and the input parameters.
For example, imagine there is a workflow definition in `tool.cwl` and the parameters are defined in `parameters.yml`, the workflow can be run as follows:

```python
import pathlib
from aiida_cwl import run

filepath_document = pathlib.Path('tool.cwl')
filepath_parameters = pathlib.Path('parameters.yml')

results, node = run(filepath_document, filepath_parameters)

assert node.is_finished_ok
print(results['stdout'].get_content())
```
The `run` function returns a tuple where the first element is a dictionary of the parsed output nodes, and the second element is a `ProcessNode` which represents the execution of the workflow in AiiDA's provenance graph.
The stdout of the tool is always captured and automatically attached as the `stdout` output node.

> **Warning**
> Filepaths in the workflow definition or parameter file are taken to be relative with respect to the current working directory when the workflow is executed.

### CLI

The `aiida-cwl` package ships with the likely named CLI `aiida-cwl`.
It is a small wrapper around the Python API.
To run a CWL workflow, simply pass its filepath, as well as that of the parameters file to the `aiida-cwl runner` command:

    aiida-cwl runner tool.cwl parameters.yml

The command will print the status of the executed tool as well as the generated outputs and content of stdout:

    Success: ShellJob<echo@localhost><90815> finished successfully.
    Results: {
        'stderr': <SinglefileData: uuid: a771eaf4-a976-4019-bc4e-37eb9e050b14 (pk: 90818)>,
        'stdout': <SinglefileData: uuid: f8736c8e-43c8-4ace-b48c-8e9a410a7949 (pk: 90819)>
    }
    Stdout: Hello world!

## Examples

The `examples` directory of this repository contains various examples of CWL workflows that are supported by `aiida-cwl`.


## License
The `aiida-cwl` plugin package is released under the MIT license.
See the `LICENSE.txt` file for more details.
