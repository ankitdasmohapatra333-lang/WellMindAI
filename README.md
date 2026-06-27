# WellMind AI

**Multi-Agent Student Wellness Intelligence System with RAG**

Built during SSSIA Internship 1 | Team of 8 | June 2026

---

## What It Does

WellMind AI analyzes a student's daily physical health, mental stress, and academic workload using 5 specialized AI agents in a sequential pipeline, grounded in a verified wellness knowledge base via RAG.

---

## Architecture

Student Input (Daily Check-In)  
-> Agent 1 - Physical Wellness Agent  
-> Agent 2 - Mental Stress Agent  
-> Agent 3 - Academic Load Agent  
-> Agent 4 - RAG Knowledge Agent (ChromaDB)  
-> Agent 5 - Recommendation Agent  
-> PDF Report + Streamlit Dashboard + MongoDB History

## Tech Stack

| Layer | Technology |
|---|---|
| AI Agents | LangChain + Gemini API (gemini-2.5-flash-lite) |
| RAG | ChromaDB |
| Backend | FastAPI |
| Database | MongoDB Atlas (pymongo) |
| Frontend | Streamlit |
| PDF Reports | ReportLab |
| Version Control | GitHub |

## Team

| Member | Role |
|---|---|
| Haifa | Agent 3 - Academic Management |
| Subham | Agent 5 + Integration |
| Ritika | Agent 1 - Physical Wellness |
| Bhavitha | Agent 2 - Mental Stress |
| Ankit | FastAPI Backend + MongoDB |
| Yaswanth | Agent 4 - RAG + ChromaDB |
| Sandhya | Frontend - Streamlit |
| Komal | Content + PDF + QA |

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/WellMindAI.git
cd WellMindAI

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install packages
pip install -r requirements.txt

# 4. Add your .env file
GEMINI_API_KEY=your_key_here
MONGO_URI=your_mongo_uri_here

# 5. Build the knowledge base (first time only)
cd agents
python build_knowledge_base.py

# 6. Start FastAPI backend
cd ../backend
uvicorn api:app --reload

# 7. Start Streamlit frontend in a new terminal
cd frontend
streamlit run app.py
```

## API Routes

| Method | Route | Description |
|---|---|---|
| POST | /analyze | Runs full 5-agent pipeline |
| POST | /save | Saves report to MongoDB |
| GET | /history/{name} | Fetches past reports |

## Features

- 5-agent sequential pipeline
- RAG-grounded wellness knowledge base
- Real-time score analysis with contextual hints
- PDF wellness report generation
- 7-day wellness trend dashboard
- AI-generated personalized weekly timetable
- Dark / Light theme toggle
- MongoDB history storage

## Deadline

June 27, 2026
