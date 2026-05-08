Markdown# 🚀 Autonomous Software Engineer Orchestrator

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

```text
[ React.js Frontend ] ──(REST API)──> [ Port 8000: LangGraph Orchestrator ]
                                                │         │
                   (A2A Network Protocol) ──────┘         └────── (MCP Protocol)
                                                ▼                 ▼
                                 [ Port 8002: Coder ]    [ Port 8001: MCP Sandbox ]
                                 (Stateless Logic)       (Secure Execution Node)
✨ Key FeaturesA2A (Agent-to-Agent) Debugging Loops: Overcame "hallucination loops" by engineering stateful HTTP payloads. The Orchestrator injects the last 5 nodes of error tracebacks across the network, giving the stateless Coder microservice the memory required to fix its own bugs.Isolated MCP Sandbox: AI-generated code is never executed on the main application thread. It is routed to an isolated Model Context Protocol server, preventing malicious or broken code from crashing the Orchestrator.Full-Stack Visibility: A React UI that allows users to submit prompts and monitor the Agent-to-Agent network jumps in real-time.Cloud-Native Deployment: Fully containerized using Docker and deployed on Google Cloud Platform using Cloud Run and Vertex AI Agent Engine.🛠️ Tech StackLayerTechnologies UsedFrontendReact.js, HTML5, CSS3BackendPython 3.11, FastAPI, UvicornAI & OrchestrationLangGraph, LangChain, Google Gemini 2.5 FlashProtocolsA2A (Agent-to-Agent) Networking, MCP (Model Context Protocol)Cloud (GCP)Vertex AI Agent Engine, Cloud Run, Artifact Registry, IAM🧠 Engineering Challenges & SolutionsChallenge: The "Stateless Coder" Infinite LoopMoving the Coder to an independent microservice stripped it of session memory. When code failed, it received the original prompt without the bug report, causing GraphRecursionError crashes.Solution: Upgraded the A2A network payload to inject LangGraph state history (including QA tracebacks) directly into the POST request, granting the Coder dynamic memory to break the loop.Challenge: API Quota ExhaustionHigh-frequency A2A communication during debugging triggered 429 RESOURCE_EXHAUSTED errors from the Gemini API.Solution: Implemented exponential backoff for external API calls and transitioned authentication to Google Cloud IAM roles via Vertex AI to utilize enterprise-grade routing.🚀 Quick Start (Local Deployment)1. Clone the RepositoryBashgit clone [https://github.com/YOUR_USERNAME/autonomous-software-engineer-orchestrator.git](https://github.com/YOUR_USERNAME/autonomous-software-engineer-orchestrator.git)
cd autonomous-software-engineer-orchestrator
2. Start the Backend Cluster (Requires Docker)Bashcd backend
docker-compose up --build
Orchestrator runs on http://localhost:8000MCP Sandbox runs on http://localhost:8001Coder Service runs on http://localhost:80023. Start the React FrontendBashcd frontend
npm install
npm start
☁️ Cloud Deployment (GCP)This project is optimized for Google Cloud Platform.Container images are pushed to Artifact Registry.The Coder and MCP Sandbox are deployed as stateless Cloud Run services.The LangGraph Orchestrator is initialized via the Vertex AI Agent Engine (agent_engines.create), securely binding the A2A communication through Google's IAM.📈 Impact / ATS MetricsArchitected a distributed multi-agent system using LangGraph and FastAPI, decoupling AI logic into a 3-node microservice cluster that reduced debugging iteration loops by providing stateful error feedback via A2A (Agent-to-Agent) networking.Engineered an isolated Model Context Protocol (MCP) sandbox for secure AI code execution, successfully containerizing the pipeline with Docker to safely execute and validate 100% of AI-generated scripts outside the main application thread.
Once you commit this to your main branch, GitHub will automatically render those badges and code blocks into a beautiful landing page. 

Are you planning to add a few screenshots or a GIF of the React UI working into the READ
