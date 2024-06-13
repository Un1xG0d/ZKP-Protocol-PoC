#!/bin/bash
# Update and install necessary packages
sudo yum update -y
sudo yum install -y python3 python3-pip git

# Install dependencies
sudo pip3 install grpcio grpcio-tools

# Create a directory for the client
mkdir /home/ec2-user/client
cd /home/ec2-user/client

# Download the client.py script from GitHub
wget https://raw.githubusercontent.com/Un1xG0d/ZKP-Protocol-PoC/master/client.py

# Download gRPC generated files
wget https://raw.githubusercontent.com/Un1xG0d/ZKP-Protocol-PoC/master/zkp_auth_pb2.py
wget https://raw.githubusercontent.com/Un1xG0d/ZKP-Protocol-PoC/master/zkp_auth_pb2_grpc.py

# Set the server IP address as an environment variable
echo "export HOST=${server_ip}" >> /home/ec2-user/.bashrc
source /home/ec2-user/.bashrc

# Run the client
python3 client.py > output.txt
