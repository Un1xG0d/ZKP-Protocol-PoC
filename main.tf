provider "aws" {
  region = var.region
}

variable "region" {
  description = "The AWS region to deploy in"
  default     = "us-east-1"
}

variable "allowed_ssh_ip" {
  description = "The IP address allowed to SSH into the instances"
  default     = "73.61.200.156/32" # Alan's apartment IP address
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "main" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_security_group" "main" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_ip]
  }

  ingress {
    from_port   = 50051
    to_port     = 50051
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "server" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.main.id
  security_groups = [aws_security_group.main.name]

  user_data = file("setup_server.sh")
  tags = {
    Name = "ServerInstance"
  }
}

resource "aws_instance" "client" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.main.id
  security_groups = [aws_security_group.main.name]

  user_data = file("setup_client.sh")
  tags = {
    Name = "ClientInstance"
  }
}

output "server_ip" {
  description = "Public IP of the server instance"
  value       = aws_instance.server.public_ip
}

output "client_ip" {
  description = "Public IP of the client instance"
  value       = aws_instance.client.public_ip
}
