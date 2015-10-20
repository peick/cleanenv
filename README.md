Clean environment is the logical successor of python's virtualenv.

It's using docker to create a full encapsulated working environment.

The usage is really simple and fully transparent to the user. You will not
even notice that you are working in the environment. All programs can be started
from the _outsite_ as if they were usual programs. They are automatically
wrapped and started in a docker container.


Why not using docker or virtualenv directly
===========================================

Virtualenv not only lacks of full isolation from the host system. You are also
bound the that specific operating system. In some cases you are not allowed to
install and run your own privileged services like a database or use another
version of a software.

Docker - although some people call it the virtualenv killer - lacks of
usability to be a virtualenv replacement. You will always need some handcrafted
scripts to make it handsome.

Cleanenv wraps programs running in docker containers as if they were part of your
host machine. Programs, users and pathes are mapped transparently. You can use
it as a drop-in-replacement to virtualenv.

And it's not strictly bound to python. Everything that you want to transparently
execute isolated can be used with cleanenv. Suppose you need to run a newer or
older version of ruby but cannot upgrade/downgrade your host system version.
Cleanenv creates a shortcut binary for you to let you run it isolated with
your user and pathes mapped.


Create an environment
=====================

    $ cleanenv create <path>

The simple `create` command creates an environment in the path specified.
To enter the environment type:

    $ source <path>/bin/activate

To deactivate, but not destroy, the environment type:

    $ deactivate

On deactivation, all running processes are stopped. If you want to keep them
running, use the --persistent directive on creation.

To start a program, e.g. a mysql server, whenever the environment is activated
use the --on-activate directive. The <program> argument will be executed inside
the container after start up.

    $ cleanenv create --on-activate <program> --on-deactivate <program2> <path>

    (not implemented yet, sorry)

If you plan to use programs inside the environment without entering it, you
should use the --persistent directive. This keeps your container running even
when your programs exits.

Because docker containers are completely isolated to the host system, all
existing users of your host system does not exist in the container. Cleanenv
automatically creates a user inside the docker container that matches the user
who called cleanenv. You can override this settings with the --user directive:

    $ cleanenv create --user [<id>:]<name> <path>

    $ cleanenv create --user system:[<id>:]<name> <path>

Mapping of programs to easily call them from your host machine can be achieved
with the --program directive:

    $ cleanenv create --link <full-path-in-container> <path>

By default, only the root directory of you host system is mounted read-only into
the container under the path `/r`. To override these settings you can provide
a mapping like:

    $ cleanenv create --directory <host-path>:<container-path>[:rw]

If `:rw` is not present, the host-path is mounted read-only. Be careful when
using :rw (full access read and write) mounts. You may alter/delete files in
your host system, because of missing security features in docker.


Configuration file
==================

If you have a complex configuration or you need a reproducable configuration
you can put all above mentioned settings into a .cleanenv.conf file.
When executing `cleanenv create <path>` it searches this file in the current
working directory. Alternatively you can provide a configuration file with
`--config`


Reset the state of an environment
=================================

To cleanup the environment and reuse it without fully destroying the environment
you can use the `cleanenv reset` command.

Internally it stops and removes the docker container.


Proper destroying of an environment
===================================

Cleanenv manages a set of docker images (snapshots), which needs to be removed
when you don't need the environment anymore. To remove them just type:

    $ cleanenv destroy

inside the activated environment or directly:

    $ <path>/bin/destroy


Using snapshots (not implemented yet, sorry)
===============

Snapshots are used to store the current state of the docker container for
rollback and roll-forward of changes.

Set a program to automatically create a snapshot when executed.

    $ cleanenv snapshot configure pip --pattern 'install' --name 'pip-{id}'

List available snapshots:

    $ cleanenv snapshot list

Create a snapshot:

    $ cleanenv snapshot create [<name>]

Restore a snapshot:

    $ cleanenv snapshot <id|name>

To restore the initial start - after creating the cleanenv - use:

    $ cleanenv reset

Be careful when doing this, because all snapshots may get lost on the next
snapshot creation.

To freeze the state of your cleanenv, type:

    $ cleanenv freeze

It creates a docker image with a snapshot history and prevents all upcoming
changes.

    $ cleanenv unfreeze

reverts the freeze state, which means you are free to do any changes.

