"""Functional tests."""
import subprocess

import pytest
from molecule import logger
from molecule.util import run_command


LOG = logger.get_logger(__name__)


@pytest.fixture
def scenario_to_test(request):
    return request.param


@pytest.fixture
def driver_name(request):
    return request.param


@pytest.fixture
def scenario_name(request):
    return request.param


def format_result(result: subprocess.CompletedProcess):
    """Return friendly representation of completed process run."""
    return (
        f"RC: {result.returncode}\n"
        + f"STDOUT: {result.stdout}\n"
        + f"STDERR: {result.stderr}\n"
    )


def test_command_init_role_goss_verifier(temp_dir):
    """Verify that init scenario works."""
    cmd = ["molecule", "init", "role", "test-init", "--verifier-name", "goss"]
    assert run_command(cmd).returncode == 0


@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [("docker/centos7", "docker", "default")],
    #    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_scenario_centos7(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "test", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0


@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [("docker/ubuntu18.04", "docker", "default")],
    #    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_scenario_ubuntu18(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "test", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0
