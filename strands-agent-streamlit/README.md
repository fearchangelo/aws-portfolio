# Agentic AI Travel Picker

🚀 **[View Live Demo](https://d2i9r4rwutpa0d.cloudfront.net)**

A simulation of friends debating on a travel destination powered by Agentic AI. 
Built with Streamlit and Strands SDK, deployed on AWS using CDK.

## Features

* **Select LLM** - Choose between Nova or Claude models
* **Configure participants** - Add or select from predefined participant groups
* **Pick between quick travel ideas** - Use preset travel scenarios or create custom prompts

## Architecture

The application is deployed on AWS with the following components:

* **Streamlit App** - Running on Amazon Fargate with ECS
* **Load Balancer** - Application Load Balancer for traffic distribution
* **CDN** - Amazon CloudFront for global content delivery
* **Authentication** - Amazon Cognito user pool (optional)
* **AI Models** - Amazon Bedrock with Claude 3.5 Haiku and Nova Lite

## Quick Start

### Prerequisites

* Python >= 3.8
* AWS CLI configured
* AWS CDK installed
* Claude 3.5 Haiku and Nova Lite model access in Amazon Bedrock

### Local Development

1. **Setup virtual environment**
```bash
cd docker_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Run locally**
```bash
streamlit run app.py --server.port 8080
```

3. **Open browser**
Navigate to `http://localhost:8080`

### AWS Deployment

1. **Configure settings**
Edit `docker_app/config_file.py` with your stack name and preferences

2. **Install CDK dependencies**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Deploy to AWS**
```bash
cdk bootstrap
cdk deploy
```

4. **Access your app**
Use the CloudFront URL from the deployment output

## Usage Examples

Try these sample queries with the travel agent:

* "I want to plan a romantic weekend getaway in Europe"
* "Find me adventure activities in Costa Rica"
* "Suggest a family-friendly destination for summer vacation"
* "Plan a 5-day itinerary for Tokyo with cultural experiences"
* "What are the best food experiences in Bangkok?"

## Customization

To adapt this for your own travel use case:

1. **Modify the agent** - Edit `docker_app/app.py` to customize the AI agent's behavior
2. **Update UI** - Customize the Streamlit interface components
3. **Add tools** - Integrate additional APIs for flights, hotels, or activities
4. **Configure auth** - Enable Cognito authentication in `config_file.py`

## Security Notes

* Authentication is disabled by default for demo purposes
* Enable HTTPS for production deployments
* Configure proper IAM roles and policies
* Review and update dependencies regularly
* Consider enabling AWS WAF and other security services

## License

This project is provided as a demo and starting point. Review all dependencies and security configurations before production use.
