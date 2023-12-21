#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PROJECT_DIR=$(realpath "$SCRIPT_DIR/..")
PROTO_DIR="$PROJECT_DIR/robot-test/libs/proto"

cd "$PROTO_DIR"

find . -name "*.proto" -exec protoc --python_out="$PROTO_DIR" {} +
