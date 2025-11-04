output "tgw_id" {
  value = aws_ec2_transit_gateway.this.id
}

output "dx_gateways" {
  value = {
    transit = aws_dx_gateway.transit.id
    private = aws_dx_gateway.private.id
  }
}

output "transit_vifs" {
  value = { for k, v in aws_dx_transit_virtual_interface.tr_vifs : k => v.id }
}

output "private_vifs" {
  value = { for k, v in aws_dx_private_virtual_interface.pr_vifs : k => v.id }
}

output "dx_associations" {
  value = {
    tgw_assoc = aws_dx_gateway_association.tgw_assoc.id
    vgw_assoc = aws_dx_gateway_association.vgw_assoc.id
  }
}
