"""Pytest Fixtures."""
import os

import pytest
from molecule.test.conftest import random_string, temp_dir  # noqa
from molecule import config, logger, util
from molecule.test.conftest import change_dir_to
from molecule.util import run_command

LOG = logger.get_logger(__name__)


@pytest.fixture
def driver_name():
    """Return name of the driver to be tested."""
    return "docker"


@pytest.fixture
def molecule_project_directory():
    return os.getcwd()


@pytest.fixture
def molecule_directory():
    return config.molecule_directory(molecule_project_directory())


@pytest.fixture
def molecule_scenario_directory():
    return os.path.join(molecule_directory(), "default")


@pytest.fixture
def molecule_file():
    return get_molecule_file(molecule_scenario_directory())


@pytest.fixture
def get_molecule_file(path):
    return config.molecule_file(path)


@pytest.fixture
def with_scenario(request, scenario_to_test, driver_name, scenario_name):
    scenario_directory = os.path.join(
        os.path.dirname(util.abs_path(__file__)), "scenarios", scenario_to_test
    )

    with change_dir_to(scenario_directory):
        yield
        if scenario_name:
            msg = "CLEANUP: Destroying instances for all scenario(s)"
            LOG.info(msg)
            cmd = ["molecule", "destroy", "--driver-name", driver_name, "--all"]
            assert run_command(cmd).returncode == 0
