#!/bin/bash
set -e

cd src
rm -rf yamcs/cli/protobuf
mkdir yamcs/cli/protobuf

cp ../../yamcs/yamcs-core/src/main/proto/* yamcs/cli/protobuf

# Some internal protos depend on API types.
# The pb2.py files already exist in yamcs-client dependency,
# so just delete them afterwards.
cp -r ../../yamcs/yamcs-api/src/main/proto/yamcs yamcs/cli/protobuf

cd yamcs/cli/protobuf
protoc --proto_path=. --python_out=. *.proto

rm -rf yamcs
rm *.proto
