#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import pytest

from molecule import config
from molecule_goss import goss


@pytest.fixture
def _patched_ansible_verify(mocker):
    m = mocker.patch("molecule.provisioner.ansible.Ansible.verify")
    m.return_value = "patched-ansible-verify-stdout"

    return m


@pytest.fixture
def _patched_goss_get_tests(mocker):
    m = mocker.patch("molecule_goss.goss.Goss._get_tests")
    m.return_value = ["foo.py", "bar.py"]

    return m


@pytest.fixture
def _verifier_section_data():
    return {"verifier": {"name": "goss", "env": {"FOO": "bar"}}}


# NOTE(retr0h): The use of the `patched_config_validate` fixture, disables
# config.Config._validate from executing.  Thus preventing odd side-effects
# throughout patched.assert_called unit tests.
@pytest.fixture
def _instance(_verifier_section_data, patched_config_validate, config_instance):
    return goss.Goss(config_instance)


def test_config_private_member(_instance):
    assert isinstance(_instance._config, config.Config)


def test_default_options_property(_instance):
    assert {} == _instance.default_options


def test_default_env_property(_instance):
    assert "MOLECULE_FILE" in _instance.default_env
    assert "MOLECULE_INVENTORY_FILE" in _instance.default_env
    assert "MOLECULE_SCENARIO_DIRECTORY" in _instance.default_env
    assert "MOLECULE_INSTANCE_CONFIG" in _instance.default_env


@pytest.mark.parametrize("config_instance", ["_verifier_section_data"], indirect=True)
def test_env_property(_instance):
    assert "bar" == _instance.env["FOO"]


def test_name_property(_instance):
    assert "goss" == _instance.name


def test_enabled_property(_instance):
    assert _instance.enabled


@pytest.mark.parametrize("config_instance", ["_verifier_section_data"], indirect=True)
def test_options_property(_instance):
    x = {}

    assert x == _instance.options


@pytest.mark.parametrize("config_instance", ["_verifier_section_data"], indirect=True)
def test_options_property_handles_cli_args(_instance):
    _instance._config.args = {"debug": True}
    x = {}

    # Does nothing.  The `goss` command does not support
    # a `debug` flag.
    assert x == _instance.options


def test_bake(_instance):
    assert _instance.bake() is None


def test_execute(
    patched_logger_info,
    _patched_ansible_verify,
    _patched_goss_get_tests,
    patched_logger_success,
    _instance,
):
    _instance.execute()

    _patched_ansible_verify.assert_called_once_with()

    msg = "Executing Goss tests found in {}/...".format(_instance.directory)
    patched_logger_info.assert_called_once_with(msg)

    msg = "Verifier completed successfully."
    patched_logger_success.assert_called_once_with(msg)


def test_execute_bakes():
    pass
