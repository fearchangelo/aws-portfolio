# Case Study: Hybrid Network Architecture with AWS Direct Connect

![Hybrid Network Diagram](docs/Hybrid_Network_Diagram.drawio.svg)

This diagram illustrates a hybrid network architecture that connects an on-premises corporate data center to AWS using two distinct AWS Direct Connect connections for secure, highly available, high-bandwidth, low-latency connectivity.

## Business Requirements
- Allow safe connectivity between on-premises data center and AWS environment
- Single Region
- Dozens of VPCs across multiple accounts
- A single VPC requires a high-throughput, dedicated VPC link
- Phyisical fiber path redundancy

## Solution Overview
- Two AWS Direct Connect connections are established through distinct service providers. An on-premises BGP router is connected to each provider by 10-Gbps physical fiber paths, cross-connected to Direct Connect locations (see https://aws.amazon.com/directconnect/locations/).
- VPCs are connected to a Transit Gateway. Whenever a new VPC is created, connectivity is established by attaching it to the TGW.
- The Transit Direct Connect Gateway allows traffic to flow from on-premises to the TGW.
- The high-throughput VPC is connected directly through a Private Direct Connect Gateway, bypassing the TGW for performance-sensitive workloads.
- The architecture demonstrates a redundant, highly available connection between on-premises infrastructure and AWS cloud resources using multiple Direct Connect connections and gateways.

## Benefits of This Architecture

### Performance
- **Dedicated Bandwidth**: Direct Connect provides consistent, predictable network performance
- **Low Latency**: Private connection reduces latency compared to internet-based connections
- **High Throughput**: Supports bandwidth requirements up to 100G
- **Dedicated VPC throughput**: Virtual Private Gateway provides a direct VPC connection from Direct Connect

### Reliability
- **Redundant Connections**: Multiple Direct Connect links eliminate single points of failure

### Security
- **Private Connectivity**: Traffic doesn't traverse the public internet
- **Network Isolation**: VIFs provide logical separation of different types of traffic
- **Consistent Security Policies**: Maintain corporate security standards across hybrid environment

### Scalability
- **Transit Gateway Integration**: Easily connect additional VPCs without complex routing
- **Multiple VPC Support**: Single connection can serve multiple AWS environments

## Use Cases

This architecture is ideal for:
- **Enterprise Hybrid Cloud**: Organizations with significant on-premises infrastructure
- **Data Migration**: Large-scale data transfers to AWS
- **Disaster Recovery**: Backup and recovery solutions spanning on-premises and cloud
- **Multi-VPC Environments**: Organizations with complex AWS architectures
- **Compliance Requirements**: Industries requiring private connectivity for regulatory compliance

## Implementation Considerations

### Network Planning
- Ensure adequate bandwidth provisioning for peak traffic
- Plan IP address spaces to avoid conflicts between on-premises and AWS networks
- Design routing policies for optimal traffic flow
- Direct Connect is *pricy*. Depending on the organization's requirements, having a single Direct Connect circuit and a Site-to-Site VPN (over the internet) as failover is enough.

### Redundancy Strategy
- Implement connections in different Direct Connect locations for maximum availability

### Security
- Implement appropriate access controls and network segmentation
- Monitor traffic flows and maintain security policies
- Ensure encryption for sensitive data in transit

This hybrid network architecture provides a robust foundation for enterprise cloud adoption, offering the performance, reliability, and security required for mission-critical applications spanning on-premises and AWS environments.

## Terraform Implementation

This project includes Terraform code to deploy the hybrid network architecture.

### Prerequisites
- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Existing AWS Direct Connect connections

### Deployment

1. Navigate to the terraform directory:
   ```bash
   cd tf/
   ```

2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Review and customize variables in `variables.tf` or create a `terraform.tfvars` file:
   ```hcl
   dx_connection_ids = ["dxcon-xxxxxxxxx", "dxcon-yyyyyyyyy"]
   customer_asn = 65000
   ```

4. Plan the deployment:
   ```bash
   terraform plan
   ```

5. Apply the configuration:
   ```bash
   terraform apply
   ```

### Key Variables
- `dx_connection_ids`: List of existing Direct Connect connection IDs
- `customer_asn`: Your on-premises BGP ASN
- `vpcs`: VPC configurations for Transit Gateway attachments
- `cost_center`: Cost center tag (default: "Networking")
- `application`: Application tag (default: "NetworkFoundation")

### Resources Created
- Transit Gateway with VPC attachments
- Multiple VPCs with subnets across AZs
- Direct Connect Gateways (Transit and Private)
- Virtual Interfaces (Transit and Private VIFs)
- VPN Gateway for private connectivity path
