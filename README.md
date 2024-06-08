# Nillion’s ZKP Protocol PoC
## Overview
I chose to attempt my solution in Python, since that is what I’m most comfortable with.

To implement the Chaum–Pedersen Protocol as outlined in the document, I needed to not only read the sections in the attached book, but also scour through several docs pages and take a look at some existing open source implementations of gRPC. I will try to add any helpful docs to the Resources section.

## Set up Protobuf and gRPC
This information came from the PDF I was sent. The filename is `zkp_auth.proto`, which I used to create the gRPC code from the Protobuf file.

After installing the required dependencies, I used the following command to accomplish that:
```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. zkp_auth.proto
```

This generates `zkp_auth_pb2.py` which contains the generated request and response classes and `zkp_auth_pb2_grpc.py` which contains the generated client and server classes.

## Resources
[IntroToCrypto Book](https://www.cs.umd.edu/~waa/414-F11/IntroToCrypto.pdf)
[gRPC Python Quickstart](https://grpc.io/docs/languages/python/quickstart/)
[gRPC Python Basics Tutorial](https://grpc.io/docs/languages/python/basics/)
