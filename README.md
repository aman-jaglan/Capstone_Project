# Credge AI – Your Financial Coach

## 📺 Demo

https://github.com/user-attachments/assets/2b3f13fc-bf67-42e6-8894-247373f131c3

Credge AI is an AI-driven personal finance coach that empowers users with intelligent, data-driven money management solutions. Our platform generates realistic synthetic financial data to protect user privacy while enabling rich model training ([research paper](https://github.com/aman-jaglan/Capstone_Project/raw/master/research_paper/Latex/Credge%20AI%20Research%20Paper.pdf)).

## 📋 Table of Contents
- [Data Synthesizer Workflow](#-data-synthesizer-workflow)
- [Key Features](#-key-features)
- [System Architecture](#️-system-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
  - [Environment Setup](#environment-setup)
  - [Running the Application](#running-the-application)
- [Docker Deployment](#-docker-deployment)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Research & Performance](#-research--performance)
- [Technology Stack](#️-technology-stack)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## 🔄 Data Synthesizer Workflow

Our Data Synthesizer module generates realistic financial transaction data through a sophisticated multi-step process:

### 1. Merchant Data Collection (`merchant_fetcher.py`)
- Fetches real business data from DC's official business license database
- Filters for active businesses in relevant categories (restaurants, retail, services, etc.)
- Caches data locally to avoid repeated API calls
- Cleans and standardizes merchant information (name, category, location, etc.)

### 2. Customer Profile Generation
- Creates synthetic customer profiles with realistic attributes:
  - Demographics (age, gender)
  - Financial information (income level)
  - Location data (ZIP code)
  - Household size
- Uses statistical distributions to ensure demographic diversity

### 3. Transaction Synthesis (`transaction_synthesizer_groq.py`)
- Generates realistic financial transactions using:
  - Customer profiles
  - Merchant data
  - Spending patterns
  - Geographic proximity

Key Features:
- **Category-based Spending**: Implements realistic spending distributions across different merchant categories
- **Geographic Intelligence**: Uses real DC ZIP codes and coordinates for location-based transactions
- **Temporal Patterns**: Generates transactions with realistic timing and frequency
- **Income-based Scaling**: Adjusts transaction amounts and frequencies based on customer income
- **Merchant Selection**: Picks merchants based on proximity and category relevance

### Running the Data Synthesizer

1. **Setup Environment**
```bash
cd src/Data_Synthesizer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure API Keys**
```python
# In config.py
API_KEY_Groq = "your_groq_api_key"
```

3. **Generate Data**
```bash
# Fetch merchant data
python code/merchant_fetcher.py

# Generate transactions
python code/transaction_synthesizer_groq.py
```

The synthesizer will create:
- Cached merchant data in `data/dc_businesses_cleaned.csv`
- Generated transactions in `synthetic_transactions.csv`
- Customer profiles and transaction logs in the specified output directory

### API Integration
- Endpoint: `/generate`
- Method: POST
- Input: Customer profile data (age, income, location, etc.)
- Output: Stream of synthetic transactions

Example API Response:
```json
{
  "transaction_id": "tx_123456",
  "timestamp": "2024-04-26T14:30:00",
  "merchant_name": "Local Grocery Store",
  "amount": 67.89,
  "category": "groceries",
  "location": {"zip": "20001", "lat": 38.9109, "lon": -77.0163}
}
```

## 🚀 Key Features

### 1. Synthetic Data Generator
- Uses advanced Bayesian modeling and GANs to simulate realistic transaction records
- Protects user privacy while maintaining data utility
- Research-backed methodology ([paper](https://arxiv.org/pdf/2410.15653))

### 2. Budget Classification & Optimization
- Deep learning-powered expense classification using LLMs (BERT, LLaMA3)
- Smart budget improvement suggestions
- Average savings of 3–5% on monthly expenses

### 3. LLM Investment Advisor
- Personalized investment advice using BERT/GPT based models
- Research-proven effectiveness ([study](https://markets.businessinsider.com/news/stocks/chatgpt-4-vs-humans-ai-financial-analysis-forecasting-new-study-2024-5))
- Real-time market analysis

### 4. Interactive Web Interface
- React-based modern UI
- Intuitive goal setting and tracking
- Comprehensive financial visualizations

## 🏗️ System Architecture

Credge AI consists of three core components working in harmony:

1. **Synthetic Data Engine**
   - Bayesian modeling
   - GANs for data generation
   - LLM integration

2. **Budget Classification & Optimization Agent**
   - Logistic Regression
   - BERT for text classification
   - LLaMA3 integration

3. **LLM Investment Advisor**
   - BERT/GPT models
   - FinBERT/BeBERTa for Technical Analysis
   - Ensemble of FinBERT, RoBERTa and VADER for Funadamental and News Based Analysis
   - Real-time market data integration

## 🚀 Getting Started

### Prerequisites
Before you begin, ensure you have the following installed:
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)
- Docker (optional, for containerized deployment)
- Git

### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/aman-jaglan/Capstone_Project.git
cd Capstone_Project
```

### Environment Setup

1. Create a `.env` file in the root directory:
```bash
cp .env.example .env
(add these below lines inside your env file)
REACT_APP_FIREBASE_API_KEY=your_api
REACT_APP_FIREBASE_AUTH_DOMAIN=REACT_APP_FIREBASE_PROJECT_ID.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=firebase_projectID
REACT_APP_FIREBASE_STORAGE_BUCKET=REACT_APP_FIREBASE_PROJECT_ID.firebasestorage.app
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=firebase_sender_ID
REACT_APP_FIREBASE_APP_ID=firebase_app_id
REACT_APP_FIREBASE_MEASUREMENT_ID=firebase_measurement
```

2. Configure your environment variables:
```env
REACT_APP_API_URL=http://localhost:5001
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=your_database_url
```

### Running the Application

1. **Start Backend Scripts**

```bash
NOTE: Run each file in a Dedicated Terminal

(For Data Synthesizer)
cd Capstone_Project/src/Data_Synthesizer/code
python transaction_synthesizer_groq.py

(For Budget Classification)
cd Capstone_Project/src/Agents/BudgetClassification_Agent
python TransactionExtractor.py

(For Investment Advisor)
cd Capstone_Project/src/Agents/Investment_agent/API
python finapi.py

```

2. **Start React App**
```bash
cd Capstone_Project/src/app
npm start 
```

## 🔧 Troubleshooting

Common issues and solutions:

1. **Port Already in Use**
```bash
# Kill process using port 5001
lsof -i :5001  # Find PID
kill -9 <PID>  # Kill process
```

2. **Node Modules Issues**
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules
npm install
```

3. **Python Virtual Environment Issues**
```bash
# Recreate virtual environment
deactivate  # If already in a venv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🐳 Docker Deployment

### Container Setup
```bash
# Build the Docker image
docker build -t credge-api .

# Run the container
docker run -d \
  -p 80:80 \
  -p 443:443 \
  -p 8000:8000 \
  --name credge-container \
  credge-api
```

### SSL Certificate Configuration
When accessing the API (https://52.71.240.201/generate), you may encounter a security warning due to self-signed SSL certificates in development.

To proceed:
1. Click "Advanced" in your browser
2. Select "Proceed to [IP] (unsafe)"
3. This is a one-time action per browser session

> **Production Note**: For production environments, we recommend using a proper domain with Let's Encrypt SSL certificates.

### API Infrastructure
The system uses Nginx as a reverse proxy with:
- SSL/TLS encryption
- CORS configuration
- Proxy pass to FastAPI backend (port 8000)

Key Endpoints:
- Frontend: https://credge.vercel.app
- API: https://52.71.240.201/generate

Nginx handles:
- HTTP to HTTPS redirection
- CORS headers for Vercel frontend
- SSL certificate management
- FastAPI proxy configuration

## 📡 API Documentation

### Key Endpoints

1. **Frontend Application**
   - URL: https://credge.vercel.app
   - Local: http://localhost:3000

2. **Backend API**
   - Production: https://52.71.240.201/generate
   - Local: http://localhost:5001

### API Routes

| Endpoint | Method | Description | Required Headers |
|----------|---------|-------------|-----------------|
| `/generate` | POST | Generate synthetic data | `Authorization` |
| `/analyze` | POST | Analyze transactions | `Authorization` |
| `/optimize` | POST | Get budget optimization | `Authorization` |

## 📊 Research & Performance

### Key Findings
- **Synthetic Data Quality**: GAN-generated records achieve high realism in spending patterns
- **Classification Accuracy**: 71% multi-class budget categorization (comparable to WeNet-RF benchmark of 90%)
- **Budget Optimization**: Demonstrated 3–5% monthly savings through smart reallocation
- **Investment Advisor**: GPT-based advice matches human-level financial forecasting accuracy

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| Backend | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) |
| Frontend | ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB) ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white) |
| AI/ML | ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white) |
| LLM | ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) ![Hugging Face](https://img.shields.io/badge/HuggingFace-FFD21F?style=for-the-badge&logo=huggingface&logoColor=black) |
| Infrastructure | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white) |

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

## 🙏 Acknowledgments

Special thanks to:
- Credge AI Academy mentors
- Open-source community (Hugging Face, TensorFlow, OpenAI, SDV)
- Data providers (DC Open Data, Census, Yelp Open Data)
