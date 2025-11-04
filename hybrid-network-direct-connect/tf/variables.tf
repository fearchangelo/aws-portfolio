variable "region" {
  type        = string
  description = "AWS region for TGW/VPCs"
  default     = "sa-east-1"
}

variable "customer_asn" {
  description = "On-premises BGP ASN"
  type        = number
  default     = 65010
}

variable "dx_private_amazon_side_asn" {
  type        = number
  description = "Amazon side ASN for private DX Gateway"
  default     = 64600
}

variable "dx_transit_amazon_side_asn" {
  type        = number
  description = "Amazon side ASN for transit DX Gateway"
  default     = 64601
}

variable "dx_connection_ids" {
  description = "List of Direct Connect connection IDs"
  type        = list(string)
  default     = ["dxcon-g9x2k4rp", "dxcon-t7mzc1qa"]
}

# One transit VLAN per DX connection
variable "transit_vlans" {
  description = "VLANs for Transit VIFs"
  type        = list(number)
  default     = [1000, 1001]
}

# One private VLAN per DX connection
variable "private_vlans" {
  description = "VLANs for Private VIFs"
  type        = list(number)
  default     = [1002, 1003]
}

# BGP Customer IPs for Transit VIFs
variable "allowed_prefixes_to_aws" {
  description = "On-prem prefixes advertised toward AWS via DXGW association"
  type        = list(string)
  default     = ["10.0.0.0/8", "172.16.0.0/12"]
}

# VPC definitions for TGW attachments
variable "vpcs" {
  description = "List of VPCs to attach to TGW"
  type = list(object({
    name     = string
    cidr     = string
    az1_cidr = string
    az2_cidr = string
  }))
  default = [
    { name = "management", cidr = "10.101.0.0/16", az1_cidr = "10.101.1.0/24", az2_cidr = "10.101.2.0/24" },
    { name = "shared", cidr = "10.102.0.0/16", az1_cidr = "10.102.1.0/24", az2_cidr = "10.102.2.0/24" },
    { name = "apps", cidr = "10.103.0.0/16", az1_cidr = "10.103.1.0/24", az2_cidr = "10.103.2.0/24" }
  ]
}

# The VPC that will host the VGW (for the Private VIF path)
variable "vgw_vpc_cidr" {
  type        = string
  description = "CIDR of the VPC that will get a Virtual Private Gateway (VGW) for Private VIF"
  default     = "10.200.0.0/16"
}

variable "vgw_vpc_az1_cidr" {
  type    = string
  default = "10.200.1.0/24"
}

variable "vgw_vpc_az2_cidr" {
  type    = string
  default = "10.200.2.0/24"
}

# Jumbo frame configuration for DX
variable "dx_mtu" {
  type    = number
  default = 8500
}

# Tag value for CostCenter key
variable "cost_center" {
  type        = string
  description = "Cost center tag value"
  default     = "Networking"
}

# Tag value for Application key
variable "application" {
  type        = string
  description = "Application tag value"
  default     = "NetworkFoundation"
}

