#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROTO_DIR="${ROOT}/tests/config/proto"
OUT_DIR="${ROOT}/tests/config/generated_proto"

protoc -I "${PROTO_DIR}" --python_out="${OUT_DIR}" "${PROTO_DIR}/protobuf.proto"

if command -v grpc_python_plugin >/dev/null 2>&1; then
  protoc -I "${PROTO_DIR}" \
    --grpc_python_out="${OUT_DIR}" \
    --plugin=protoc-gen-grpc_python="$(command -v grpc_python_plugin)" \
    "${PROTO_DIR}/protobuf.proto"
fi

echo "Generated protobuf stubs in ${OUT_DIR}"
