# lambda security group

resource "aws_security_group" "lambda_security_group" {
  name        = "lambda_security_group"
  description = "Security Group for the lambda subnet"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_security_group" "vpc_endpoint" {
  name        = "VPC Endpoint Security Group"
  description = "Allow incoming TLS connectivity for VPC endpoints"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

}
