############################
# Core network: TGW + VPCs #
############################

resource "aws_ec2_transit_gateway" "this" {
  description                     = "Org TGW"
  amazon_side_asn                 = var.dx_transit_amazon_side_asn
  auto_accept_shared_attachments  = "enable"
  default_route_table_association = "enable"
  default_route_table_propagation = "enable"
  dns_support                     = "enable"
  vpn_ecmp_support                = "enable"
  tags = {
    Name        = "org-tgw"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

# VPCs attached to TGW
resource "aws_vpc" "tgw_vpcs" {
  for_each             = { for v in var.vpcs : v.name => v }
  cidr_block           = each.value.cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name        = "vpc-${each.key}"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

data "aws_availability_zones" "available" {}

resource "aws_subnet" "tgw_vpc_az1" {
  for_each          = aws_vpc.tgw_vpcs
  vpc_id            = each.value.id
  cidr_block        = var.vpcs[index(keys(aws_vpc.tgw_vpcs), each.key)].az1_cidr
  availability_zone = data.aws_availability_zones.available.names[0]
  tags = {
    Name        = "sn-${each.key}-az1"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

resource "aws_subnet" "tgw_vpc_az2" {
  for_each          = aws_vpc.tgw_vpcs
  vpc_id            = each.value.id
  cidr_block        = var.vpcs[index(keys(aws_vpc.tgw_vpcs), each.key)].az2_cidr
  availability_zone = data.aws_availability_zones.available.names[1]
  tags = {
    Name        = "sn-${each.key}-az2"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

resource "aws_ec2_transit_gateway_vpc_attachment" "tgw_attachments" {
  for_each = aws_vpc.tgw_vpcs

  transit_gateway_id = aws_ec2_transit_gateway.this.id
  vpc_id             = each.value.id
  subnet_ids         = [aws_subnet.tgw_vpc_az1[each.key].id, aws_subnet.tgw_vpc_az2[each.key].id]

  dns_support  = "enable"
  ipv6_support = "disable"

  tags = {
    Name        = "tgw-att-${each.key}"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

######################################
# VPC with VGW for Private DX path   #
######################################

resource "aws_vpc" "vgw_vpc" {
  cidr_block           = var.vgw_vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name        = "vpc-vgw"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

resource "aws_subnet" "vgw_vpc_az1" {
  vpc_id            = aws_vpc.vgw_vpc.id
  cidr_block        = var.vgw_vpc_az1_cidr
  availability_zone = data.aws_availability_zones.available.names[0]
  tags = {
    Name        = "sn-vgw-az1"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

resource "aws_subnet" "vgw_vpc_az2" {
  vpc_id            = aws_vpc.vgw_vpc.id
  cidr_block        = var.vgw_vpc_az2_cidr
  availability_zone = data.aws_availability_zones.available.names[1]
  tags = {
    Name        = "sn-vgw-az2"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

resource "aws_vpn_gateway" "this" {
  vpc_id          = aws_vpc.vgw_vpc.id
  amazon_side_asn = 64520
  tags = {
    Name        = "vgw-private-path"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

#################################
# Direct Connect Gateways (2x)  #
#################################

# DXGW for Transit VIFs
resource "aws_dx_gateway" "transit" {
  name            = "dxgw-transit"
  amazon_side_asn = var.dx_transit_amazon_side_asn
}

# DXGW for Private VIFs
resource "aws_dx_gateway" "private" {
  name            = "dxgw-private"
  amazon_side_asn = var.dx_private_amazon_side_asn
}

# Associate TGW <-> DXGW (Transit)
resource "aws_dx_gateway_association" "tgw_assoc" {
  dx_gateway_id         = aws_dx_gateway.transit.id
  associated_gateway_id = aws_ec2_transit_gateway.this.id
  allowed_prefixes      = var.allowed_prefixes_to_aws
}

# Associate VGW <-> DXGW (Private)
resource "aws_dx_gateway_association" "vgw_assoc" {
  dx_gateway_id         = aws_dx_gateway.private.id
  associated_gateway_id = aws_vpn_gateway.this.id
  allowed_prefixes      = var.allowed_prefixes_to_aws
}

########################################
# Virtual Interfaces on BOTH circuits  #
########################################

locals {
  conn_map = {
    for idx, id in var.dx_connection_ids :
    idx => {
      id           = id
      transit_vlan = var.transit_vlans[idx]
      private_vlan = var.private_vlans[idx]
      tr_cust_ip   = null # let AWS auto-assign
      tr_aws_ip    = null # let AWS auto-assign
      pr_cust_ip   = null # let AWS auto-assign
      pr_aws_ip    = null # let AWS auto-assign
    }
  }
}

# One Transit VIF per connection → DXGW (transit) → TGW
resource "aws_dx_transit_virtual_interface" "tr_vifs" {
  for_each = local.conn_map

  connection_id  = each.value.id
  dx_gateway_id  = aws_dx_gateway.transit.id
  name           = "tr-vif-${each.key + 1}"
  vlan           = each.value.transit_vlan
  address_family = "ipv4"
  mtu            = var.dx_mtu
  bgp_asn        = var.customer_asn

  customer_address = each.value.tr_cust_ip
  amazon_address   = each.value.tr_aws_ip

  tags = {
    Path        = "transit"
    CostCenter  = var.cost_center
    Application = var.application
  }
}

# One Private VIF per connection → DXGW (private) → VGW
resource "aws_dx_private_virtual_interface" "pr_vifs" {
  for_each = local.conn_map

  connection_id  = each.value.id
  dx_gateway_id  = aws_dx_gateway.private.id
  name           = "pr-vif-${each.key + 1}"
  vlan           = each.value.private_vlan
  address_family = "ipv4"
  mtu            = var.dx_mtu
  bgp_asn        = var.customer_asn

  customer_address = each.value.pr_cust_ip
  amazon_address   = each.value.pr_aws_ip

  tags = {
    Path        = "private"
    CostCenter  = var.cost_center
    Application = var.application
  }
}
