resource "aws_vpc" "terraform_vpc" {
    cidr_block = var.vpc_cidr
}
resource "aws_subnet" "terraform_subnet" {
    vpc_id = aws_vpc.terraform_vpc.id
    cidr_block = "10.0.1.0/24"
}
resource "aws_instance" "terraform_instance" {
    ami = data.aws_ami.ubuntu.id
    instance_type = var.instance_type
    subnet_id = aws_subnet.terraform_subnet.id
}
resource "aws_internet_gateway" "tf_igw" {
    vpc_id = aws_vpc.terraform_vpc.id
}
resource "aws_route_table" "tf_rt" {
    vpc_id = aws_vpc.terraform_vpc.id
}
resource "aws_route" "tf_route" {
    route_table_id = aws_route_table.tf_rt.id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.tf_igw.id
}
resource "aws_route_table_association" "tf-rta" {
    subnet_id = aws_subnet.terraform_subnet.id
    route_table_id = aws_route_table.tf_rt.id
}