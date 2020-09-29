# Creates a VPC with ipv4 and ipv6 enabled
resource "aws_vpc" "main" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"
  assign_generated_ipv6_cidr_block = true # unable to specify cidr block of ipv6 
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "main"
    Stage = "security-serverless"
  }
}