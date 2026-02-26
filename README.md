# Regulatory-Compliance-Q-A-System
An AI-powered "Retrieval Augmented Generation (RAG)" system designed to automate regulatory inquiries for healthcare. This tool ensures that compliance teams receive accurate, cited, and validated answers regarding GDPR, HIPAA, SOX, and more.

---

## 🏛️ Business Challenge
Compliance teams are often overwhelmed by repetitive regulatory questions. Inaccurate guidance in high-stakes industries like healthcare can lead to violations costing millions of dollars in fines and legal fees.

## 🎯 Project Objective
To build a validated RAG system that:
* Provides instant answers to employee questions about complex regulations.
* Ensures **100% source traceability** with exact citations.
* Minimizes human error through a multi-layered validation workflow.

---

## 🛠️ Tech Stack & Tools
* **Orchestration:** N8N / LangFlow
* **Vector Database:** Pinecone
* **Data Management:** Notion & Airtable
* **Reranking:** Cohere Rerank
* **Interface:** Telegram / Slack
* **LLM Integration:** Semantic chunking and multi-query retrieval models

---

## 🏗️ Implementation Approach

### 1. Knowledge Base Architecture
Regulations are structured in **Notion** using hierarchical tagging: 
`Regulation` → `Article` → `Section`.

### 2. RAG Pipeline
#### 📂 Document Processing
- Upload regulation PDFs to vector DB
- Add metadata (date, jurisdiction)
- Semantic chunking with overlap
- Context-preserving segmentation

#### 🔎 Retrieval Strategy
- Multi-query retrieval (3 rephrased queries)
- Semantic similarity search
- Reranking via Cohere Rerank
- Return top relevant chunks
  
### 3. Answer Generation & Validation
* **Expert Prompting:** The system is constrained to answer *only* based on provided sources and must quote exact text.
* **Confidence Scoring:** Every answer includes a reliability metric.
* **Human-in-the-loop:** A validation layer via **Airtable** allows compliance officers to approve or version-control answers before they reach the end-user.

---

## 📊 Success Metrics
| Metric | Target |
| :--- | :--- |
| **Answer Accuracy** | 95%+ |
| **Self-Service Rate** | 80% |
| **Response Time** | < 2 Minutes |
| **Traceability** | 100% Source Citation |

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

---

## 📦 Deliverables
1.  **Chatbot Interface:** A functional RAG-enabled bot (Telegram/Slack).
2.  **Technical Report:** Documentation of dataset setup, vector DB architecture, and validation workflows.
3.  **Performance Summary:** Final audit of system accuracy and citation reliability.

---
