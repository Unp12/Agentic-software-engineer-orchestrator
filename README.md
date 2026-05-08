# 🚀 Autonomous Software Engineer Orchestrator

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![React](https://img.shields.io/badge/React-18.2-61DAFB?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi)
![GCP](https://img.shields.io/badge/Google_Cloud-Vertex_AI-4285F4?style=flat-square&logo=google-cloud)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)

> A full-stack, distributed AI microservice cluster that acts as an autonomous engineering team. It researches, writes, tests, and safely executes code using **A2A (Agent-to-Agent)** networking and **MCP (Model Context Protocol)**.

---

## 📖 Overview
The Autonomous Software Engineer Orchestrator is a transition from monolithic AI scripts to a cloud-native, distributed architecture. Users submit feature requests via a **React.js frontend**, which triggers a 3-node AI cluster. The system splits cognitive load between a Product Manager, Coder, and QA Agent, utilizing secure isolated sandboxes to iteratively debug its own code until validation is achieved.

## 🏗️ System Architecture

The architecture is decoupled into three distinct microservices to prevent context degradation and ensure host machine security.

<img width="1920" height="1080" alt="Screenshot (164)" src="https://github.com/user-attachments/assets/9cec57de-7a60-4967-b0ae-cbdba35f9538" />

```
[ React.js Frontend ] ──(REST API)──> [ Port 8000: LangGraph Orchestrator ]
                                                │         │
                   (A2A Network Protocol) ──────┘         └────── (MCP Protocol)
                                                ▼                 ▼
                                 [ Port 8002: Coder ]    [ Port 8001: MCP Sandbox ]
                                 (Stateless Logic)       (Secure Execution Node)
```
```
Layer,Technologies Used
Frontend,"React.js, HTML5, CSS3"
Backend,"Python 3.11, FastAPI, Uvicorn"
AI & Orchestration,"LangGraph, LangChain, Google Gemini 2.5 Flash"
Protocols,"A2A (Agent-to-Agent) Networking, MCP (Model Context Protocol)"
Cloud (GCP),"Vertex AI Agent Engine, Cloud Run, Artifact Registry, IAM"
Deployment,"Docker, Docker Compose"

```

## ✨ Key Features
* **A2A (Agent-to-Agent) Debugging Loops:** Overcame "hallucination loops" by engineering stateful HTTP payloads. The Orchestrator injects the last 5 nodes of error tracebacks across the network, giving the stateless Coder microservice the memory required to fix its own bugs.
* **Isolated MCP Sandbox:** AI-generated code is never executed on the main application thread. It is routed to an isolated Model Context Protocol server, preventing malicious or broken code from crashing the Orchestrator.
* **Full-Stack Visibility:** A React UI that allows users to submit prompts and monitor the Agent-to-Agent network jumps in real-time.
* **Cloud-Native Deployment:** Fully containerized using Docker and deployed on Google Cloud Platform using Cloud Run and Vertex AI Agent Engine.



## 🧠 Engineering Challenges & Solutions

**Challenge:** *The "Stateless Coder" Infinite Loop*
Moving the Coder to an independent microservice stripped it of session memory. When code failed, it received the original prompt without the bug report, causing `GraphRecursionError` crashes.
**Solution:** Upgraded the A2A network payload to inject LangGraph state history (including QA tracebacks) directly into the POST request, granting the Coder dynamic memory to break the loop.

**Challenge:** *API Quota Exhaustion*
High-frequency A2A communication during debugging triggered `429 RESOURCE_EXHAUSTED` errors from the Gemini API.
**Solution:** Implemented exponential backoff for external API calls and transitioned authentication to Google Cloud IAM roles via Vertex AI to utilize enterprise-grade routing.

🚀 Quick Start (Local Deployment)

1. Clone the Repository
Bash
git clone [https://github.com/Unp12/Agentic-software-engineer-orchestrator.git](https://github.com/Unp12/Agentic-software-engineer-orchestrator.git)
cd Agentic-software-engineer-orchestrator

2. Start the Backend Cluster (Requires Docker)
Bash
cd backend
docker-compose up --build
Orchestrator runs on http://localhost:8000

MCP Sandbox runs on http://localhost:8001

Coder Service runs on http://localhost:8002

3. Start the React Frontend
Bash
cd frontend
npm install
npm start

☁️ Cloud Deployment (GCP)
This project is optimized for Google Cloud Platform.

Container images are pushed to Artifact Registry.

The Coder and MCP Sandbox are deployed as stateless Cloud Run services via Docker containers.

The LangGraph Orchestrator is initialized via the Vertex AI Agent Engine (agent_engines.create), securely binding the A2A communication through Google's IAM.
