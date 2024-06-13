#!/bin/bash
# Update and install necessary packages
sudo yum update -y
sudo yum install -y python3 python3-pip git

# Install dependencies
sudo pip3 install grpcio grpcio-tools

# Create a directory for the server
mkdir /home/ec2-user/server
cd /home/ec2-user/server

# Download the server.py script from GitHub
wget https://raw.githubusercontent.com/Un1xG0d/ZKP-Protocol-PoC/master/server.py

# Download gRPC generated files
wget https://raw.githubusercontent.com/Un1xG0d/ZKP-Protocol-PoC/master/zkp_auth_pb2.py
wget https://raw.githubusercontent.com/Un1xG0d/ZKP-Protocol-PoC/master/zkp_auth_pb2_grpc.py

# Run the server
python3 server.py > output.txt
