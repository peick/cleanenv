#!/bin/bash
set -e

bash $1
cd /src
py.test --basetemp=/tmp/pytest ${@:2}
