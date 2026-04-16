<div align="center">

<img src="https://img.shields.io/badge/Clarionyx-Regulatory%20AI-1a2b4a?style=for-the-badge&logoColor=white" />

# 🛡️ Regulatory Compliance Intelligence Copilot

### Grounded Multi-Framework RAG for GDPR · HIPAA · NIST

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1--mini-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-00BFFF?style=flat-square)](https://pinecone.io)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

> **A production-grade, evidence-grounded Q&A system that answers regulatory compliance questions with verified citations, confidence-based human review routing, and full audit logging — built for healthcare and data privacy organisations.**

[Features](#-key-features) · [Architecture](#-architecture) · [Pipeline](#-10-stage-rag-pipeline) · [Results](#-validation--kpi-results) · [Tech Stack](#-tech-stack) · [Setup](#-getting-started)

</div>

---

## 🎯 Problem Statement

Compliance teams in regulated industries spend enormous time manually answering the same GDPR, HIPAA, and NIST questions — inconsistently, slowly, and without a traceable audit trail. Generic chatbots make this worse by generating plausible-sounding but unsupported answers, creating serious legal exposure.

**This project solves that.** Instead of hallucinating, it retrieves — grounding every answer in authoritative regulatory source documents, normalising citations, and escalating uncertain cases to a human compliance officer before they reach end users.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Multi-Framework RAG** | Covers GDPR, HIPAA, and NIST from 3,600 embedded regulatory chunks |
| 📎 **Grounded Citations** | Every answer cites specific Articles, CFR sections, or NIST controls |
| 🤖 **Semantic Reranking** | Cohere reranks retrieved evidence before answer generation |
| 🧠 **Multi-Query Expansion** | Rewrites queries into 3 variants to maximise semantic recall |
| 📊 **Confidence Scoring** | Combines rerank strength, citation presence, and consistency signals |
| 🚦 **Human Review Routing** | Low-confidence answers are escalated to a compliance officer via Telegram |
| 🔒 **Policy Guardrails** | Three-class classifier blocks prompt injections, jailbreaks, and off-topic requests |
| 📋 **Airtable Audit Trail** | Every interaction — question, answer, citations, confidence, status — is logged |
| ⚡ **Fast Responses** | 11.8s average end-to-end latency, well within interactive use requirements |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER / UI LAYER                          │
│   Streamlit UI  →  FastAPI /query  →  Framework Router          │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    INTELLIGENCE LAYER (FastAPI)                  │
│  Validate → Detect Framework → Multi-Query Expansion            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    RETRIEVAL (Pinecone)                          │
│  6 Namespaces: gdpr_pdf · gdpr_structured · hipaa_pdf           │
│                hipaa_structured · nist_pdf · nist_csf_pdf        │
│  3,600 total embedded chunks                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    RERANKING (Cohere)                            │
│  Deduplicate → Semantic Rerank → Keep Top-5 Evidence Chunks     │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│               ANSWER GENERATION (OpenAI GPT-4.1-mini)           │
│  Grounded Prompt → Generate → Normalise Citations               │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────▼──────────────┐
              │    Confidence Score ≥ 0.85?  │
              └──────┬──────────────┬────────┘
                     │ YES          │ NO
              ┌──────▼──────┐ ┌────▼──────────────────┐
              │  Auto-serve │ │  Escalate → n8n →      │
              │  to user    │ │  Telegram → Officer    │
              └──────┬──────┘ │  Review → Airtable     │
                     │        └────────────────────────┘
              ┌──────▼────────────────────────────────────────────┐
              │              AIRTABLE AUDIT TRAIL                  │
              │  Question · Answer · Citations · Confidence ·      │
              │  Status · Namespaces · Record ID                   │
              └───────────────────────────────────────────────────┘
```

---

## ⚙️ 10-Stage RAG Pipeline

```
1. Request Intake & Validation      →   FastAPI schema validation
2. Framework Routing                →   GDPR / HIPAA / NIST / Multi-framework
3. Multi-Query Expansion            →   3 semantic query variants
4. Namespace Selection              →   PDF + structured namespaces per framework
5. Semantic Retrieval               →   Pinecone cosine similarity search
6. Deduplication & Reranking        →   Cohere semantic reranking
7. Grounded Answer Generation       →   OpenAI from retrieved chunks only
8. Citation Normalisation           →   GDPR Art. / HIPAA CFR / NIST CSF format
9. Confidence Scoring & Routing     →   Auto-approve or pending_review
10. Airtable Logging & Retrieval    →   Full audit trail, reviewed answer by record ID
```

---

## 📊 Validation & KPI Results

### Headline KPIs — Pure Regulatory Q&A (45 questions)

| Metric | Target | Actual | Status |
|---|---|---|---|
| ✅ Answer Accuracy | ≥ 90% | **93.3%** | **PASS** |
| ✅ Self-Service Rate | ≥ 80% | **86.7%** | **PASS** |
| ✅ Response Time | < 120s | **11.8s avg** | **PASS** |
| ✅ Validation Coverage | 100% | **100%** | **PASS** |
| ✅ RAGAS Faithfulness | > 90% | **90.5%** | **PASS** |
| ⚠️ Source Traceability | 100% | 80% | In Progress |
| ⚠️ RAGAS Correctness | > 90% | 77.3% | In Progress |

### RAGAS Automated Evaluation (15-question subset)

| Framework | Faithfulness | Answer Correctness |
|---|---|---|
| GDPR | 93.1% | 79.5% |
| HIPAA | 88.2% | 86.6% |
| NIST | 90.1% | 65.7% |
| **Average** | **90.5%** | **77.3%** |

> NIST correctness gap reflects chunk-limited scope vs. exhaustive reference answers — not factual errors. Zero major hallucinations detected across all Pure Regulatory Q&A tests.

### Guardrail Performance

| Test Category | Questions | Block Success |
|---|---|---|
| Prompt Injection / Jailbreak | 6 | **100%** |
| Ambiguous / Cross-Framework | 10 | Correct escalation routing |

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit | Query entry, answer display, review lookup |
| **Backend** | FastAPI | Orchestration, routing, confidence scoring |
| **Vector DB** | Pinecone | 3,600 regulatory chunk embeddings across 6 namespaces |
| **Reranking** | Cohere | Semantic evidence reranking |
| **LLM** | OpenAI GPT-4.1-mini | Grounded answer generation |
| **Governance** | Airtable | Full audit trail and reviewed-answer storage |
| **Automation** | n8n | Pending review alerts to Telegram |
| **Human Review** | Python Telegram Bot | Officer review, correction, Airtable write-back |

---

## 📁 Data Coverage

| Framework | Namespaces | Chunks |
|---|---|---|
| GDPR | `gdpr_pdf`, `gdpr_structured` | 915 (487 PDF + 428 structured) |
| HIPAA | `hipaa_pdf`, `hipaa_structured` | 396 (390 PDF + 6 structured) |
| NIST | `nist_pdf`, `nist_csf_pdf` | 2,289 (2,190 general + 99 CSF) |
| **Total** | 6 namespaces | **3,600 chunks** |

> All source documents downloaded from official government and standards bodies. Chunked at ~1,000 characters with 150-character overlap.

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.10+
Pinecone account + API key
OpenAI API key
Cohere API key
Airtable account + base
Telegram bot token (for human review)
n8n instance (for automation)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/regulatory-compliance-copilot.git
cd regulatory-compliance-copilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Fill in your credentials
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
COHERE_API_KEY=your_cohere_key
AIRTABLE_API_KEY=your_airtable_key
AIRTABLE_BASE_ID=your_base_id
TELEGRAM_BOT_TOKEN=your_telegram_token
```

### Run the Application

```bash
# Start the FastAPI backend
uvicorn app.main:app --reload --port 8000

# In a separate terminal, start the Streamlit frontend
streamlit run frontend/app.py
```

---

## 📂 Project Structure

```
regulatory-compliance-copilot/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── routers/
│   │   ├── query.py            # /query endpoint — main RAG pipeline
│   │   └── review.py           # /review endpoint — Airtable answer retrieval
│   ├── services/
│   │   ├── retrieval.py        # Pinecone namespace retrieval
│   │   ├── reranker.py         # Cohere reranking
│   │   ├── generator.py        # OpenAI grounded answer generation
│   │   ├── confidence.py       # Confidence scoring logic
│   │   └── guardrails.py       # Policy-based input guardrail layer
│   └── utils/
│       ├── citations.py        # Citation normalisation
│       ├── framework_router.py # GDPR/HIPAA/NIST routing logic
│       └── airtable_logger.py  # Audit trail logging
├── frontend/
│   └── app.py                  # Streamlit UI
├── ingestion/
│   ├── chunker.py              # Document chunking pipeline
│   └── embedder.py             # Embedding and Pinecone upload
├── telegram_bot/
│   └── review_bot.py           # Human review bot
├── validation/
│   ├── manual_workbook.xlsx    # LLM-as-judge validation results
│   └── ragas_eval.py           # RAGAS automated evaluation script
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔒 Guardrails

The system implements a three-class policy guardrail layer before any retrieval occurs:

- **Hard-block**: Prompt injection, jailbreak attempts, unsafe requests, explicit off-topic creative prompts
- **Policy-block**: Intent classification for data exfiltration workarounds, private data extraction, misleading compliance framing
- **Review**: Borderline cases escalated for human inspection rather than blocked outright

---

## 🗺️ Roadmap

- [ ] Improve NIST answer correctness with better chunking strategies
- [ ] Add structured review dashboards and SLA tracking in Airtable
- [ ] Role-based authentication and per-user audit trails
- [ ] Hosted deployment with distributed logging and performance alerts
- [ ] Expand to additional frameworks (SOC 2, ISO 27001, CCPA)
- [ ] Multi-language regulatory source support

---

## 🎓 Academic Context

> **TalentSprint Capstone 2026** — Applied Generative AI and Agentic AI  
> Project 3 | Group-5 | Submission: April 15, 2026

This project was developed as the capstone deliverable for the Applied Generative AI and Agentic AI programme, demonstrating advanced RAG engineering, LLMOps integration, and production-grade governance patterns applicable to enterprise compliance use cases.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Please open an issue first to discuss proposed changes.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with precision for regulated industries · Evidence-grounded · Audit-ready**

*If this project helped you, please consider giving it a ⭐*

</div>
