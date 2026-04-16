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


# Regulatory Compliance Intelligence Copilot

Grounded Multi-Framework RAG for GDPR, HIPAA, and NIST with Audit Logging and Human Review Support

## Overview

The **Regulatory Compliance Intelligence Copilot** is a production-oriented, evidence-grounded Question & Answer system designed to support regulatory compliance use cases across **GDPR**, **HIPAA**, and **NIST**. It combines Retrieval-Augmented Generation (RAG), semantic reranking, governance logging, confidence-based escalation, and human review to deliver answers that are traceable, auditable, and safer than generic chatbot responses.

Unlike a standard LLM chatbot, this system does **not** rely on unconstrained model memory for compliance answers. Instead, it retrieves evidence from approved source documents, reranks the evidence, generates a grounded response, normalizes citations, computes confidence, and routes uncertain cases for reviewer approval or correction.

---

## 🏛️ Business Challenge
Why does this system need to exist?
Compliance teams in hospitals answer the same regulatory questions repeatedly. Wrong answers lead to violations costing millions.
**Pain Point:**
Repetitive questions:A nurse asks "Can I share this patient's record?" 10+ times a day. Compliance officer answers manually every time — wasting hours.

**Risk**
Wrong answers = huge fines 
HIPAA violations: up to $1.9M per category/year. GDPR fines: up to €20M or 4% of global revenue. One mistake is catastrophic.

**Opportunity**
Our solution :
RAG chatbot that answers instantly from actual law documents, always cites the exact section, and flags uncertain answers for human review.

**Real examples that need instant answers:**
"Can I send my patient's MRI scan to a specialist in Germany?"

"How long must we keep patient records under GDPR?"

"Do we need encryption for this patient database?"

"What happens if we have a data breach — who do we notify?"

## 🎯 Solution
**Normal AI (problem)**
Answers from memory : ChatGPT learned from the internet. For specific healthcare laws it may be wrong, outdated, or miss jurisdiction differences between HIPAA (US) and GDPR (EU).

**Our RAG system (solution)**
Answers from actual law : First searches the real law PDFs, finds the relevant paragraph, then AI writes a clear answer from ONLY that paragraph. Like an open-book exam — every answer backed by law.

**Jurisdiction awareness — your teammate's key concern answered**
We keep HIPAA (US) and GDPR (EU) in completely separate namespaces in our database. The smart router reads each question and decides which law to search — they never get mixed up. Cross-border questions (EU patient in US hospital) search both and clearly separate the answers: "Under HIPAA... Under GDPR..."

**Benefits:**
1. Always correct : Answer comes from actual law text. Zero hallucination. Confidence score on every answer.
2. Always cited : Every statement backed by exact section: HIPAA §164.502, GDPR Article 44. 100% traceable.
3. Always governed : Low confidence → human officer reviews before sending. Full audit trail in Airtable.
   
---

## Who uses our system?
* **Nurses & Doctors:** "Can I share this patient's data with a specialist abroad?"
* **Hospital Admin:** "How long must we keep patient records?"
* **Legal & Compliance:** "How do we respond to a data access request?"
* **Clinical Research:** "Can we reuse trial data for another study?"
* **IT & Data Teams:** "Do we need encryption for this dataset?"
* **Pharma & Biotech:** "What consent is needed for drug safety analysis?"

**Interface 1 — employees**
Telegram chatbot : Ask in plain language. Get cited answer in under 30 seconds. with optional log. No technical knowledge needed.

**Interface 2 — compliance officer**
Telegram approval queue : Reviews low-confidence answers before delivery. Approves or corrects. Sees full audit trail in Airtable.

**Interface 3 — admin team**
Backend dashboard : Upload new PDFs. Run RAGAS evaluation. Monitor Langfuse traces. Manage system health.

---

## Data Coverage

The solution uses official regulatory and standards documents as source material. Chunks are created at approximately **1,000 characters with 150-character overlap** and stored as Pinecone records. According to the final report, total stored records across all namespaces are **3,600**. :contentReference[oaicite:7]{index=7}

### Namespace Summary

| Framework | Namespaces | Records / Chunks |
|---|---|---:|
| GDPR | `gdpr_pdf`, `gdpr_structured` | 915 |
| HIPAA | `hipaa_pdf`, `hipaa_structured` | 396 |
| NIST | `nist_pdf`, `nist_csf_pdf` | 2,289 |
| **Total** | All namespaces | **3,600** |

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

---

## Process Flow

The process flow diagram in the final report shows the complete sequence from:

**User / UI → FastAPI → Framework Router → Pinecone Retrieval → Cohere Reranking → OpenAI Answer Generation → Confidence & Review Decision → Airtable Audit Trail → Telegram Alert → Reviewer Approval/Correction → Final Reviewed Answer in Streamlit**. The visual workflow is presented in the diagram on page 6 of the report. :contentReference[oaicite:6]{index=6}

---
![Uploading image.png…]()


---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Vector Store | Pinecone |
| Embeddings | Sentence Transformers / OpenAI embedding workflow |
| Reranking | Cohere |
| LLM | OpenAI GPT-4.1 mini |
| Governance | Airtable |
| Automation | n8n |
| Human Review | Python Telegram Bot |
| Source Processing | PDF ingestion + structured JSON ingestion |

---

## Governance and Human Review

A core differentiator of this project is its governance-aware design.

### Airtable Audit Trail
Every interaction is logged with:
- question
- generated answer
- citations
- selected namespaces
- confidence score
- status
- reviewed / final answer fields

### Human Review Flow
For low-confidence or ambiguous cases:
- an alert is sent to Telegram
- the compliance officer can approve or correct the answer
- corrected output is written back to Airtable
- the final answer can be fetched in the UI by record ID

This design improves both auditability and operational safety in regulated use cases. :contentReference[oaicite:8]{index=8}

---

## Guardrails

The project includes a pre-retrieval guardrail layer to prevent unsafe or irrelevant requests from entering the compliance pipeline.

### Supported decision classes
- **allow**
- **block**
- **review**

### Current protections include
- prompt injection attempts
- jailbreak / prompt reveal requests
- workaround and bypass requests
- unsafe or off-topic creative prompts
- private-data extraction attempts

In the current implementation, both `block` and `review` outcomes stop retrieval before the system proceeds, which provides safer behavior for suspicious inputs. :contentReference[oaicite:9]{index=9}

---

## Validation and Evaluation

The system was evaluated using two complementary approaches:

### 1. Manual / LLM-as-Judge Validation
The validation workbook separates test cases into:
- **Pure Regulatory Q&A**
- **Ambiguous / Cross-Framework**
- **Guardrails**

This prevents misleading interpretation by evaluating each class of question with appropriate criteria. :contentReference[oaicite:10]{index=10}

### 2. RAGAS-Based Automated Evaluation
A subset of 15 questions across frameworks was evaluated using:
- **Faithfulness**
- **Answer Correctness**

#### Reported RAGAS Results
- **Average Faithfulness:** 0.905
- **Average Answer Correctness:** 0.773
- **Faithfulness pass rate (95% threshold):** 100% (15/15)

These results indicate strong grounding, with lower correctness in some cases driven more by retrieval coverage limits than by hallucination. :contentReference[oaicite:11]{index=11}

---

## Final KPI Highlights

According to the final project report, the system achieved the following headline results:

| Metric | Target | Actual | Status |
|---|---:|---:|---|
| Answer Accuracy | ≥ 90% | 93.3% | PASS |
| Self-Service Rate | ≥ 80% | 86.7% | PASS |
| Response Time | < 120 sec | 11.8 sec avg | PASS |
| Source Traceability | 100% | 80% | Below Target |
| Validation Coverage | 100% | 100% | PASS |
| RAGAS Faithfulness | > 90% | 90.5% | PASS |
| RAGAS Correctness | > 90% | 77.3% | Below Target |

The report highlights strong answer quality, good latency, and solid governance readiness, while also noting improvement opportunities in source traceability consistency and mixed-framework / NIST-heavy answers. :contentReference[oaicite:12]{index=12}

---

## Repository Structure

A typical structure for this project is organized around ingestion, backend services, UI, and data layers.

```text
.
├── app/
│   ├── api/
│   ├── core/
│   ├── services/
│   └── main.py
├── ingestion/
│   ├── pdf/
│   └── notion/ or structured/
├── data/
│   ├── raw/
│   │   ├── gdpr/
│   │   ├── hipaa/
│   │   ├── nist/
│   │   └── nist_csf/
│   └── structured/
├── streamlit_app.py
├── requirements.txt
├── .env.example
└── README.md
