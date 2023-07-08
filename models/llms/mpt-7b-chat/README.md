# MPT-7b-chat


### Build the protos

- run from the ~/protos directory

`python -m grpc_tools.protoc -Icompletion --python_out=completion --pyi_out=completion --grpc_python_out=completion completion/completion.proto`

`python -m grpc_tools.protoc -Ichat --python_out=chat --pyi_out=chat --grpc_python_out=chat chat/chat.proto`

- Then move the 3 files (`_pb2.py`, `_pb2.pyi`, `_pb2_grpc.py`) to the respective 