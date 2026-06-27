# WellMind AI - Final Project Report

## Project Title

WellMind AI: Multi-Agent Student Wellness Intelligence System with RAG

## Institution

Sri Sathya Sai Institute of Actuaries

## Team Members

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

## Problem Statement

Students often face combined pressure from physical health issues, mental stress, and academic workload. These factors are usually analyzed separately, which makes it difficult to generate balanced and personalized wellness recommendations.

## Objective

The objective of WellMind AI is to create a multi-agent wellness system that collects student check-in data, analyzes it through specialized AI agents, retrieves wellness knowledge using RAG, and generates practical recommendations along with a PDF report and dashboard view.

## System Overview

The system follows a sequential multi-agent pipeline:

1. Student enters daily check-in details.
2. Physical Wellness Agent analyzes sleep, energy, and health indicators.
3. Mental Stress Agent analyzes emotional and stress signals.
4. Academic Load Agent analyzes study pressure and workload.
5. RAG Knowledge Agent retrieves relevant verified wellness knowledge.
6. Recommendation Agent creates personalized guidance.
7. The backend saves reports and the frontend displays results.

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Model | Gemini API |
| Agent Framework | LangChain |
| RAG Database | ChromaDB |
| Database | MongoDB Atlas |
| PDF Generation | ReportLab |
| Language | Python |

## Key Features

- 5-agent sequential AI pipeline
- RAG-grounded wellness recommendations
- Student daily check-in analysis
- Physical, mental, and academic score interpretation
- Personalized weekly timetable generation
- PDF wellness report generation
- MongoDB history storage
- Streamlit dashboard interface

## Source Code Structure

| Folder/File | Purpose |
|---|---|
| backend/ | FastAPI backend, database logic, pipeline, PDF generation |
| frontend/ | Streamlit user interface |
| agents/ | AI agents, knowledge base builder, RAG utilities |
| requirements.txt | Python dependencies |
| README.md | Setup and usage instructions |

## Setup Summary

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Add required environment variables in a local `.env` file.
5. Build the knowledge base if needed.
6. Start the FastAPI backend.
7. Start the Streamlit frontend.

## Limitations

- The system depends on valid API keys and database credentials.
- Recommendations are educational and supportive, not a replacement for professional medical or mental health advice.
- Deployment requires secure environment variable configuration.

## Future Scope

- Add authentication for students and mentors.
- Improve analytics using longer wellness history.
- Deploy the application publicly.
- Add role-based dashboards for counselors or teachers.
- Expand the wellness knowledge base.

## Conclusion

WellMind AI demonstrates how a multi-agent AI system can combine student health, stress, academic workload, and verified wellness knowledge to produce personalized recommendations. The project integrates AI agents, RAG, backend APIs, database storage, PDF reports, and a user-friendly dashboard into one complete solution.
