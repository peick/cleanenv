#!/bin/bash
set -e

source $1
cd /src
py.test --basetemp=/tmp/pytest ${@:2}
