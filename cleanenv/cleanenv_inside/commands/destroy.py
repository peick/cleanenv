"""Complete destroys the environment:

    * remove all created images and container (like reset command)
    * removes the directory
"""
from __future__ import print_function
import os
import shutil

from . import reset


NEEDS_ENVIRONMENT = True


def run_command(options):
    if os.path.exists(options.environment_path):
        print("Destroying %s" % options.environment_path)
        reset.run_command(options)
        shutil.rmtree(options.environment_path)

