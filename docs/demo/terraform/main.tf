provider "aws" {
  region = "eu-west-1"

  # Make it faster by skipping something
  skip_get_ec2_platforms      = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

resource "aws_key_pair" "deployer" {
  key_name   = "cloudselect-demo"
  public_key = file("./id_rsa.pub")
}

module "web-dev" {
  environment    = "dev"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "web"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "web-qa" {
  environment    = "qa"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "web"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "web-stg" {
  environment    = "stg"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "web"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "web-prod" {
  environment    = "stg"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "web"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "backend-dev" {
  environment    = "dev"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "backend"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "backend-qa" {
  environment    = "dev"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "backend"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "backend-stg" {
  environment    = "stg"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "backend"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "backend-prod" {
  environment    = "prod"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "backend"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "middleware-dev" {
  environment    = "dev"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "middleware"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "middleware-qa" {
  environment    = "qa"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "middleware"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "middleware-stg" {
  environment    = "stg"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "middleware"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}

module "middleware-prod" {
  environment    = "prod"
  instance_type  = var.instance_type
  key_name       = aws_key_pair.deployer.key_name
  name           = "middleware"
  quantity       = 4
  security_group = var.security_group
  source         = "./group"
  vpc_id         = var.vpc_id
}
