"""DEPRECATED: Detect and analyze modules, functions, and classes."""

from modulefinder import ModuleFinder
from pathlib import Path

from isort import place_module
from importlib import util

import importlib
import pkgutil

from os import path
from glob import glob
import sys

from typing import Any
from typing import List

analyzed_test_files = {}


def add_sys_path(requested_path: str) -> None:
    """Add the requested_path to the sys.path."""
    sys.path.insert(0, requested_path)


def import_submodules(start_path, include_start_directory=True):
    start_path = path.abspath(start_path)
    pattern = "**/*.py" if include_start_directory else "*/**/*.py"
    py_files = [
        f
        for f in glob(path.join(start_path, pattern), recursive=True)
        if not f.endswith("__.py")
    ]
    for py_file in py_files:
        spec = util.spec_from_file_location("", py_file)
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)


def import_submodules_pkgutil(package, recursive=True):
    """Import submodules in recursive fashion using pkgutil."""
    # Reference:
    # https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules_pkgutil(full_name))
    return results


def collect_program_modules(
    project_directory_path: Path, program_name: str
) -> List[Any]:
    """Find imported modules recursively by starting at the provided directory."""
    add_sys_path(str(project_directory_path / program_name))
    print(f"This is the sys.path: {sys.path}")
    importlib.import_module(program_name)
    # import_submodules_pkgutil(program_name)
    results_dictionary = import_submodules_pkgutil(program_name, True)
    print(results_dictionary)


def find_imported_modules_of_test_suite_file(test_suite_file_path: Path) -> None:
    """Find all of the modules imported by a specific test file."""
    global analyzed_test_files
    module_finder = ModuleFinder()
    module_finder.run_script(str(test_suite_file_path))
    test_suite_file_path_str = str(test_suite_file_path)
    if test_suite_file_path_str not in analyzed_test_files:
        analyzed_test_files[test_suite_file_path_str] = True
        print(
            f"---> starting to analyze the loaded modules of {test_suite_file_path_str}:"
        )
        for name, mod in module_finder.modules.items():
            # print(f"-----> predicting to place the module {name} in {place_module(name)}")
            if (
                name not in sys.stdlib_module_names
                and place_module(name) == "THIRDPARTY"
            ):
                print("-------> likely confirmed it is part of the application!")
                print("-------> %s:" % name, end="\n")
                created_application_module = importlib.import_module(name)
                print(f"-------> details about module: {created_application_module}")
