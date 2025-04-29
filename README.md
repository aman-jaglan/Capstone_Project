<img src="Credge.png" alt="Credge AI Banner" width="200" height="200"/>

# Credge AI – Your Financial Coach

Credge AI is an AI-driven personal finance coach designed to empower users with intelligent, data-driven money management. It generates realistic **synthetic financial data** to protect privacy while enabling rich model training ([paper](https://arxiv.org/pdf/2410.15653)). It automatically **classifies and optimizes budgets**, and offers an **LLM-based investment advisor** for personalized guidance.

---

## ✨ Features

- **Synthetic Data Generator**: Uses Bayesian modeling and GANs to simulate realistic transaction records ([paper](https://arxiv.org/pdf/2410.15653)).
- **Budget Classification & Optimization**: Classifies expenses using deep learning (BERT, LSTM) and suggests budget improvements (~3–5% savings).
- **LLM Investment Advisor**: Provides personalized advice leveraging LLaMA/GPT-based models ([study](https://markets.businessinsider.com/news/stocks/chatgpt-4-vs-humans-ai-financial-analysis-forecasting-new-study-2024-5)).
- **Interactive Web App**: React-based app for goal setting, budget visualization, and investment chat.

---

## 🏗️ Architecture

Credge AI has three major components:

1. **Synthetic Data Engine** (Bayesian + GANs + LLMs)
2. **Budget Classification & Optimization Agent** (Logistic Regression, LSTM, BERT, LLaMA)
3. **LLM Investment Advisor** (LLaMA, GPT, FinBERT)

These modules work together through an interactive front-end, ensuring smooth data and decision flows.

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/aman-jaglan/Credge.git
cd credge-ai

# Navigate to app directory
cd Credge/src/app

# Install dependencies
npm install

# Start the app
npm run
```

Visit: [http://localhost:3000/](http://localhost:3000/)

> Ensure your API keys are set in the `.env` file if using external LLM APIs!

---

## 🐳 Docker & API Setup

### Docker Container Setup
```bash
# Build and run the Docker container
docker build -t credge-api .
docker run -d -p 80:80 -p 443:443 -p 8000:8000 --name credge-container credge-api
```

### SSL Certificate Notice
When accessing the API (https://52.71.240.201/generate), you'll see a security warning because we use a self-signed SSL certificate. This is normal for development environments.

To proceed:
1. Click "Advanced" in your browser
2. Click "Proceed to [IP] (unsafe)" or "Accept the Risk and Continue"
3. This only needs to be done once per browser session

> **Note**: For production deployment, we recommend using a proper domain name with Let's Encrypt SSL certificates.

### API Configuration
The API uses Nginx as a reverse proxy with the following features:
- SSL/TLS encryption (self-signed certificates)
- CORS configuration for secure frontend-backend communication
- Proxy pass to FastAPI backend on port 8000

Key endpoints:
- Frontend: https://credge.vercel.app
- API: https://52.71.240.201/generate

The Nginx configuration handles:
- HTTP to HTTPS redirection
- CORS headers for Vercel frontend
- SSL certificate management
- Proxy configuration to FastAPI

---

## 🚀 Usage

- **Generate Synthetic Data**
- **Classify & Optimize Budgets**
- **Request Investment Advice**
- **View Financial Visualizations**

Access everything through the intuitive web interface!

---

## 📚 Technologies Used

| Language / Framework | Description |
| :------------------ | :--------- |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | For data generation, model training |
| ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white) | Backend/API development |
| ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB) | Frontend interactive app |
| ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white) | Model training (GANs, LSTM) |
| ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) | LLM Investment Advisor (GPT, LLaMA) |
| ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white) | Deep learning framework for model building |
| ![Hugging Face](https://img.shields.io/badge/HuggingFace-FFD21F?style=for-the-badge&logo=huggingface&logoColor=black) | Transformer models and NLP APIs |
| ![Vantage API](https://img.shields.io/badge/Vantage-0085CA?style=for-the-badge&logo=datadog&logoColor=white) | Real-time stock market data API |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) | High-performance backend services |
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) | Interactive AI demos and dashboards |
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) | Containerization and deployment |

---

## 📈 Research Highlights

- **Synthetic Data Realism**: GAN-generated records indistinguishable from real spending patterns.
- **Classification Accuracy**: ~71% multi-class budget categorization ([WeNet-RF benchmark ~90%](https://pmc.ncbi.nlm.nih.gov/articles/PMC12021194/)).
- **Budget Optimization**: Users could reallocate and save 3–5% of monthly income.
- **Investment Advisor Effectiveness**: GPT-based advice aligned with human-level financial forecasting ([source](https://arxiv.org/abs/2504.05862)).

---

## 🤝 Contributing

1. Fork the repo.
2. Create a new branch: `git checkout -b feature/my-feature`
3. Make changes and commit: `git commit -m 'Add my feature'`
4. Push to your branch: `git push origin feature/my-feature`
5. Open a Pull Request!

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for details.

---

## 📄 License

Licensed under the [MIT License](./LICENSE).

---

## 🙏 Acknowledgments

Special thanks to:
- Credge AI Academy mentors
- Open-source libraries (Hugging Face, TensorFlow, OpenAI, SDV)
- Financial datasets from DC Open Data, Census & Yelp Open Data.

---
