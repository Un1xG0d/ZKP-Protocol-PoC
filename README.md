# Nillion’s ZKP Protocol PoC
## Overview
I chose to attempt my solution in Python, since that is what I have the most years of experience with.

To implement the Chaum–Pedersen Protocol as outlined in the [attached document](https://github.com/Un1xG0d/Nillion-ZKP-Protocol-PoC/blob/master/Nillion_Technical_Test_V4.pdf), I needed to not only read the sections of the book that were linked, but also analyze several documentation pages and take a look at some existing open source implementations of gRPC. I will try to add any helpful docs to the Resources section.

## Set up Protobuf and gRPC
The Protobuf definition came from the PDF I received with the project requirements. The filename of the definition is `zkp_auth.proto`, which I used to create the gRPC code.

After installing the required dependencies, I used the following command to accomplish that:
```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. zkp_auth.proto
```

This generates `zkp_auth_pb2.py` which contains the generated request and response classes, and `zkp_auth_pb2_grpc.py` which contains the generated client and server classes.

## Client implementation
The client script consists of two primary functions:
1. **Register**: Calculates y1 and y2 using the secret x and public values g and h, and sends them to the server.
2. **Authenticate**: Initiates the challenge-response protocol and verifies the response from the server.

Most of the variable and function names were given to me from either the requirements document, the supplied Protobuf definition or the equations referenced in the book, so after configuring a basic gRPC setup, most of what I had to do was plug in the variables and equations given to me.

Since there was no specific requirement to allow user input, I hardcoded the variables for user, x, g, and h; however this can be easily amended if needed. The variables g and h are the public values used both in the client and server scripts.

## Resources
[IntroToCrypto Book](https://www.cs.umd.edu/~waa/414-F11/IntroToCrypto.pdf)

[gRPC Python Quickstart](https://grpc.io/docs/languages/python/quickstart/)

[gRPC Python Basics Tutorial](https://grpc.io/docs/languages/python/basics/)

[Implementing gRPC In Python: A Step-by-step Guide](https://www.velotio.com/engineering-blog/grpc-implementation-using-python)
