<img width="550" height="391" alt="image" src="https://github.com/user-attachments/assets/100991bf-39e0-444c-97b3-0b485e120b2f" /># Regulatory-Compliance-Q-A-System
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

### 3️⃣ Answer Generation

**System Prompt:**

You are a compliance expert.
Answer ONLY from provided sources.
Quote exact regulatory text.


Features:
- Exact quotations
- Section citations
- Confidence score
- Hallucination guardrails

---

### 4️⃣ Validation Workflow

- Airtable approval forms
- Workflow:

Question → AI Answer → Officer Review → Approval → Version Log

- Full audit trail
- Version history tracking

---

### 5️⃣ Chatbot Interface

Deployment Options:
- Telegram Bot
- Slack Integration
- Internal Web App
- Microsoft Teams

---

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| Orchestration | N8N / LangFlow |
| Vector DB | Pinecone |
| Reranking | Cohere |
| Workflow | Airtable |
| Interface | Telegram / Slack |
| Integration | APIs / Webhooks |

---

## 📊 Success Metrics

- 95%+ Accuracy  
- 80% Self-Service Rate  
- <2 Min Response Time  
- 100% Source Traceability  
- Zero Hallucinated Citations  

---

## 📚 Dataset Sources

### 🏛️ GDPR
- Official Regulation (EU) 2016/679
- GDPR NLP Dataset (HuggingFace)
- GDPR Articles Dataset (Kaggle)
- GDPR Violations Dataset (Kaggle)
- NIST SP 800-53 Rev.5

### 🏥 HIPAA
- HIPAA Privacy Rule Summary
- Limited Data Set Documentation

### 🔄 Additional Sources
- Synthetic compliance queries
- Internal anonymized manuals
- Sample policy documents

---

## 📦 Expected Deliverables

1. RAG-enabled Compliance Chatbot  
2. Architecture & Validation Documentation  
3. Performance Summary Report  

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
