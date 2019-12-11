data "aws_vpc" "default" {
  id = var.vpc_id
}

data "aws_subnet_ids" "all" {
  vpc_id = data.aws_vpc.default.id
}

data "aws_subnet" "all" {
  count = length(data.aws_subnet_ids.all.ids)
  id    = tolist(data.aws_subnet_ids.all.ids)[count.index]
}

data "aws_security_group" "default" {
  vpc_id = data.aws_vpc.default.id
  name   = var.security_group
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["137112412989"] # Amazon

  filter {
    name = "name"

    values = [
      "amzn-ami-hvm-*-x86_64-gp2",
    ]
  }

  filter {
    name = "owner-alias"

    values = [
      "amazon",
    ]
  }
}

module "asg" {
  source  = "terraform-aws-modules/autoscaling/aws"
  version = "~> 3.0"

  name = "${var.name}-${var.environment}"

  # Launch configuration
  lc_name = "${var.name}-${var.environment}-lc"

  image_id        = data.aws_ami.amazon_linux.id
  instance_type   = "t3.medium"
  key_name        = var.key_name
  security_groups = [data.aws_security_group.default.id]

  ebs_block_device = [
    {
      device_name           = "/dev/xvdz"
      volume_type           = "gp2"
      volume_size           = "50"
      delete_on_termination = true
    },
  ]

  root_block_device = [
    {
      volume_size = "50"
      volume_type = "gp2"
    },
  ]

  # Auto scaling group
  asg_name                  = "${var.name}-${var.environment}-asg"
  vpc_zone_identifier       = [element(data.aws_subnet.all.*.id, 0)]
  health_check_type         = "EC2"
  min_size                  = 0
  max_size                  = var.quantity
  desired_capacity          = var.quantity
  wait_for_capacity_timeout = 0

  tags = [
    {
      key                 = "Environment"
      value               = var.environment
      propagate_at_launch = true
    },
  ]
}
