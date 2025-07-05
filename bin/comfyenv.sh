#!/bin/bash
CURRENT_DIR=$(dirname $(realpath $0))
$CONDA_DIR/python $CURRENT_DIR/../main.py "$@"