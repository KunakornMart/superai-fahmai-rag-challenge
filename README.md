# Super AI Engineer S6 – FahMai RAG Challenge

> Retrieval-Augmented Generation (RAG) solution for Thai product-support question answering in **Super AI Engineer Season 6 – FahMai RAG Challenge (Level 1)**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Retrieval--Augmented--Generation-7B61FF)
![Thai NLP](https://img.shields.io/badge/Thai%20NLP-Question%20Answering-2EC866)
![Super AI Engineer](https://img.shields.io/badge/Super%20AI%20Engineer-Season%206-F36F21)
![Score](https://img.shields.io/badge/Score-1.00-EDB227)

---

## Highlights

| Item | Result |
|---|---:|
| Competition | **Super AI Engineer Season 6 – FahMai RAG Challenge (Level 1)** |
| Task | Thai RAG / Multiple-choice Question Answering |
| Final Score | **1.00** |
| Rank | **17 / 341 participants** |
| Evaluation Metric | Accuracy |
| Organizer | Artificial Intelligence Association of Thailand (AIAT) |
| Certificate | [Verify credential](https://mysuperai.aiat.or.th/certificate/hack3/600637) |

---

## Project Overview

**FahMai (ฟ้าใหม่)** is a fictional Thai electronics store.  
The challenge was to build a **Retrieval-Augmented Generation (RAG)** system that answers **100 Thai multiple-choice questions** using a provided knowledge base.

The knowledge base contains Thai documents about:

- Product pages
- Product specifications and prices
- Store policies
- Return and warranty rules
- Shipping and membership details
- Store information, branches, contact details, FAQ, and buying guides

Each question contains **10 answer choices**.

| Choice | Meaning |
|---:|---|
| 1–8 | Content-specific answers |
| 9 | No data available in the knowledge base |
| 10 | This question is not related to FahMai store |

The system must retrieve relevant evidence from the knowledge base and select the correct answer choice.

---

## Repository Structure

```text
.
├── README.md
├── data/
│   ├── knowledge_base/
│   │   ├── policies/
│   │   ├── products/
│   │   └── store_info/
│   ├── questions.csv
│   └── sample_submission.csv
├── docs/
├── notebooks/
└── src/
```

---

## Folder Guide

| Path | Description |
|---|---|
| [`data/`](./data) | Competition dataset used in the project |
| [`data/knowledge_base/`](./data/knowledge_base) | Thai markdown knowledge base for retrieval |
| [`data/knowledge_base/products/`](./data/knowledge_base/products) | Product pages, specifications, prices, features, and related product information |
| [`data/knowledge_base/policies/`](./data/knowledge_base/policies) | Store policies such as return, warranty, shipping, membership, and service rules |
| [`data/knowledge_base/store_info/`](./data/knowledge_base/store_info) | Store overview, branch information, contact details, FAQ, and buying guides |
| [`data/questions.csv`](./data/questions.csv) | 100 Thai multiple-choice questions |
| [`data/sample_submission.csv`](./data/sample_submission.csv) | Official submission format |
| [`notebooks/`](./notebooks) | Main experiment notebook and solution workflow |
| [`src/`](./src) | Utility scripts such as submission validation |
| [`docs/`](./docs) | Additional documentation, notes, and LinkedIn-ready project text |

---

## Dataset Description

The dataset contains a Thai knowledge base and question file.

### Knowledge Base

The knowledge base is organized into three major document groups.

| Folder | Content |
|---|---|
| `products/` | Product descriptions, specifications, prices, features, and related product details |
| `policies/` | Return policy, warranty policy, shipping policy, membership rules, and service terms |
| `store_info/` | Store overview, contact information, branches, FAQ, promotions, and buying guides |

All knowledge base documents are written in Thai and stored as Markdown files.

### Questions

The `questions.csv` file contains 100 questions.

Each row contains:

```text
id
question
choice_1
choice_2
...
choice_10
```

### Submission Format

The official submission must contain exactly two columns:

```csv
id,answer
1,5
2,3
3,7
...
100,2
```

Rules:

- `id` must be an integer from 1 to 100
- `answer` must be an integer from 1 to 10
- The file must contain exactly 100 rows
- No missing IDs
- No duplicated IDs

---

## Challenge Constraints

The competition required participants to use only the provided ThaiLLM models:

- `OpenThaiGPT-ThaiLLM-8B-instruct-v7.2`
- `Pathumma-ThaiLLM-qwen3-8b-think-3.0.0`
- `Typhoon-S-ThaiLLM-8B-Instruct`
- `THaLLE-0.2-ThaiLLM-8b-fa`

The ThaiLLM APIs were available through the official ThaiLLM playground.

---

## Methodology

This project uses an evidence-grounded RAG workflow.

```text
Question
   ↓
Thai text normalization
   ↓
Knowledge base loading
   ↓
Document chunking
   ↓
Hybrid retrieval
   ↓
Evidence reranking
   ↓
Choice-aware answer matching
   ↓
Special-case handling
   ↓
ThaiLLM fallback / deterministic decision
   ↓
Submission CSV
```

---

## Technical Approach

### 1. Thai Text Normalization

Thai text can be difficult to retrieve directly because spacing and punctuation are often inconsistent.  
The preprocessing step normalizes both knowledge base documents and questions.

Main steps include:

- Unicode normalization
- Lowercasing where applicable
- Whitespace cleanup
- Thai punctuation cleanup
- Product and policy term normalization
- Choice text normalization
- Keyword preservation for Thai store-specific terms

---

### 2. Knowledge Base Construction

Markdown files are loaded from the three knowledge base folders:

- `products/`
- `policies/`
- `store_info/`

Each document is converted into searchable chunks with metadata such as:

- Source folder
- File name
- Document category
- Raw text content

This metadata is useful for tracing which document supports each answer.

---

### 3. Hybrid Retrieval

The solution combines lexical and semantic retrieval to improve recall.

Main retrieval components:

- **BM25** via `rank-bm25`
- **Dense embeddings** via `sentence-transformers`
- Embedding model: `intfloat/multilingual-e5-large`
- Thai tokenization via `PyThaiNLP`
- Score merging / ranking for top evidence selection

BM25 helps capture exact keyword matches, while dense embeddings improve semantic matching when the wording differs between the question and the knowledge base.

---

### 4. Evidence Reranking

After retrieval, the system narrows down the most relevant chunks before answering.

The reranking step considers:

- Question terms
- Choice terms
- Product names
- Policy keywords
- Store-specific terminology
- Retrieved document category

This reduces irrelevant context and improves answer stability.

---

### 5. Choice-Aware Answer Selection

This challenge is not open-ended generation.  
The system must select exactly one answer from 10 choices.

The pipeline compares each answer choice against retrieved evidence and assigns support based on:

- Direct text overlap
- Product or policy match
- Semantic relevance
- Numeric or factual consistency
- Category match between question intent and evidence source

---

### 6. Special Answer Handling

The competition includes two special answer classes.

| Choice | Meaning | Handling |
|---:|---|---|
| 9 | ไม่มีข้อมูลนี้ในฐานข้อมูล | Used when the question is related to FahMai but the knowledge base does not contain enough evidence |
| 10 | คำถามนี้ไม่เกี่ยวข้องกับร้านฟ้าใหม่ | Used when the question is outside the FahMai store domain |

The pipeline includes rule-based checks to avoid forcing unsupported questions into content-specific answers.

---

### 7. ThaiLLM-Assisted Reasoning

The solution can use ThaiLLM reasoning as a fallback when retrieval and deterministic scoring are not confident enough.

The ThaiLLM call is designed to:

- Read retrieved evidence
- Compare evidence against the 10 choices
- Return only the selected choice number
- Avoid unsupported hallucinated answers

---

### 8. Submission Validation

Before submission, the output is validated to make sure it follows the official format.

Validation checks:

- Correct columns: `id,answer`
- Exactly 100 rows
- IDs from 1 to 100
- No missing IDs
- No duplicated IDs
- Answers are integers from 1 to 10

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/KunakornMart/superai-fahmai-rag-challenge.git
cd superai-fahmai-rag-challenge
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Open the Notebook

Open the main solution notebook inside:

```text
notebooks/
```

Then run the notebook step by step.

### 4. Add ThaiLLM API Key

If running the ThaiLLM-based parts, set your API key using your preferred environment method.

Example:

```bash
export THAILLM_API_KEY="your_api_key_here"
```

Do not commit real API keys to GitHub.

### 5. Validate Submission

If using the validation script:

```bash
python src/validate_submission.py results/submission.csv
```

---

## Expected Output

A valid submission file should look like this:

```csv
id,answer
1,5
2,3
3,7
...
100,2
```

The final answer column must contain only integers from `1` to `10`.

---

## Skills Demonstrated

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Thai Natural Language Processing
- Information Retrieval
- BM25 Retrieval
- Dense Embedding Retrieval
- Hybrid Search
- Evidence-grounded Question Answering
- Multiple-choice Answer Selection
- Prompt Engineering
- Rule-based Reasoning
- Data Validation
- Python
- Competition Pipeline Design

---

## Key Takeaways

This project demonstrates how RAG can be adapted for Thai-language product-support question answering.

The main challenge was not only retrieving relevant documents, but also mapping retrieved evidence to one of ten answer choices while correctly handling unsupported and unrelated questions.

Important lessons from this project:

- Thai document retrieval requires careful normalization and tokenization
- Dense retrieval and BM25 complement each other well
- Multiple-choice RAG needs answer-choice-aware scoring, not only document retrieval
- Rule-based checks are useful for handling out-of-domain or missing-information cases
- Submission validation is essential in competition settings

---

## Competition Details

| Item | Detail |
|---|---|
| Challenge | FahMai RAG Challenge Level 1 |
| Program | Super AI Engineer Season 6 |
| Start Date | Mar 27, 2026 |
| Close Date | Mar 29, 2026 |
| Evaluation | Accuracy |
| Task | Answer 100 Thai multiple-choice questions |
| Dataset License | MIT |

---

## LinkedIn Project Description

Built a retrieval-augmented generation pipeline for Thai product-support question answering using a knowledge base of product pages, store policies, and store information. The system combines hybrid retrieval, Thai text normalization, evidence reranking, choice-aware scoring, and ThaiLLM-assisted reasoning to select answers from 10 multiple-choice options.

Achieved a perfect score of **1.00** and ranked **17/341 participants**.

---

## Certificate

FahMai RAG Hackathon Certificate:  
https://mysuperai.aiat.or.th/certificate/hack3/600637

---

## Author

**Kunakorn Pruksakorn**  
Automation Engineer · Data Science · AI / LLM / RAG · Industrial IoT

- GitHub: [KunakornMart](https://github.com/KunakornMart)
- Portfolio: [kunakornmart.github.io](https://kunakornmart.github.io)
- LinkedIn: [Kunakorn Pruksakorn](https://linkedin.com/in/kunakorn-pruksakorn)

---

## License

This repository is provided for portfolio and educational purposes.

Dataset license follows the original competition dataset license.
