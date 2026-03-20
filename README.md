# Regulatory-Compliance-Q-A-System
An AI-powered "Retrieval Augmented Generation (RAG)" system designed to automate regulatory inquiries for healthcare. This tool ensures that compliance teams receive accurate, cited, and validated answers regarding GDPR, HIPAA, SOX, and more.

Domain: Healthcare  ·  Jurisdictions: US (HIPAA) + EU (GDPR)  ·  Stack: LangChain · Pinecone · HuggingFace · N8N
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
Telegram chatbot : Ask in plain language. Get cited answer in under 2 minutes. No login. No technical knowledge needed.

**Interface 2 — compliance officer**
Airtable approval queue : Reviews low-confidence answers before delivery. Approves or corrects. Sees full audit trail.

**Interface 3 — admin team**
Streamlit dashboard : Upload new PDFs. Run RAGAS evaluation. Monitor Langfuse traces. Manage system health.


---

## 🏗️ Datasets
### 1. Documents used 

<img width="1007" height="671" alt="image" src="https://github.com/user-attachments/assets/2b16ab0c-796f-4187-825b-4e2551bf2f16" />


**Chunk metadata** — answers teammate's question on metadata structure
Every chunk stored with: regulation · jurisdiction · section_type · version · effective_date · citation · is_deprecated. Router uses jurisdiction tag to never mix HIPAA and GDPR searches.

  
---

### Architecture - 5 zones — what lives where

**Zone A:** - regulation documents (download once)
- HIPAA PDFs (hhs.gov)
- GDPR PDF (eur-lex.europa.eu)
- NIST 800-53 PDF
- HuggingFace GDPR dataset
- GDPR Violations (Kaggle)
- 30 synthetic Q&A test pairs

**Zone B :** - GitHub Codespace (write & test all Python)
- ingest.py — chunk + embed to Pinecone
- rag_pipeline.py — full retrieval logic
- app.py — FastAPI server
- evaluator.py — RAGAS scoring
- ui.py — Streamlit 4 tabs

**Zone C :** - HuggingFace Space (live Python backend)
- FastAPI public URL
- Streamlit UI
- RAGAS evaluator
- Langfuse auto-trace

**Zone D :** - Zone D — external stores
- Pinecone — 3 namespaces
- Airtable — audit log
- Langfuse — live traces

**Zone E :** - N8N (workflow + governance)
- Telegram trigger
- HTTP POST → HuggingFace
- Airtable audit logging
- Confidence check
- Approval workflow
- RAGAS score report
- Version alerts

**Note: ** N8N cannot run Python. All ML logic (RAG, RAGAS, Langfuse) lives in HuggingFace. N8N calls POST /query with {question, user_id, role} and receives {answer, citations, confidence, regulation} back as JSON._

---

### Validation Workflow

- Airtable approval forms
- Workflow:

Question → AI Answer → Officer Review → Approval → Version Log

- Full audit trail
- Version history tracking

---

### Pipeline (7 steps · 5 LLM calls · 3.5 seconds)

**Step1: User asks in Telegram** → N8N sends JSON to HuggingFace - N8N records: user_id, role, timestamp. Sends {question, user_id, role} via HTTP POST.

**Step 2: LLM calls 1–3 run in parallel via asyncio — total ~0.5s**

**LLM Call 1 :** Query structuring + Step-back
Extracts: regulations list, legal keywords, metadata filters, broader concept question. Decides jurisdiction: US/EU/both.

**LLM Call 2 :** ** HyDE**
Writes fake regulation-style answer in legal vocabulary. Embeds this — not the original question. Fixes casual vs legal language gap.

**LLM Call 3** RAG Fusion
Generates 4 query variations. Each searched separately. RRF scores: chunks appearing in more searches ranked higher.


**Step3 : Hybrid search across correct namespaces (parallel)**
**Dense (Pinecone):** Semantic search using HyDE embedding + jurisdiction filter. HIPAA searches HIPAA namespace only. GDPR searches GDPR namespace only. They never mix.
**Sparse (BM25):** Exact keyword search using extracted legal terms like "§164.312" and "Article 44".

**Step4:**
Cohere reranker → top 6 chunks selected
All retrieved chunks merged. Cohere specialist model picks top 6 most relevant. Removes noise before LLM sees anything. Not an LLM — dedicated reranker model.

**Step 5:**
LLM Call 4 — final answer with forced citations
Claude/GPT-4o-mini reads 6 law chunks. Rules: answer ONLY from chunks, cite exact sections, structure multi-regulation answers clearly ("Under HIPAA... Under GDPR..."), include confidence score.

**Step6 :**
**Score ≥ 0.8** — direct delivery (Answer sent to employee via Telegram immediately. 80% of all questions.)
**⚠️ Score < 0.8** — human review (Compliance officer reviews in Airtable. Approves or corrects. Then sent.)

**Step7 : Audit log + Langfuse trace recorded automatically**
Airtable: user_id, question, answer, citations, confidence, timestamp, approved_by.
Langfuse: latency per step, token count, cost per query — proves <2 min response metric.


---

## 🛠️ Tech Stack

<img width="853" height="797" alt="image" src="https://github.com/user-attachments/assets/48baa06b-dd43-4b26-8652-6f8ef207f44d" />


---

## 📊 Governance 

**What makes this enterprise-grade**

Product Features:

1. **Multi-regulation router :** Outputs a LIST of namespaces — ["HIPAA","GDPR"] — not one label. Searches all relevant jurisdictions in parallel. Answers teammate's concern about mixing.
2. **Audit logging :** Every query → Airtable row: user, question, answer, citations, confidence, timestamp, approved_by. Full traceable history.
3. **Approval workflow :** Confidence <0.8 → N8N creates Airtable record → compliance officer notified → reviews → approves or edits → sent to user.
4. **Document versioning :** Every chunk tagged with version + effective_date. Old chunks marked deprecated when new PDF uploaded. Answers always from current law.
5. **Live document upload :** Admin uploads new regulation PDF → Streamlit calls /ingest → auto-chunks → Pinecone updated → immediately searchable.
6. **RBAC (simulated) :** Role tag on every query: employee/officer/admin. System prompt adjusts detail level. Demonstrates concept without full auth complexity.
7. **Jurisdiction awareness :** metadata.jurisdiction = "US" or "EU". Router filters by jurisdiction. HIPAA and GDPR never searched together unless question explicitly spans both.
8. **Langfuse monitoring :** One line of code. Auto-traces every query: latency per step, token count, cost. Dashboard open during presentation — live proof.
9. **Violation risk warning :** GDPR Violations dataset loaded. AI can add: "Companies were fined €X for similar violations." Makes answers more actionable.


---

## Evaluation

<img width="730" height="486" alt="image" src="https://github.com/user-attachments/assets/4ae4ddee-30fb-4536-b948-e191b0f0f156" />


###  Demo
<img width="730" height="471" alt="image" src="https://github.com/user-attachments/assets/0bd3e9cd-07ef-4c17-8e6e-e40a04d7d06e" />


---

## 🧠 Key Capabilities

- Multi-jurisdiction compliance intelligence  
- Semantic retrieval & reranking  
- Audit-ready traceability  
- Human-in-the-loop governance  
- Enterprise scalability  

---

## 🚀 Future Enhancements

- Automated regulation updates
- Cross-regulation reasoning
- Compliance risk scoring
- Analytics dashboard
- Enterprise SSO integration

---

## 🏁 Conclusion

Enterprise-grade regulatory intelligence system combining:

AI + Governance + Traceability = Compliance Confidence

---

## 📦 Deliverables
1.  **Chatbot Interface:** A functional RAG-enabled bot (Telegram/Slack).
2.  **Technical Report:** Documentation of dataset setup, vector DB architecture, and validation workflows.
3.  **Performance Summary:** Final audit of system accuracy and citation reliability.

---
## 📂 Dataset Sources
The system utilizes a mix of authoritative public texts and synthetic data:

### EU General Data Protection Regulation (GDPR)
* [Official EU Text (Regulation 2016/679)](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679)
* [GDPR NLP Dataset (HuggingFace)](https://huggingface.co/datasets/AndreaSimeri/GDPR)
* [GDPR Articles & Violations (Kaggle)](https://www.kaggle.com/datasets/jessemostipak/gdpr-violations)
* [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

### Health Insurance Portability and Accountability Act (HIPAA)
* [HIPAA Privacy Rule Summary](https://www.hhs.gov/hipaa/for-professionals/privacy/index.html)
* [Limited Data Set Guidelines](https://www.hhs.gov/hipaa/for-professionals/faq/limited-data-set/index.html)
