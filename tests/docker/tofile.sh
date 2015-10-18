#!/bin/bash
RELTO=$1
DISTDIR=$2
OUT=$3

function newpath() {
    if echo $1 | grep -F "$DISTDIR" 2>&1 >/dev/null; then
        echo "'/.toxdist/$(realpath --relative-to $DISTDIR $1)'"
    elif echo $1 | grep -F "$RELTO" 2>&1 >/dev/null; then
        echo "'/src/$(realpath --relative-to $RELTO $1)'"
    else
        echo "'$1'"
    fi
}

DEPS=""

for v in ${@:4}; do
    DEPS="$DEPS $(newpath $v)"
done

if [ -n "$DEPS" ]; then
    echo pip install $DEPS >> $OUT
fi
