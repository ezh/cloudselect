resource "aws_instance" "bastion" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t3.medium"
  key_name                    = var.key_name
  vpc_security_group_ids      = [data.aws_security_group.default.id]
  associate_public_ip_address = true
  subnet_id                   = element(data.aws_subnet.all.*.id, 0)

  tags = {
    Name = "Bastion"
  }
}
