# BC Registered Nurse Assessment

An AI-powered assessment tool for evaluating nursing competency in British Columbia. 
Built with Streamlit and Strands SDK, deployed on AWS using CDK.

## Features

* **Select LLM** - Choose between Nova or Claude models
* **Interactive Scenarios** - Realistic nursing scenarios with visual context
* **Real-time Evaluation** - AI agent guides candidates through assessments
* **Progress Tracking** - Visual checklist of completed necessary actions
* **Comprehensive Reports** - Detailed final assessment with ratings and feedback

## Architecture

The application is deployed on AWS with the following components:

* **Streamlit App** - Running on Amazon Fargate with ECS
* **Load Balancer** - Application Load Balancer for traffic distribution
* **CDN** - Amazon CloudFront for global content delivery
* **Authentication** - Amazon Cognito user pool (optional)
* **AI Models** - Amazon Bedrock with Claude 3.5 Haiku and Nova Lite

## How It Works

1. **Scenario Presentation** - Agent presents a nursing scenario with context image
2. **User Actions** - Candidate describes their actions via text input
3. **AI Evaluation** - Agent evaluates responses and tracks correct actions
4. **Guidance** - Agent provides subtle guidance without revealing answers
5. **Final Report** - Evaluator agent generates comprehensive assessment when all necessary actions are completed

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

## Sample Scenario

**Post-Operative Patient Care**
- 65-year-old patient, 2 hours post-surgery
- Necessary actions: Check vital signs, assess pain level, check surgical site, review medication orders, assess consciousness
- Red flags: Administering medication without checking orders, skipping vital signs, leaving patient unattended

## Customization

To adapt this for your own assessment scenarios:

1. **Add scenarios** - Edit `docker_app/app.py` to add new SCENARIO definitions
2. **Modify evaluation** - Update `docker_app/agents/nurse_agent_config.py` for different guidance styles
3. **Add scenario images** - Place images in `docker_app/img/` directory
4. **Configure auth** - Enable Cognito authentication in `config_file.py`

## Security Notes

* Authentication is disabled by default for demo purposes
* Enable HTTPS for production deployments
* Configure proper IAM roles and policies
* Review and update dependencies regularly
* Consider enabling AWS WAF and other security services

## License

This project is provided as a demo and starting point. Review all dependencies and security configurations before production use.
