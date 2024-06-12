provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "main" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

resource "aws_security_group" "main" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["73.61.200.156/32"] # Alan's apartment IP address
  }

  ingress {
    from_port   = 50051
    to_port     = 50051
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 50051
    to_port     = 50051
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "server" {
  ami           = "ami-08a0d1e16fc3f61ea"  # Amazon Linux 2023 AMI
  instance_type = "t2.micro"
  key_name      = "zkp_test"
  subnet_id     = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.main.id]
  associate_public_ip_address = true

  user_data = file("setup_server.sh")
  tags = {
    Name = "ServerInstance"
  }
}

resource "aws_instance" "client" {
  ami           = "ami-08a0d1e16fc3f61ea"  # Amazon Linux 2023 AMI
  instance_type = "t2.micro"
  key_name      = "zkp_test"
  subnet_id     = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.main.id]
  associate_public_ip_address = true

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
