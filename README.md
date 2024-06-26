# ZKP Protocol PoC
## Overview
I chose to attempt my solution in Python, since that is what I have the most years of experience with.

To implement the Chaum–Pedersen Protocol as outlined in the [attached document](https://github.com/Un1xG0d/ZKP-Protocol-PoC/blob/master/Technical_Test_V4.pdf), I needed to not only read the sections of the book that were linked, but also analyze several documentation pages and take a look at some existing open source implementations of gRPC. I will try to add any helpful docs to the Resources section.

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

## Server implementation
Other than the gRPC setup stuff, the server script has three main functions:
1. **Register**: Stores the y1 and y2 values calculated by the client.
2. **CreateAuthenticationChallenge**: Generates a challenge c and stores it along with r1 and r2.
3. **VerifyAuthentication**: Checks the prover's response using the challenge and returns a session ID based on the verification.

## Functional test
I included a bunch of print statements to debug most steps of the process for when things didn’t work properly, but if everything works as expected, you should see something similar to the following outputs:
### Server output
```
Registered test_user: y1=1152921504606846976, y2=4352281909005599932
Challenge for test_user: auth_id=test_user_8836, r1=1152921504606846976, r2=4352281909005599932, c=69261
Verification: g^s=2251799813685248, r1 * y1^c=2251799813685248, h^s=3618114605990078510, r2 * y2^c=3618114605990078510
```

### Client output
```
Registering test_user: y1=1152921504606846976, y2=4352281909005599932
Register Response:
Authenticating test_user: r1=1152921504606846976, r2=4352281909005599932
Challenge: auth_id=test_user_8836, c=69261, s=855039390
Authentication Response: session_id: "valid_session"
```

## Unit tests
I included two scripts using the Python `unittest` module. One to test the client script and one to test the server script.

You can run these tests using the following command:
```
python3 -m unittest discover -s . -p "test_*.py"
```

There are also many ways to accomplish this using the `grpcio-testing` library, but the method I chose was a bit cleaner.

## Deploy on Docker
This repo includes two Dockerfiles; one for the server and one for the client. The `docker-compose.yml` file will manage both containers. To deploy the containers, simply use the command:
```
docker-compose up --build
```

In the client script, I used an environment variable called HOST to determine which value it should use, whether the app is deployed in Docker or on the local machine.

If this deploys successfully, you should get output similar to the following:
```
Attaching to client-1, server-1
client-1  | Registering test_user: y1=1152921504606846976, y2=4352281909005599932
client-1  | Register Response:
client-1  | Authenticating test_user: r1=1152921504606846976, r2=4352281909005599932
client-1  | Challenge: auth_id=test_user_6133, c=54388, s=671432205
client-1  | Authentication Response: session_id: "valid_session"
client-1  |
client-1 exited with code 0
```

## Deploy on AWS
There are several ways to deploy this code to AWS. I could either deploy the scripts in containers to EKS, but since the requirements stated "the client in one machine and the server in another machine" I assumed this to mean separate EC2 machines. I built this to be deployed on two EC2 instances with Terraform, however, this can be easily ammended to use EKS if needed.

The `main.tf` file holds all the resource definitions. There are also two setup scripts to configure each of the EC2 instances.

This uses a keypair stored on my personal AWS account, but you can properly configure SSH to connect to the new instances if you generate a keypair called `zkp_test.pem`.

To start the deployment, use the commands:
```
terraform init
terraform apply
```

If this works correctly, you should be able to remote into the instances and see the expected script output in a file called `output.txt`.

## Bonus requirements
:white_check_mark: Unit tests

:white_check_mark: Functional test of the ZKP Protocol

:white_check_mark: A setup to run the Client and the Server

:white_check_mark: Code organization

:white_check_mark: Code quality 

:white_check_mark: Well documented code

:white_check_mark: Each instance runs in a separated docker container and have a docker compose to run the setup 

:white_check_mark: There is code to deploy the two containers in AWS. The client in one machine and the
server in another machine

## Resources
[IntroToCrypto Book](https://www.cs.umd.edu/~waa/414-F11/IntroToCrypto.pdf)

[gRPC Python Quickstart](https://grpc.io/docs/languages/python/quickstart/)

[gRPC Python Basics Tutorial](https://grpc.io/docs/languages/python/basics/)

[Implementing gRPC In Python: A Step-by-step Guide](https://www.velotio.com/engineering-blog/grpc-implementation-using-python)

[A Simpler Explanation of Chaum-Pederson](https://medium.com/asecuritysite-when-bob-met-alice/to-the-builders-of-our-future-meet-the-chaum-pedersen-non-interactive-zero-knowledge-proof-method-9846dee47fbc)

[How To Use unittest to Write a Test Case for a Function in Python](https://www.digitalocean.com/community/tutorials/how-to-use-unittest-to-write-a-test-case-for-a-function-in-python)

[Terraform AWS Instance Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance)

[Terraform AWS Security Group Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group)

[How To Create A Terraform EC2 Instance On AWS](https://www.bacancytechnology.com/blog/terraform-ec2-instance-on-aws)
