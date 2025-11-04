# Case Study: Hybrid Network Architecture with AWS Direct Connect

![Hybrid Network Diagram](docs/Hybrid_Network_Diagram.drawio.svg)

This diagram illustrates a hybrid network architecture that connects an on-premises corporate data center to AWS using two distinct AWS Direct Connect connections for secure, highly-available, high-bandwidth, low-latency connectivity.

## Business Requirements
- Allow safe connectivity between on-premises data center and AWS environment
- Single Region
- Dozens of VPCs across multiple accounts
- A single VPC requires a high-throughput, dedicated VPC link
- Phyisical fiber path redundancy

## Architecture Overview

The architecture demonstrates a redundant, highly available connection between on-premises infrastructure and AWS cloud resources using multiple Direct Connect connections and gateways.

### Key Components

#### On-Premises Infrastructure
- **Corporate Data Center**: The on-premises environment containing business-critical applications and data
- **Customer Gateway**: A router that serves as the connection point between the corporate network and AWS Direct Connect

#### AWS Direct Connect Infrastructure
- **AWS Direct Connect Connection #1**: Primary dedicated network connection
- **AWS Direct Connect Connection #2**: Secondary connection for redundancy
- **Transit VIF #1 & #2**: Transit Virtual Interfaces that enable connectivity to multiple VPCs through Transit Gateway
- **Private VIF #1 & #2**: Private Virtual Interfaces for direct VPC connectivity

#### AWS Gateway Infrastructure
- **DX Gateway (Transit)**: Direct Connect Gateway configured for Transit Gateway integration
- **DX Gateway (Private)**: Direct Connect Gateway for private VPC connectivity
- **Transit Gateway**: Central hub for connecting multiple VPCs and on-premises networks

#### AWS Cloud Resources
- **Region**: AWS region containing the cloud infrastructure
- **Multiple VPCs**: Virtual Private Clouds hosting various applications and services
- **Virtual Private Gateway**: Enables VPC connectivity to on-premises networks

## Network Flow and Connectivity

### Primary Data Path
1. Traffic originates from the corporate data center
2. Passes through the Customer Gateway
3. Travels over AWS Direct Connect connections
4. Routes through appropriate Virtual Interfaces (VIFs)
5. Reaches AWS resources via Direct Connect Gateways and Transit Gateway

### Redundancy and High Availability
- **Dual Direct Connect Connections**: Provides redundancy at the physical connection level
- **Multiple VIFs**: Separate Virtual Interfaces ensure traffic isolation and redundancy
- **Multiple Gateways**: Both Transit and Private Direct Connect Gateways offer different connectivity patterns

## Benefits of This Architecture

### Performance
- **Dedicated Bandwidth**: Direct Connect provides consistent, predictable network performance
- **Low Latency**: Private connection reduces latency compared to internet-based connections
- **High Throughput**: Supports bandwidth requirements from 50 Mbps to 100 Gbps

### Reliability
- **Redundant Connections**: Multiple Direct Connect links eliminate single points of failure
- **Multiple VIFs**: Traffic can be distributed across different virtual interfaces
- **Gateway Redundancy**: Both Transit and Private gateways provide failover capabilities

### Security
- **Private Connectivity**: Traffic doesn't traverse the public internet
- **Network Isolation**: VIFs provide logical separation of different types of traffic
- **Consistent Security Policies**: Maintain corporate security standards across hybrid environment

### Scalability
- **Transit Gateway Integration**: Easily connect additional VPCs without complex routing
- **Multiple VPC Support**: Single connection can serve multiple AWS environments
- **Flexible Bandwidth**: Adjust connection speeds based on requirements

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

### Redundancy Strategy
- Implement connections in different Direct Connect locations for maximum availability
- Configure appropriate failover mechanisms
- Test failover scenarios regularly

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
