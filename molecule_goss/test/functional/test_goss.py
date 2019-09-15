import os
import sh
import pytest
from conftest import change_dir_to


def test_command_init_role_goss(temp_dir):
    role_directory = os.path.join(temp_dir.strpath, 'test-init')
    options = {'role_name': 'test-init', 'verifier_name': 'goss'}
    cmd = sh.molecule.bake('init', 'role', **options)
    pytest.helpers.run_command(cmd)
    pytest.helpers.metadata_lint_update(role_directory)

    with change_dir_to(role_directory):
        cmd = sh.molecule.bake('test')
        pytest.helpers.run_command(cmd)


def test_command_init_scenario_goss(temp_dir):
    role_directory = os.path.join(temp_dir.strpath, 'test-init')
    options = {'role_name': 'test-init'}
    cmd = sh.molecule.bake('init', 'role', **options)
    pytest.helpers.run_command(cmd)
    pytest.helpers.metadata_lint_update(role_directory)

    with change_dir_to(role_directory):
        molecule_directory = pytest.helpers.molecule_directory()
        scenario_directory = os.path.join(molecule_directory, 'test-scenario')
        options = {
            'scenario_name': 'test-scenario',
            'role_name': 'test-init',
            'verifier_name': 'goss',
        }
        cmd = sh.molecule.bake('init', 'scenario', **options)
        pytest.helpers.run_command(cmd)

        assert os.path.isdir(scenario_directory)
