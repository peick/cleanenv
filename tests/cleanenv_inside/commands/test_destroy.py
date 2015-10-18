import shutil
from flexmock import flexmock

from cleanenv.cleanenv_inside import cli
from cleanenv.cleanenv_inside.commands import destroy, reset


def test_get_plugin():
    plugin = cli._get_plugin(destroy)
    assert plugin


def test_run_command(tmpdir):
    home_dir = tmpdir.strpath
    options = flexmock(environment_path=home_dir)
    flexmock(reset).should_receive('run_command').once()
    flexmock(shutil).should_receive('rmtree').with_args(home_dir)

    destroy.run_command(options)

