# Private Subnet No Internet with Endpoint
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "ap-southeast-1a"

  tags = {
    Name = "Private"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "Private No Internet With endpoint"
  }
}

resource "aws_route_table_association" "private-route" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}