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

# Detect OS and set sed command
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS (BSD sed)
  SED_CMD=(sed -i '')
else
  # Linux (GNU sed)
  SED_CMD=(sed -i)
fi

# This targets the 'from google.protobuf' string and redirects it to the vendor folder
find . -name "*_pb2.py" -exec "${SED_CMD[@]}" \
    -e 's/^from google\.protobuf/from yamcs.protobuf._vendor.google.protobuf/g' \
    -e 's/^import google\.protobuf/import yamcs.protobuf._vendor.google.protobuf/g' {} +
