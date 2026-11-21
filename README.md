# EduPath — AI-Powered Personalized Career & Education Advisor

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Async%20Motor-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![PyTest](https://img.shields.io/badge/PyTest-Automated%20Tests-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)

An intelligent, full-stack educational advisory platform designed to help students discover personalized academic streams, higher-education degrees, college admission criteria, and career roadmaps using psychometric evaluation and AI-guided counseling.

---

## 🏛️ System Architecture

The platform is designed around a high-performance asynchronous microservice pattern:

```
┌────────────────────────────────────────────────────────┐
│                   React Client Layer                   │
│   (Student Dashboard, Aptitude Tests, Chatbot UI)      │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS / REST API
┌───────────────────────────▼────────────────────────────┐
│                  FastAPI Backend Server                │
│   • Asynchronous Request Pipelines                     │
│   • Pydantic v2 Data Validation & Schemas              │
│   • JWT Authentication & Bcrypt Password Security      │
│   • Psychometric & Aptitude Evaluation Engine          │
│   • LLM Conversational Guidance Agent                  │
└───────────────────────────┬────────────────────────────┘
                            │ Async Motor Driver
┌───────────────────────────▼────────────────────────────┐
│                    MongoDB Database                    │
│   (Users, Assessments, Colleges, Degrees, Chat History)│
└────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

- **Aptitude & Psychometric Assessment:** Multi-category scoring matrix evaluating analytical reasoning, verbal ability, technical aptitude, and creative problem solving to suggest optimal academic streams.
- **AI Career Counselor Chatbot:** Conversational guidance assistant capable of answering student queries on course prerequisites, entrance examinations, and scholarship programs.
- **College & Degree Directory:** Comprehensive search engine for higher-education institutions with filtering by state, stream, tuition budget, and accreditation.
- **Career Pathway Roadmaps:** Detailed career roadmaps mapping specific undergraduate degrees (B.Tech, B.Sc, BBA, BA) to entry-level job titles, industry skill stacks, and expected salary brackets.
- **Role-Based Admin Analytics:** Administrative dashboard tracking student registration metrics, test completion rates, and trending academic streams.

---

## 📂 Project Structure

```
AI-One-Stop-Personalized-Career-Education-Advisor/
├── .github/
│   └── workflows/
│       └── python-ci.yml              # GitHub Actions CI for linting & PyTest
├── backend/
│   ├── server.py                      # FastAPI application with routes & controllers
│   └── requirements.txt               # Python package dependencies
├── frontend/                          # Client Layer (React, CRACO, Tailwind)
├── tests/
│   ├── __init__.py
│   └── test_auth_and_models.py        # PyTest suite for auth, JWT, and scoring
├── Dockerfile                         # Production container image
├── docker-compose.yml                 # Multi-service stack (FastAPI + MongoDB)
└── README.md                          # Documentation
```

---

## 🚀 Quick Start & Local Execution

### Option A: Running with Docker Compose (Recommended)

Start both MongoDB and the FastAPI backend:

```bash
docker-compose up -d --build
```

Access the interactive Swagger API documentation at:  
👉 **`http://localhost:8000/docs`**

---

### Option B: Running Locally

#### 1. Setup Backend
```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run automated tests
pytest ../tests/ -v

# Start the development server
uvicorn server:app --reload --port 8000
```

#### 2. Setup Frontend
```bash
cd ../frontend
npm install
npm start
```

---

## 🧪 Automated Testing

The automated test suite verifies:
- Bcrypt password hashing and salt verification
- JWT token encoding, decoding, and expiration rejection
- Multi-category psychometric weight calculation algorithms

Run tests locally:
```bash
pytest tests/ -v
```

---

## 📄 License
This project is licensed under the MIT License.
