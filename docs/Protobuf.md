# Create new Model


## Generate a stubbed out Python server

```shell
pip install grpc-tools
```


To create the generated files use this call
```shell
python -m grpc_tools.protoc --proto_path=proto generate.proto --python_out=llms/repeater  --pyi_out=llms/repeater --grpc_python_out=llms/repeater
```

which creates the following files
* generate_pb2_grpc.py
* generate_pb2.py
* generate_pb2.pyi

and then those objects are used in the `repeater.py` to implement the grpc service